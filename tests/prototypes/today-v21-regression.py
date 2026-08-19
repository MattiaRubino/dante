"""Regression suite for the standalone LifeOS Today v21 prototype.

Usage:
    python today-v21-regression.py /path/to/LifeOS_Home_Oggi_v21_canvas.html
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
    page.wait_for_timeout(450)
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
    prototype = Path(sys.argv[1] if len(sys.argv) > 1 else "LifeOS_Home_Oggi_v21_canvas.html")
    html = prototype.read_text(encoding="utf-8")

    with sync_playwright() as playwright:
        browser = launch_browser(playwright)

        # Core rendering, 24h timeline, layout and v19 guarantees.
        page, errors = load_page(browser, html)
        assert page.title().endswith("v21")
        assert page.locator(".ev-block").count() >= 12
        assert not errors
        assert page.locator("#tl-day-title").inner_text().startswith("Oggi")
        assert page.eval_on_selector("#tl-grid", "el => el.scrollTop") > 0

        hours = page.locator('.day-section[data-date="2026-08-04"] .tl-hour:not(.tl-hour--minor) .tl-hour__label').all_inner_texts()
        assert hours[0] == "00:00"
        assert hours[-1] == "24:00"
        assert all(f"{hour:02d}:00" in hours for hour in range(24))

        reminder = page.locator('.ev-block[data-ev-block="12"]')
        reminder_box = reminder.bounding_box()
        assert reminder_box and reminder_box["width"] >= 160 and reminder_box["height"] >= 68, reminder_box
        assert reminder.locator(".ev-block__time").inner_text() == "14:45–15:00"

        # Regression from v20 screenshot: time must always occupy its own row below the title.
        for event_id in (4, 7, 12):
            block = page.locator(f'.ev-block[data-ev-block="{event_id}"]')
            block.scroll_into_view_if_needed()
            title_box = block.locator(".ev-block__title-action").bounding_box()
            time_box = block.locator(".ev-block__time-action").bounding_box()
            assert title_box and time_box
            assert time_box["y"] >= title_box["y"] + title_box["height"] - 1, (event_id, title_box, time_box)

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

        # V19 controls and cluster margins remain intact.
        ruler = page.locator(".tl-ruler").first.bounding_box()
        eye = page.locator(".tl-groupbar__reset").bounding_box()
        first_group = page.locator(".tl-groupbar__chip").first.bounding_box()
        assert ruler and eye and first_group
        assert eye["x"] >= ruler["x"] + ruler["width"] - 1
        assert first_group["x"] > eye["x"] + eye["width"]
        margins = page.evaluate("window.__lifeosDebug.marginGaps()")
        today_margins = [m for m in margins if m["from"] <= 18 * 60]
        assert {"gap": 0, "from": 15 * 60 + 15, "to": 15 * 60 + 15} in today_margins
        assert not errors
        page.close()

        # V21 time picker: portal popover, no card reflow, segmented spin controls.
        page, errors = load_page(browser, html)
        reminder = page.locator('.ev-block[data-ev-block="12"]')
        time_action = reminder.locator(".js-time-edit")
        time_action.scroll_into_view_if_needed()
        page.wait_for_timeout(100)
        card_before = reminder.bounding_box()
        title_before = reminder.locator(".ev-block__title-action").bounding_box()
        time_before = time_action.bounding_box()
        assert card_before and title_before and time_before

        time_action.click()
        page.wait_for_timeout(160)
        popover = page.locator(".ev-time-popover")
        assert popover.count() == 1 and popover.is_visible()
        assert popover.evaluate("el => el.parentElement === document.body")
        assert time_action.get_attribute("aria-expanded") == "true"
        assert page.locator("#modal-backdrop.is-open").count() == 0
        card_after = reminder.bounding_box()
        assert card_after
        assert abs(card_after["width"] - card_before["width"]) < 0.5
        assert abs(card_after["height"] - card_before["height"]) < 0.5
        assert abs(card_after["x"] - card_before["x"]) < 0.5
        assert abs(card_after["y"] - card_before["y"]) < 0.5

        start_field = popover.locator('[data-time-field="start"]')
        end_field = popover.locator('[data-time-field="end"]')
        start_hour = start_field.locator(".js-time-hour")
        start_minute = start_field.locator(".js-time-minute")
        end_hour = end_field.locator(".js-time-hour")
        end_minute = end_field.locator(".js-time-minute")
        assert start_hour.input_value() == "14"
        assert start_minute.input_value() == "45"
        assert end_hour.input_value() == "15"
        assert end_minute.input_value() == "00"
        assert popover.locator(".ev-time-popover__duration").inner_text() in {"15 min", "15m"}

        # Arrow controls appear for the active field and modify the selected segment.
        start_minute.focus()
        page.wait_for_timeout(60)
        opacity = start_field.locator(".ev-time-spin__steps").evaluate("el => getComputedStyle(el).opacity")
        assert float(opacity) > 0.9
        start_field.locator('.js-time-step[data-dir="1"]').click()
        assert start_minute.input_value() == "50"
        assert end_hour.input_value() == "15" and end_minute.input_value() == "05"
        assert popover.locator(".ev-time-popover__duration").inner_text() in {"15 min", "15m"}

        # Keyboard arrows and exact typing coexist.
        start_minute.press("ArrowDown")
        assert start_minute.input_value() == "45"
        start_minute.fill("47")
        assert end_hour.input_value() == "15" and end_minute.input_value() == "02"
        popover.locator(".js-time-save").click()
        page.wait_for_timeout(280)
        assert page.locator(".ev-time-popover").count() == 0
        assert reminder.locator(".js-time-edit").inner_text() == "14:47–15:02"
        assert reminder.locator(".js-time-edit").get_attribute("aria-expanded") == "false"
        moved_top = reminder.bounding_box()["y"]
        assert abs(moved_top - card_before["y"]) > 1
        assert page.locator("#move-toast-text").inner_text() == "Orario aggiornato: 14:47–15:02"

        # Undo restores both values.
        page.locator("#move-toast-undo").click()
        page.wait_for_timeout(180)
        assert reminder.locator(".js-time-edit").inner_text() == "14:45–15:00"

        # Invalid values remain in the popover and do not move the event.
        reminder.locator(".js-time-edit").click()
        popover = page.locator(".ev-time-popover")
        popover.locator('[data-time-field="start"] .js-time-hour').fill("25")
        popover.locator(".js-time-save").click()
        assert popover.locator(".ev-time-popover__error").is_visible()
        assert popover.count() == 1
        assert page.evaluate("window.__lifeosDebug.activeTimeEdit()") is not None
        page.keyboard.press("Escape")
        assert page.locator(".ev-time-popover").count() == 0
        assert reminder.locator(".js-time-edit").inner_text() == "14:45–15:00"

        # Manual end editing changes duration and Enter confirms exact minutes.
        reminder.locator(".js-time-edit").click()
        popover = page.locator(".ev-time-popover")
        popover.locator('[data-time-field="start"] .js-time-minute').fill("47")
        popover.locator('[data-time-field="end"] .js-time-minute').fill("19")
        assert popover.locator(".ev-time-popover__duration").inner_text() in {"32 min", "32m"}
        popover.locator('[data-time-field="end"] .js-time-minute').press("Enter")
        page.wait_for_timeout(240)
        assert reminder.locator(".js-time-edit").inner_text() == "14:47–15:19"
        assert not errors
        page.close()

        # Smart positioning stays inside the visible timeline viewport.
        page, errors = load_page(browser, html)
        target = page.locator('.ev-block[data-ev-block="9"] .js-time-edit')
        target.scroll_into_view_if_needed()
        page.wait_for_timeout(80)
        target.click()
        page.wait_for_timeout(140)
        pop_box = page.locator(".ev-time-popover").bounding_box()
        grid_box = page.locator("#tl-grid").bounding_box()
        assert pop_box and grid_box
        assert pop_box["x"] >= grid_box["x"] - 1
        assert pop_box["x"] + pop_box["width"] <= grid_box["x"] + grid_box["width"] + 1
        assert pop_box["y"] >= grid_box["y"] - 1
        assert pop_box["y"] + pop_box["height"] <= grid_box["y"] + grid_box["height"] + 1
        assert page.locator(".ev-time-popover").get_attribute("data-placement") in {"top", "bottom"}
        page.keyboard.press("Escape")
        assert not errors
        page.close()

        # V18 zoom regression remains protected.
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
        assert not errors
        page.close()

        # Drag still snaps to five minutes and preserves category.
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
        assert parse_start(moved_time) % 5 == 0
        assert page.locator('.ev-block[data-ev-block="2"] .ev-block__meta').inner_text() == original_cat
        assert not errors
        page.close()

        browser.close()

    print("Today v21 regression suite: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
