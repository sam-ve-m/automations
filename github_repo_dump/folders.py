import os


class Console:

    @staticmethod
    def _read_git_config_file(folder: str) -> str:
        git_folder_path = os.path.join(folder, ".git")
        if not os.path.exists(git_folder_path):
            return ""
        config_file_path = os.path.join(git_folder_path, "config")
        if not os.path.exists(config_file_path):
            return ""
        return config_file_path

    @classmethod
    def delete_git_repo(cls, folder: str) -> str:
        config_file_path = cls._read_git_config_file(folder)
        if not config_file_path:
            return ""
        with open(config_file_path, 'r') as file:
            config_file = file.read()

        config_file_sections = config_file.split("[")
        final_config_file_sections, removed_config_file_sections = [], [""]
        for section in config_file_sections:
            (final_config_file_sections.append(section)
             if 'bitbucket' not in section else
             removed_config_file_sections.append(section))

        final_config_file = "[".join(final_config_file_sections)
        with open(config_file_path, 'w') as file:
            file.write(final_config_file)
        removed_config_file = "[".join(removed_config_file_sections)
        return removed_config_file

    @staticmethod
    def push_git_repository_to_github(folder: str ,repo_name: str):
        os.system(f'gh repo create {repo_name} --source="{folder}" --remote=upstream --public --push')
        os.system(f'git -C "{folder}" push --all')

    @classmethod
    def init_github_repository(cls, folder: str, repo_name: str) -> str:
        if removed_section := cls.delete_git_repo(folder):
            cls.push_git_repository_to_github(folder, repo_name)
            return removed_section
