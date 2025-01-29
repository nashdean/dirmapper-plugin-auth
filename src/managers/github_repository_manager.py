import base64
import requests
from typing import Optional, List, Dict
from ..auth.github_auth import GitHubAuthManager
from ..utils.request_utils import make_request_with_retry
from dirmapper_core.models.directory_item import DirectoryItem
from dirmapper_core.models.directory_structure import DirectoryStructure
from dirmapper_core.utils.logger import logger
from .repository_manager import RepositoryManager

class GitHubRepositoryManager(RepositoryManager):
    def __init__(self, auth_manager: GitHubAuthManager):
        self.auth_manager = auth_manager

    def fetch_directory_structure(self, owner: str, repo: str, path: str = "") -> DirectoryStructure:
        directory_structure = DirectoryStructure()
        self._fetch_directory_contents(owner, repo, path, directory_structure, level=0)
        return directory_structure

    def _fetch_directory_contents(self, owner: str, repo: str, path: str, directory_structure: DirectoryStructure, level: int):
        contents = self.get_repository_contents(owner, repo, path)
        if contents is None:
            return

        for item in contents:
            item_path = item['path']
            item_name = item['name']
            item_type = item['type']
            directory_item = DirectoryItem(path=item_path, level=level, name=item_name, metadata={'type': item_type})

            if item_type == 'file':
                file_content = self._get_file_content(owner, repo, item_path)
                if file_content:
                    directory_item.metadata['content'] = file_content
                    directory_item.metadata['content_hash'] = directory_item._hash_content(file_content)

            directory_structure.add_item(directory_item)

            if item_type == 'dir':
                self._fetch_directory_contents(owner, repo, item_path, directory_structure, level + 1)

    def get_repository_contents(self, owner: str, repo: str, path: str = "") -> Optional[List[Dict]]:
        """
        Get the contents of a repository or a specific directory from the GitHub API.

        Args:
            owner (str): The owner of the repository.
            repo (str): The name of the repository.
            path (str): The path to the directory or file within the repository.

        Returns:
            Optional[List[Dict]]: The contents of the repository or directory if the request is successful, None otherwise.
        """
        try:
            url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
            response = make_request_with_retry(url, auth=self.auth_manager)
            self.auth_manager._check_rate_limit(response)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get repository contents: {response.status_code} {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting repository contents: {str(e)}")
            return None

    def _get_file_content(self, owner: str, repo: str, path: str) -> Optional[str]:
        """
        Get the content of a file from the GitHub API.

        Args:
            owner (str): The owner of the repository.
            repo (str): The name of the repository.
            path (str): The path to the file within the repository.

        Returns:
            Optional[str]: The content of the file if the request is successful, None otherwise.
        """
        try:
            url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
            response = make_request_with_retry(url, auth=self.auth_manager)
            self.auth_manager._check_rate_limit(response)
            if response.status_code == 200:
                content = response.json().get('content')
                if content:
                    return base64.b64decode(content).decode('utf-8')
                else:
                    logger.error("File content is empty.")
                    return None
            else:
                logger.error(f"Failed to get file content: {response.status_code} {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting file content: {str(e)}")
            return None
