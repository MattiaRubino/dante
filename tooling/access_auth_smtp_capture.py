from __future__ import annotations

import json
import socketserver
import threading
from dataclasses import dataclass
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit


@dataclass(frozen=True, slots=True)
class CapturedEmail:
    recipient: str
    subject: str
    body: str


class EmailCaptureStore:
    """Thread-safe in-memory sink scoped to one disposable full-stack run."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._messages: list[CapturedEmail] = []

    def append(self, message: CapturedEmail) -> None:
        with self._lock:
            self._messages.append(message)

    def latest(self, *, recipient: str, subject: str | None) -> CapturedEmail | None:
        with self._lock:
            for message in reversed(self._messages):
                if message.recipient.casefold() != recipient.casefold():
                    continue
                if subject is not None and message.subject != subject:
                    continue
                return message
        return None

    def clear(self) -> None:
        with self._lock:
            self._messages.clear()


class _SmtpServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address: tuple[str, int], store: EmailCaptureStore) -> None:
        self.store = store
        super().__init__(server_address, _SmtpHandler)


class _SmtpHandler(socketserver.StreamRequestHandler):
    """Minimal SMTP sink implementing the command set used by smtplib.send_message."""

    _MAX_LINE_BYTES = 16_384
    _MAX_MESSAGE_BYTES = 1_048_576

    def handle(self) -> None:
        self._mail_from: str | None = None
        self._recipients: list[str] = []
        self._reply(220, "dante-e2e-smtp ESMTP ready")

        while True:
            raw_line = self.rfile.readline(self._MAX_LINE_BYTES + 1)
            if not raw_line:
                return
            if len(raw_line) > self._MAX_LINE_BYTES:
                self._reply(500, "line too long")
                return

            line = raw_line.rstrip(b"\r\n")
            command, separator, argument = line.partition(b" ")
            command_upper = command.upper()

            if command_upper in {b"EHLO", b"HELO"}:
                self._reply(250, "dante-e2e-smtp")
                continue
            if command_upper == b"NOOP":
                self._reply(250, "ok")
                continue
            if command_upper == b"RSET":
                self._reset_envelope()
                self._reply(250, "ok")
                continue
            if command_upper == b"QUIT":
                self._reply(221, "bye")
                return
            if command_upper == b"MAIL" and separator and argument.upper().startswith(b"FROM:"):
                self._mail_from = self._mailbox(argument[5:])
                self._recipients.clear()
                if self._mail_from is None:
                    self._reply(501, "invalid sender")
                else:
                    self._reply(250, "ok")
                continue
            if command_upper == b"RCPT" and separator and argument.upper().startswith(b"TO:"):
                recipient = self._mailbox(argument[3:])
                if self._mail_from is None or recipient is None:
                    self._reply(503, "bad sequence or recipient")
                else:
                    self._recipients.append(recipient)
                    self._reply(250, "ok")
                continue
            if command_upper == b"DATA" and not argument:
                if self._mail_from is None or not self._recipients:
                    self._reply(503, "bad sequence")
                    continue
                self._reply(354, "end data with <CR><LF>.<CR><LF>")
                payload = self._read_data()
                if payload is None:
                    self._reply(552, "message too large")
                    self._reset_envelope()
                    continue
                try:
                    self._capture(payload)
                except ValueError:
                    self._reply(550, "malformed message")
                    self._reset_envelope()
                    continue
                self._reply(250, "accepted")
                self._reset_envelope()
                continue

            self._reply(502, "command not implemented")

    def _read_data(self) -> bytes | None:
        chunks: list[bytes] = []
        total = 0
        overflow = False
        while True:
            line = self.rfile.readline(self._MAX_LINE_BYTES + 1)
            if not line:
                raise ValueError("SMTP client disconnected during DATA")
            if line in {b".\r\n", b".\n"}:
                break
            if line.startswith(b".."):
                line = line[1:]
            total += len(line)
            if total > self._MAX_MESSAGE_BYTES:
                overflow = True
            if not overflow:
                chunks.append(line)
        return None if overflow else b"".join(chunks)

    def _capture(self, payload: bytes) -> None:
        parsed = BytesParser(policy=policy.default).parsebytes(payload)
        subject = str(parsed.get("Subject", ""))
        body_part = parsed.get_body(preferencelist=("plain",))
        body = body_part.get_content() if body_part is not None else parsed.get_payload()
        if not isinstance(body, str):
            raise ValueError("captured email has no textual body")

        store = self.server.store  # type: ignore[attr-defined]
        for recipient in self._recipients:
            store.append(CapturedEmail(recipient=recipient, subject=subject, body=body))

    @staticmethod
    def _mailbox(raw: bytes) -> str | None:
        candidate = raw.strip()
        if candidate.startswith(b"<") and candidate.endswith(b">"):
            candidate = candidate[1:-1]
        try:
            value = candidate.decode("ascii")
        except UnicodeDecodeError:
            return None
        if not value or any(character in value for character in "\r\n"):
            return None
        return value

    def _reset_envelope(self) -> None:
        self._mail_from = None
        self._recipients.clear()

    def _reply(self, status: int, message: str) -> None:
        self.wfile.write(f"{status} {message}\r\n".encode("ascii"))
        self.wfile.flush()


class _ControlHandler(BaseHTTPRequestHandler):
    store: EmailCaptureStore

    def do_GET(self) -> None:
        parsed = urlsplit(self.path)
        if parsed.path != "/latest":
            self._json(404, {"error": "not_found"})
            return
        query = parse_qs(parsed.query, keep_blank_values=False)
        recipient_values = query.get("recipient", [])
        subject_values = query.get("subject", [])
        if len(recipient_values) != 1 or len(subject_values) > 1:
            self._json(400, {"error": "invalid_query"})
            return
        message = self.store.latest(
            recipient=recipient_values[0],
            subject=subject_values[0] if subject_values else None,
        )
        if message is None:
            self._json(404, {"error": "not_found"})
            return
        self._json(
            200,
            {
                "recipient": message.recipient,
                "subject": message.subject,
                "body": message.body,
            },
        )

    def do_DELETE(self) -> None:
        if urlsplit(self.path).path != "/messages":
            self._json(404, {"error": "not_found"})
            return
        self.store.clear()
        self._json(204, None)

    def _json(self, status: int, payload: object) -> None:
        body = b"" if payload is None else json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        if body:
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def log_message(self, _format: str, *args: object) -> None:
        _ = args


@dataclass(slots=True)
class SmtpCaptureRuntime:
    store: EmailCaptureStore
    smtp_server: _SmtpServer
    smtp_thread: threading.Thread
    control_server: ThreadingHTTPServer
    control_thread: threading.Thread

    @property
    def smtp_port(self) -> int:
        return int(self.smtp_server.server_address[1])

    @property
    def control_port(self) -> int:
        return int(self.control_server.server_address[1])

    def close(self) -> None:
        self.smtp_server.shutdown()
        self.control_server.shutdown()
        self.smtp_thread.join(timeout=2)
        self.control_thread.join(timeout=2)
        self.smtp_server.server_close()
        self.control_server.server_close()


def start_smtp_capture() -> SmtpCaptureRuntime:
    """Start loopback-only SMTP + control surfaces for one full-stack E2E run."""
    store = EmailCaptureStore()
    smtp_server = _SmtpServer(("127.0.0.1", 0), store)

    handler_type = type("BoundControlHandler", (_ControlHandler,), {"store": store})
    control_server = ThreadingHTTPServer(("127.0.0.1", 0), handler_type)

    smtp_thread = threading.Thread(target=smtp_server.serve_forever, daemon=True)
    control_thread = threading.Thread(target=control_server.serve_forever, daemon=True)
    smtp_thread.start()
    control_thread.start()
    return SmtpCaptureRuntime(
        store=store,
        smtp_server=smtp_server,
        smtp_thread=smtp_thread,
        control_server=control_server,
        control_thread=control_thread,
    )
