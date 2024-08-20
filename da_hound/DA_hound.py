import time
from datetime import datetime

import pyautogui
from playwright.sync_api import sync_playwright, Page, Playwright, Locator


def find_da_page(p: Playwright) -> Page:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    pages = browser.contexts[0].pages
    for page in pages:
        if "dataannotation" in page.url:
            return page
    raise FileNotFoundError()


def show_warning(message: str):
    pyautogui.alert(text=message, title="Warning", button="OK")


def pick_task(projects_table: Locator, page: Page) -> bool:
    original_url = page.url
    table_cell = projects_table.get_by_text("$4")
    table_row = table_cell.locator('..')
    project_cell = table_row.locator("td > a").all()[0]
    with page.expect_navigation(timeout=60000):
        project_cell.click()
    return page.url != original_url

#TODO se tiver mais de um projeto dando $40 e não conseguir pegar um, pegar o outro em seguida


def hound_watch(page: Page, reserve_task: bool):
    original_url = page.url
    table_selector = "div.tw-relative > div > table > tbody"
    retries = 0
    print("Starting the hunt.")
    while True:
        tables = page.locator(f"{table_selector}")
        try:
            projects_table = tables.all()[1]
        except Exception as e:
            retries += 1
            if retries > 1:
                raise e
            time.sleep(15)
            continue
        retries = 0
        table_content = projects_table.inner_html()
        if "$4" in table_content:
            if reserve_task:
                if not pick_task(projects_table, page):
                    time.sleep(5)
                    continue
            show_warning("'$40' found in the table!")
            break  # Exit the loop if found

        print("'$40' not found, waiting and refreshing...", datetime.now())
        time.sleep(60)  # Wait for 1 minute
        page.reload()

        # Check if the URL has changed after refresh
        if page.url != original_url:
            show_warning("URL changed after refresh. Stopping.")
            break


def main(reserve_task: bool = True):
    with sync_playwright() as p:
        page = find_da_page(p)
        hound_watch(page, reserve_task)


if __name__ == "__main__":
    main()
