import os
import json
import asyncio
from folders import Console

main_folder = "C:\\Users", "samue", "OneDrive - UBC", "Projects", "Profissional", "LionX"
name_clean_list = ".lionx.com.br", "liga-", "liga", "ouroinvest.", "caf."

main_folder_path = os.path.join(*main_folder)
folders = os.listdir(main_folder_path)


async def create_github_repo(folder: str):
    repo_name = folder
    for word in name_clean_list:
        repo_name = repo_name.replace(word, "")

    full_folder_path = os.path.join(main_folder_path, folder)

    if removed_git_config_file_section := Console.init_github_repository(full_folder_path, repo_name):
        return folder, removed_git_config_file_section


def save_backup(backup: dict):
    if os.path.exists("backup.json"):
        with open("backup.json", "r") as file:
            old_backup = json.loads(file.read())
        for key, value in old_backup.items():
            backup[key] = backup.get(key, []) + value
    with open("backup.json", "w") as file:
        json.dump(backup, file)


async def create_repos():
    tasks = (
        asyncio.create_task(create_github_repo(folder))
        for folder in folders
    )
    removed_sections = filter(bool, await asyncio.gather(*tasks))
    if removed_sections:
        save_backup({key: [value] for key, value in removed_sections})


asyncio.run(create_repos())

