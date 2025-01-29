from .provider import Provider
from ..auth.github_auth import GitHubAuthManager
from ..managers.github_api_manager import GitHubAPIManager
from ..utils.request_utils import make_request_with_retry
import base64
from typing import Optional, List, Dict
from dirmapper_core.models.directory_item import DirectoryItem
from dirmapper_core.models.directory_structure import DirectoryStructure
from dirmapper_core.utils.logger import logger

class GitHubProvider(Provider):
    def __init__(self, oauth_token: str):
        self.auth_manager = GitHubAuthManager(oauth_token)
        self.api_manager = GitHubAPIManager(self.auth_manager)

    def authenticate(self):
        return self.auth_manager.validate_token()

    def fetch_directory_structure(self, repo_url: str) -> dict:
        owner, repo = self._parse_repo_url(repo_url)
        directory_structure = self._fetch_directory_structure(owner, repo)
        return directory_structure.to_dict()

    def validate_token(self) -> bool:
        return self.auth_manager.validate_token()

    def get_user_details(self) -> Optional[dict]:
        return self.api_manager.get_user_details()

    def get_repository_details(self, owner: str, repo: str) -> Optional[dict]:
        return self.api_manager.get_repository_details(owner, repo)

    def _parse_repo_url(self, repo_url: str) -> (str, str):
        parts = repo_url.rstrip('/').split('/')
        owner = parts[-2]
        repo = parts[-1]
        return owner, repo

    def _fetch_directory_structure(self, owner: str, repo: str, path: str = "") -> DirectoryStructure:
        directory_structure = DirectoryStructure()
        self._fetch_directory_contents(owner, repo, path, directory_structure, level=0)
        return directory_structure

    def _fetch_directory_contents(self, owner: str, repo: str, path: str, directory_structure: DirectoryStructure, level: int):
        contents = self._get_repository_contents(owner, repo, path)
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

    def _get_repository_contents(self, owner: str, repo: str, path: str = "") -> Optional[List[Dict]]:
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
