"""Regression suite for the standalone LifeOS Today v18 prototype.

Usage:
    python today-v18-regression.py /path/to/LifeOS_Home_Oggi_v18_canvas.html
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def launch_browser(playwright):
    executable = shutil.which("chromium") or shutil.which("google-chrome")
    kwargs = {"headless": True}
    if executable:
        kwargs.update(executable_path=executable, args=["--no-sandbox"])
    return playwright.chromium.launch(**kwargs)


def load_page(browser, html: str):
    page = browser.new_page(viewport={"width": 1575, "height": 945})
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(f"pageerror: {error}"))
    page.on("console", lambda msg: errors.append(f"console: {msg.text}") if msg.type == "error" else None)
    page.set_content(html, wait_until="load")
    page.wait_for_timeout(350)
    return page, errors


def rectangles_intersect(a: dict, b: dict) -> bool:
    return (
        min(a["right"], b["right"]) - max(a["left"], b["left"]) > 1
        and min(a["bottom"], b["bottom"]) - max(a["top"], b["top"]) > 1
    )


def parse_start(text: str) -> int:
    match = re.match(r"(\d{2}):(\d{2})", text)
    assert match, text
    return int(match.group(1)) * 60 + int(match.group(2))


def main() -> int:
    prototype = Path(sys.argv[1] if len(sys.argv) > 1 else "LifeOS_Home_Oggi_v18_canvas.html")
    html = prototype.read_text(encoding="utf-8")

    with sync_playwright() as playwright:
        browser = launch_browser(playwright)

        page, errors = load_page(browser, html)
        assert page.title().endswith("v18")
        assert page.locator(".ev-block").count() >= 12
        assert not errors
        assert page.locator("#tl-day-title").inner_text().startswith("Oggi")
        assert page.eval_on_selector("#tl-grid", "el => el.scrollTop") > 0

        hours = page.locator('.day-section[data-date="2026-08-04"] .tl-hour:not(.tl-hour--minor) .tl-hour__label').all_inner_texts()
        assert hours[0] == "00:00", hours[:3]
        assert hours[-1] == "24:00", hours[-3:]
        assert all(f"{hour:02d}:00" in hours for hour in range(24))

        day_height = page.eval_on_selector(
            '.day-section[data-date="2026-08-04"] .tl-canvas',
            "el => parseFloat(getComputedStyle(el).height)",
        )
        assert day_height > 2100, day_height

        reminder = page.locator('.ev-block[data-ev-block="12"]')
        reminder_box = reminder.bounding_box()
        assert reminder_box and reminder_box["width"] >= 160 and reminder_box["height"] >= 68, reminder_box
        assert reminder.locator(".ev-block__title").is_visible()
        assert reminder.locator(".ev-block__time").is_visible()
        assert reminder.locator(".ev-block__time").inner_text() == "14:45–15:00"
        title_metrics = reminder.locator(".ev-block__title").evaluate(
            "el => ({clientHeight: el.clientHeight, scrollHeight: el.scrollHeight})"
        )
        assert title_metrics["scrollHeight"] <= title_metrics["clientHeight"] + 1, title_metrics

        rects = page.evaluate(
            """() => [...document.querySelector('.day-section[data-date="2026-08-04"]').querySelectorAll('.ev-block')]
            .map(el => ({id: el.dataset.evBlock, rect: el.getBoundingClientRect().toJSON()}))"""
        )
        collisions: list[tuple[str, str]] = []
        for index, item in enumerate(rects):
            for other in rects[index + 1 :]:
                if rectangles_intersect(item["rect"], other["rect"]):
                    collisions.append((item["id"], other["id"]))
        assert not collisions, collisions

        page.locator('.ev-block[data-ev-block="1"] .js-open-modal').click()
        assert page.locator("#modal-backdrop.is-open").count() == 1
        page.locator("#modal-close").click()
        page.locator('.ev-block[data-ev-block="1"] .ev-block__drag-zone').click()
        assert page.locator('.ev-block[data-ev-block="1"].is-context-selected').count() == 1
        page.locator('.ev-block[data-ev-block="1"] .ev-block__drag-zone').click()
        assert page.locator('.ev-block[data-ev-block="1"].is-context-selected').count() == 0

        initial_height = page.eval_on_selector(
            '.day-section[data-date="2026-08-04"] .tl-canvas',
            "el => parseFloat(getComputedStyle(el).height)",
        )
        page.locator('.js-filter-chip[data-cat="focus"]').click()
        page.wait_for_timeout(100)
        filtered_height = page.eval_on_selector(
            '.day-section[data-date="2026-08-04"] .tl-canvas',
            "el => parseFloat(getComputedStyle(el).height)",
        )
        assert abs(filtered_height - initial_height) < 0.5
        page.locator("#tl-toggle").click()
        page.wait_for_timeout(420)
        progress = page.eval_on_selector(
            "#content-grid",
            'el => getComputedStyle(el).getPropertyValue("--expand-progress").trim()',
        )
        assert progress == "1.000"
        page.close()

        page, errors = load_page(browser, html)
        grid_box = page.locator("#tl-grid").bounding_box()
        assert grid_box
        centre_y = grid_box["y"] + grid_box["height"] / 2
        before = page.evaluate("y => window.__lifeosDebug.zoomAnchorAt(y)", centre_y)
        page.locator('.js-zoom[data-dir="in"]').click()
        page.wait_for_timeout(100)
        after = page.evaluate("y => window.__lifeosDebug.zoomAnchorAt(y)", centre_y)
        assert before["dateKey"] == after["dateKey"]
        assert abs(before["minute"] - after["minute"]) < 0.5, (before, after)

        pointer_y = grid_box["y"] + grid_box["height"] * 0.68
        pointer_x = grid_box["x"] + grid_box["width"] * 0.55
        before = page.evaluate("y => window.__lifeosDebug.zoomAnchorAt(y)", pointer_y)
        page.mouse.move(pointer_x, pointer_y)
        page.keyboard.down("Control")
        page.mouse.wheel(0, -120)
        page.keyboard.up("Control")
        page.wait_for_timeout(100)
        after = page.evaluate("y => window.__lifeosDebug.zoomAnchorAt(y)", pointer_y)
        assert before["dateKey"] == after["dateKey"]
        assert abs(before["minute"] - after["minute"]) < 0.75, (before, after)
        assert not errors
        page.close()

        page, errors = load_page(browser, html)
        source = page.locator('.ev-block[data-ev-block="2"] .ev-block__drag-zone')
        source.scroll_into_view_if_needed()
        box = source.bounding_box()
        assert box
        x, y = box["x"] + box["width"] / 2, box["y"] + max(2, box["height"] / 2)
        original_cat = page.locator('.ev-block[data-ev-block="2"] .ev-block__meta').inner_text()
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x + 40, y + 31, steps=10)
        assert page.locator(".ev-drag-overlay").count() == 1
        page.mouse.up()
        page.wait_for_timeout(250)
        moved_time = page.locator('.ev-block[data-ev-block="2"] .ev-block__time').inner_text()
        assert parse_start(moved_time) % 5 == 0, moved_time
        assert page.locator('.ev-block[data-ev-block="2"] .ev-block__meta').inner_text() == original_cat
        assert not errors
        page.close()

        page, errors = load_page(browser, html)
        for _ in range(5):
            page.locator('.js-zoom[data-dir="in"]').click()
            page.wait_for_timeout(60)
        assert page.locator("#tl-zoom-value").inner_text() == "190%"
        assert page.evaluate('() => window.__lifeosDebug.dragSnap()') == 1
        source = page.locator('.ev-block[data-ev-block="2"] .ev-block__drag-zone')
        source.scroll_into_view_if_needed()
        box = source.bounding_box()
        assert box
        x, y = box["x"] + box["width"] / 2, box["y"] + max(2, box["height"] / 2)
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x, y + 27, steps=10)
        page.mouse.up()
        page.wait_for_timeout(250)
        precise_time = page.locator('.ev-block[data-ev-block="2"] .ev-block__time').inner_text()
        assert parse_start(precise_time) % 1 == 0, precise_time
        assert not errors
        page.close()

        browser.close()

    print("Today v18 regression suite: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
