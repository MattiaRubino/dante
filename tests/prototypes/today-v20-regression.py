"""Regression suite for the standalone LifeOS Today v20 prototype.

Usage:
    python today-v20-regression.py /path/to/LifeOS_Home_Oggi_v20_canvas.html
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
    page.wait_for_timeout(400)
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
    prototype = Path(sys.argv[1] if len(sys.argv) > 1 else "LifeOS_Home_Oggi_v20_canvas.html")
    html = prototype.read_text(encoding="utf-8")

    with sync_playwright() as playwright:
        browser = launch_browser(playwright)

        page, errors = load_page(browser, html)
        assert page.title().endswith("v20")
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

        ruler = page.locator(".tl-ruler").first.bounding_box()
        eye = page.locator(".tl-groupbar__reset").bounding_box()
        first_group = page.locator(".tl-groupbar__chip").first.bounding_box()
        assert ruler and eye and first_group
        ruler_right = ruler["x"] + ruler["width"]
        assert eye["x"] >= ruler_right - 1, (ruler, eye)
        assert first_group["x"] > eye["x"] + eye["width"], (eye, first_group)

        controls_before = page.locator(".tl-view-controls").bounding_box()
        assert controls_before and controls_before["width"] >= 60 and controls_before["height"] >= 34
        page.eval_on_selector("#tl-grid", "el => el.scrollTop += 500")
        page.wait_for_timeout(80)
        controls_after = page.locator(".tl-view-controls").bounding_box()
        assert controls_after
        assert abs(controls_after["y"] - controls_before["y"]) < 1.5, (controls_before, controls_after)

        margins = page.evaluate("window.__lifeosDebug.marginGaps()")
        today_margins = [m for m in margins if m["from"] <= 18 * 60]
        assert {"gap": 15, "from": 11 * 60 + 15, "to": 11 * 60 + 30} in today_margins
        assert not any(m["from"] == 15 * 60 and m["to"] == 15 * 60 + 15 for m in today_margins), today_margins
        assert {"gap": 0, "from": 15 * 60 + 15, "to": 15 * 60 + 15} in today_margins

        page.locator("#tl-options-toggle").click()
        assert page.locator("#tl-view-popover").is_visible()
        day_height_before = page.eval_on_selector(
            '.day-section[data-date="2026-08-04"] .tl-canvas',
            "el => parseFloat(getComputedStyle(el).height)",
        )
        visible_before = page.locator(".tl-margin:visible").count()
        assert visible_before > 0
        page.locator('[data-view-pref="margins"]').click()
        assert page.locator(".tl-margin:visible").count() == 0
        day_height_after = page.eval_on_selector(
            '.day-section[data-date="2026-08-04"] .tl-canvas',
            "el => parseFloat(getComputedStyle(el).height)",
        )
        assert abs(day_height_after - day_height_before) < 0.5
        page.locator("#tl-view-reset").click()
        assert page.locator(".tl-margin:visible").count() == visible_before
        page.locator("#tl-options-toggle").click()
        assert not page.locator("#tl-view-popover").is_visible()

        title_action = page.locator('.ev-block[data-ev-block="12"] .ev-block__title-action')
        title = title_action.locator(".ev-block__title")
        body = page.locator('.ev-block[data-ev-block="12"] .ev-block__top')
        title_action.scroll_into_view_if_needed()
        body_box = body.bounding_box()
        assert body_box
        body.hover(position={"x": body_box["width"] - 3, "y": body_box["height"] - 3})
        body_color = title.evaluate("el => getComputedStyle(el).color")
        title_action.hover()
        page.wait_for_timeout(160)
        title_color = title.evaluate("el => getComputedStyle(el).color")
        violet = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--violet-text').trim()")
        violet_rgb = page.evaluate(
            """value => {const x=document.createElement('span');x.style.color=value;document.body.appendChild(x);const c=getComputedStyle(x).color;x.remove();return c;}""",
            violet,
        )
        assert body_color != violet_rgb, (body_color, violet_rgb)
        assert title_color == violet_rgb, (title_color, violet_rgb)

        page.locator('.js-filter-chip[data-cat="focus"]').click()
        assert page.locator(".tl-groupbar__reset.is-active").count() == 1
        page.locator(".tl-groupbar__reset").click()
        assert page.locator(".tl-groupbar__reset.is-active").count() == 0

        assert page.locator("#tl-toggle").get_attribute("data-tooltip") == "Separa per gruppi"
        page.locator("#tl-toggle").click()
        page.wait_for_timeout(420)
        assert page.locator("#tl-toggle").get_attribute("aria-pressed") == "true"
        assert page.locator("#tl-toggle").get_attribute("data-tooltip") == "Riunisci nella timeline"
        progress = page.eval_on_selector(
            "#content-grid", 'el => getComputedStyle(el).getPropertyValue("--expand-progress").trim()'
        )
        assert progress == "1.000"
        assert not errors
        page.close()

        page, errors = load_page(browser, html)
        reminder = page.locator('.ev-block[data-ev-block="12"]')
        time_action = reminder.locator('.js-time-edit')
        time_action.scroll_into_view_if_needed()
        initial_top = reminder.bounding_box()["y"]
        time_action.click()
        assert reminder.locator('.ev-time-editor').count() == 1
        assert page.locator('#modal-backdrop.is-open').count() == 0
        assert reminder.locator('.is-context-selected').count() == 0
        start_input = reminder.locator('.js-time-start')
        end_input = reminder.locator('.js-time-end')
        assert start_input.input_value() == "14:45"
        assert end_input.input_value() == "15:00"
        start_input.fill("1447")
        assert end_input.input_value() == "15:02"
        reminder.locator('.js-time-save').click()
        page.wait_for_timeout(260)
        assert reminder.locator('.js-time-edit').inner_text() == "14:47–15:02"
        moved_top = reminder.bounding_box()["y"]
        assert abs(moved_top - initial_top) > 1, (initial_top, moved_top)
        assert page.locator('#move-toast-text').inner_text() == "Orario aggiornato: 14:47–15:02"
        page.locator('#move-toast-undo').click()
        page.wait_for_timeout(180)
        assert reminder.locator('.js-time-edit').inner_text() == "14:45–15:00"

        reminder.locator('.js-time-edit').click()
        reminder.locator('.js-time-start').fill("25:00")
        reminder.locator('.js-time-save').click()
        assert reminder.locator('.ev-time-editor.is-invalid').count() == 1
        assert reminder.locator('.ev-time-editor__error').is_visible()
        assert page.evaluate('window.__lifeosDebug.activeTimeEdit()') is not None
        page.keyboard.press("Escape")
        assert reminder.locator('.ev-time-editor').count() == 0
        assert reminder.locator('.js-time-edit').inner_text() == "14:45–15:00"

        reminder.locator('.js-time-edit').click()
        reminder.locator('.js-time-start').fill("14:47")
        reminder.locator('.js-time-end').fill("15:19")
        reminder.locator('.js-time-end').press("Enter")
        page.wait_for_timeout(240)
        assert reminder.locator('.js-time-edit').inner_text() == "14:47–15:19"
        assert not errors
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
        assert parse_start(moved_time) % 5 == 0
        assert page.locator('.ev-block[data-ev-block="2"] .ev-block__meta').inner_text() == original_cat
        assert not errors
        page.close()

        browser.close()

    print("Today v20 regression suite: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
