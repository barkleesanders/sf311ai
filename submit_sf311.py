#!/usr/bin/env python3
"""Automate SF311 form submissions using Playwright."""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import logging
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

BASE_URL = "https://sanfrancisco.form.us.empro.verintcloudservices.com/form/auto"
CSV_FILE = "submissions.csv"
ERROR_LOG = "errors.log"


def load_config(path: str) -> Dict[str, Dict[str, Any]]:
    """Load JSON configuration mapping form slugs to field values."""
    with open(path, "r") as f:
        return json.load(f)


async def navigate_with_retries(page: Page, url: str, max_retries: int = 3) -> None:
    """Navigate to a URL with retry logic for timeouts."""
    for attempt in range(max_retries):
        try:
            await page.goto(url, timeout=30000)
            return
        except PlaywrightTimeoutError:
            if attempt == max_retries - 1:
                raise


async def fill_required_fields(page, data: Dict[str, Any], slug: str) -> None:
    """Fill all required form fields with provided data."""
    required = page.locator("input[required], select[required], textarea[required]")
    count = await required.count()
    for i in range(count):
        el = required.nth(i)
        name = await el.get_attribute("name")
        if not name:
            continue
        if name not in data:
            raise ValueError(f"Missing value for required field '{name}' on {slug}")
        value = data[name]
        input_type = (await el.get_attribute("type")) or "text"
        tag = await el.evaluate("e => e.tagName")
        if input_type in {"checkbox", "radio"}:
            await page.check(f"input[name='{name}'][value='{value}']")
        elif input_type == "file":
            await el.set_input_files(value)
        elif tag == "SELECT":
            await el.select_option(value)
        else:
            await el.fill(str(value))
            # handle address autocomplete if present
            await page.wait_for_timeout(1000)
            try:
                await page.keyboard.press("ArrowDown")
                await page.keyboard.press("Enter")
            except Exception:
                pass


async def submit_form(page, slug: str, data: Dict[str, Any]) -> str:
    """Submit a single SF311 form and return confirmation text."""
    url = f"{BASE_URL}/{slug}"
    await navigate_with_retries(page, url)
    await fill_required_fields(page, data, slug)
    await page.click("input[type='submit'], button[type='submit']")
    await page.wait_for_load_state("networkidle")
    body = await page.text_content("body")
    return body.strip() if body else ""


async def process_forms(config: Dict[str, Dict[str, Any]], show: bool) -> None:
    """Process all forms sequentially."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=not show)
        page = await browser.new_page()
        csv_file = Path(CSV_FILE)
        csv_writer = csv.writer(csv_file.open("a", newline=""))
        for slug, data in config.items():
            try:
                confirmation = await submit_form(page, slug, data)
                csv_writer.writerow([datetime.utcnow().isoformat(), slug, confirmation])
                await page.wait_for_timeout(random.randint(2000, 5000))
            except Exception:
                logging.exception("Failed to submit %s", slug)
        await browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit SF311 forms")
    parser.add_argument("--config", default="config.json", help="Path to config JSON")
    parser.add_argument(
        "--show", action="store_true", help="Show browser for debugging"
    )
    args = parser.parse_args()

    load_dotenv()
    logging.basicConfig(filename=ERROR_LOG, level=logging.ERROR)

    config = load_config(args.config)
    asyncio.run(process_forms(config, args.show))


if __name__ == "__main__":
    main()
