from __future__ import annotations
import argparse, base64, gzip, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
M=json.loads((ROOT/"manifest.json").read_text(encoding="utf-8"))
ORACLE=ROOT/M["oracle"]["path"]
STYLE_RE=re.compile(r"<style(?:\s[^>]*)?>(.*?)</style>",re.S|re.I)
SCRIPT_RE=re.compile(r"<script(?:\s[^>]*)?>(.*?)</script>",re.S|re.I)
STYLE_PTR="DANTE_A2_ORACLE_POINTER style"
SCRIPT_PTR="DANTE_A2_ORACLE_POINTER script"
TEMPLATE_PTR="DANTE_A2_ORACLE_TEMPLATE_POINTER"
HUNK_RE=re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def oracle_text():
    data=ORACLE.read_bytes()
    exp=M["oracle"]
    if len(data)!=exp["size_bytes"] or sha256(data)!=exp["sha256"]:
        raise RuntimeError("retained complete oracle identity mismatch")
    return data.decode("utf-8")

def blocks(text):
    return [m.group(1) for m in STYLE_RE.finditer(text)],[m.group(1) for m in SCRIPT_RE.finditer(text)]

def derive_template(oracle):
    styles=list(STYLE_RE.finditer(oracle)); scripts=list(SCRIPT_RE.finditer(oracle))
    nested=set()
    for si,sm in enumerate(styles,1):
        if any(jm.start(1)<=sm.start() and sm.end()<=jm.end(1) for jm in scripts): nested.add(si)
    repl=[]
    repl += [(m.start(1),m.end(1),f"__DANTE_A2_SCRIPT_{i:02d}__") for i,m in enumerate(scripts,1)]
    repl += [(m.start(1),m.end(1),f"__DANTE_A2_STYLE_{i:02d}__") for i,m in enumerate(styles,1) if i not in nested]
    out=oracle
    for a,b,v in sorted(repl,reverse=True): out=out[:a]+v+out[b:]
    return out

def template(oracle):
    p=ROOT/M["template"]; src=p.read_text(encoding="utf-8")
    return derive_template(oracle) if TEMPLATE_PTR in src else src

def resolve_asset(oracle):
    a=M["asset"]; src=(ROOT/a["file"]).read_text(encoding="utf-8")
    if not src.startswith("DANTE_A2_EMBEDDED_ASSET_POINTER_V1"):
        b64="".join(src.split()); data=base64.b64decode(b64,validate=True)
    else:
        prefix=a["source_prefix"]; start=oracle.find(prefix)
        if start<0: raise RuntimeError("embedded day-ribbon asset missing")
        start+=len(prefix); alphabet=set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="); end=start
        while end<len(oracle) and oracle[end] in alphabet: end+=1
        b64=oracle[start:end]; data=base64.b64decode(b64,validate=True)
    if len(data)!=a["decoded_size_bytes"] or sha256(data)!=a["decoded_sha256"]:
        raise RuntimeError("day-ribbon asset identity mismatch")
    return b64

def module(group,kind,osb,ojb):
    src=(ROOT/group["file"]).read_text(encoding="utf-8")
    ptr=STYLE_PTR in src if kind=="style" else SCRIPT_PTR in src
    if ptr:
        base=osb if kind=="style" else ojb
        return [base[n-1] for n in group["blocks"]]
    sep=M["style_separator"] if kind=="style" else M["script_separator"]
    chunks=src.split(sep)
    if len(chunks)!=len(group["blocks"]): raise RuntimeError(f"{kind} chunk mismatch: {group['file']}")
    return chunks

def apply_unified_diff(original: str, patch: str) -> str:
    src=original.splitlines(True); out=[]; src_idx=0
    lines=patch.splitlines(True); i=0
    while i<len(lines) and not lines[i].startswith("@@"): i+=1
    while i<len(lines):
        m=HUNK_RE.match(lines[i])
        if not m: raise RuntimeError(f"invalid unified diff hunk: {lines[i].rstrip()}")
        old_start=int(m.group(1))-1
        out.extend(src[src_idx:old_start]); src_idx=old_start; i+=1
        while i<len(lines) and not lines[i].startswith("@@"):
            line=lines[i]
            if line.startswith(" "):
                expected=line[1:]
                if src_idx>=len(src) or src[src_idx]!=expected: raise RuntimeError("override context mismatch")
                out.append(src[src_idx]); src_idx+=1
            elif line.startswith("-"):
                expected=line[1:]
                if src_idx>=len(src) or src[src_idx]!=expected: raise RuntimeError("override removal mismatch")
                src_idx+=1
            elif line.startswith("+"):
                out.append(line[1:])
            elif line.startswith("\\"):
                pass
            else:
                raise RuntimeError("invalid unified diff line")
            i+=1
    out.extend(src[src_idx:])
    return "".join(out)

def apply_overrides(data: bytes) -> bytes:
    current=data
    for ov in M.get("accepted_overrides",[]):
        if sha256(current)!=ov["base_sha256"]: raise RuntimeError(f"override base mismatch: {ov['id']}")
        patch_data=(ROOT/ov["file"]).read_bytes()
        if sha256(patch_data)!=ov["patch_sha256"]: raise RuntimeError(f"override patch identity mismatch: {ov['id']}")
        if ov["format"]=="gzip-base64-unified-diff":
            text=patch_data.decode("utf-8")
            marker="DANTE_GZIP_BASE64_UNIFIED_DIFF_V1\n"
            if not text.startswith(marker): raise RuntimeError(f"override encoding marker mismatch: {ov['id']}")
            patch_text=gzip.decompress(base64.b64decode("".join(text[len(marker):].split()),validate=True)).decode("utf-8")
        elif ov["format"]=="unified-diff":
            patch_text=patch_data.decode("utf-8")
        else:
            raise RuntimeError(f"unsupported override format: {ov['format']}")
        current=apply_unified_diff(current.decode("utf-8"),patch_text).encode("utf-8")
        if sha256(current)!=ov["result_sha256"]: raise RuntimeError(f"override result mismatch: {ov['id']}")
    return current

def build():
    oracle=oracle_text(); osb,ojb=blocks(oracle)
    if len(osb)!=38 or len(ojb)!=20: raise RuntimeError("oracle block count changed; re-baseline modular source")
    styles={}
    for g in M["styles"]:
        for n,c in zip(g["blocks"],module(g,"style",osb,ojb)): styles[n]=c
    out=template(oracle); nested={int(k):v for k,v in M["nested_style_blocks"].items()}
    for n,c in styles.items():
        if n not in nested: out=out.replace(f"__DANTE_A2_STYLE_{n:02d}__",c,1)
    asset=resolve_asset(oracle)
    for g in M["scripts"]:
        for n,c in zip(g["blocks"],module(g,"script",osb,ojb)):
            for sn,meta in nested.items():
                if meta["inside_script_block"]==n:
                    ms=list(STYLE_RE.finditer(c))
                    if len(ms)!=1: raise RuntimeError(f"nested style changed in script {n}")
                    sm=ms[0]; c=c[:sm.start(1)]+styles[sn]+c[sm.end(1):]
            if n==20:
                prefix=M["asset"]["source_prefix"]; hit=c.find(prefix)
                if hit<0: raise RuntimeError("day-ribbon image missing in script 20")
                start=hit+len(prefix); alphabet=set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="); end=start
                while end<len(c) and c[end] in alphabet: end+=1
                c=c[:start]+asset+c[end:]
            out=out.replace(f"__DANTE_A2_SCRIPT_{n:02d}__",c,1)
    baseline=out.encode("utf-8")
    exp=M["oracle"]
    if len(baseline)!=exp["size_bytes"] or sha256(baseline)!=exp["sha256"]:
        raise RuntimeError(f"baseline build mismatch size={len(baseline)} sha256={sha256(baseline)}")
    return apply_overrides(baseline)

def materialize(target):
    # Materialize against the retained baseline. If the target overlaps an accepted
    # override, absorb/remove that override in the same future bounded scope first.
    oracle=oracle_text(); osb,ojb=blocks(oracle); p=(ROOT/target).resolve()
    rel=p.relative_to(ROOT).as_posix()
    if rel==M["template"]:
        p.write_text(derive_template(oracle),encoding="utf-8"); print(f"Materialized {rel}"); return
    for g in M["styles"]:
        if g["file"]==rel:
            p.write_text(M["style_separator"].join(osb[n-1] for n in g["blocks"]),encoding="utf-8"); print(f"Materialized {rel}"); return
    for g in M["scripts"]:
        if g["file"]==rel:
            chunks=[ojb[n-1] for n in g["blocks"]]
            if 20 in g["blocks"]:
                idx=g["blocks"].index(20); c=chunks[idx]; prefix=M["asset"]["source_prefix"]; hit=c.find(prefix); start=hit+len(prefix)
                alphabet=set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="); end=start
                while end<len(c) and c[end] in alphabet: end+=1
                chunks[idx]=c[:start]+M["asset"]["token"]+c[end:]
            p.write_text(M["script_separator"].join(chunks),encoding="utf-8"); print(f"Materialized {rel}"); return
    raise SystemExit(f"unknown module: {target}")

def main():
    p=argparse.ArgumentParser(); p.add_argument("output",nargs="?",default=str(ROOT/"build"/"home.html")); p.add_argument("--materialize")
    a=p.parse_args()
    if a.materialize: materialize(a.materialize); return
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); data=build(); h=sha256(data); exp=M["accepted_output"]
    if len(data)!=exp["size_bytes"] or h!=exp["sha256"]: raise SystemExit(f"accepted build mismatch size={len(data)} sha256={h}")
    out.write_bytes(data); print(f"Built {out}\nsize={len(data)}\nsha256={h}\naccepted_match=PASS")

if __name__=="__main__": main()
