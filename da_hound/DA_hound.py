import time
from rich import print
from datetime import datetime

import pyautogui
from playwright.sync_api import sync_playwright, Page, Playwright, Locator


def find_da_page(p: Playwright) -> Page:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    pages = browser.contexts[0].pages
    for page in pages:
        if "dataannotation" in page.url and "projects" in page.url:
            return page
    raise FileNotFoundError()


def show_warning(message: str):
    pyautogui.alert(text=message, title="Warning", button="OK")


def pick_task(projects_table: Locator, page: Page, project_name: str) -> bool:
    original_url = page.url
    table_cell = projects_table.get_by_text(project_name)
    project_cell = table_cell.locator('..')
    with page.expect_navigation(timeout=60000):
        project_cell.click()
    return page.url != original_url


def map_table(projects_table: Locator, priorities: tuple) -> dict:
    headers = [th.text_content() for th in projects_table.locator('th > div > div:nth-child(1)').all()]
    data, max_priority = {}, len(priorities) + 1
    for row in projects_table.locator('tr').all():
        cols = row.locator('td').all()
        if not cols:
            continue
        row_data = {headers[i]: cols[i].text_content() for i in range(len(cols))}
        name, priority = row_data["Name"], 1
        for i in range(len(priorities)):
            if priorities[i] in name:
                priority = max_priority - i
                break
        row_data["Priority"] = priority
        data[name] = row_data
    return data


def good_project(project_fields: dict) -> bool:
    if "$4" in project_fields["Pay"]:
        return True
    if "$3" in project_fields["Pay"]:
        return True
    if "Cod" in project_fields["Name"]:
        return True
    return False


def search_tasks(projects: dict, previous_projects: dict) -> str:
    if projects == previous_projects:
        return ""
    active_projects, previous_projects = set(projects.keys()), set(previous_projects.keys())
    if new_projects := (active_projects - previous_projects):
        print("New projects found:", {
            project_name: projects[project_name]
            for project_name in new_projects
        })
    if old_projects := (previous_projects - active_projects):
        print("Old projects gone:", {
            project_name: projects[project_name]
            for project_name in old_projects
        })

    selected_priority, selected_project = 0, ""
    for project, fields in projects.items():
        if not good_project(fields):
            continue
        priority = fields["Priority"]
        if priority > selected_priority:
            selected_priority, selected_project = priority, project
    return selected_project


def hound_watch(page: Page, reserve_task: bool, priorities: tuple):
    previous_projects = {}
    original_url = page.url
    table_selector = "div.tw-relative > div > table"
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
        projects = map_table(projects_table, priorities)
        if project_name := search_tasks(projects, previous_projects):
            previous_projects = projects.copy()
            if reserve_task:
                if not pick_task(projects_table, page, project_name):
                    time.sleep(5)
                    continue
            show_warning(f"Good project {project_name} found in the table!")
            break  # Exit the loop if found
        previous_projects = projects.copy()
        print("No good project found, waiting and refreshing...", datetime.now())
        time.sleep(60)
        page.reload()

        # Check if the URL has changed after refresh
        if page.url != original_url:
            show_warning("URL changed after refresh. Stopping.")
            break


def main(priorities: tuple, reserve_task: bool = True):
    with sync_playwright() as p:
        page = find_da_page(p)
        hound_watch(page, reserve_task, priorities)


if __name__ == "__main__":
    priorities = "Achilles",
    main(priorities)
