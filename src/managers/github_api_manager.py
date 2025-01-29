import requests
from typing import Optional
from ..auth.github_auth import GitHubAuthManager
from dirmapper_core.utils.logger import logger
from ..utils.request_utils import make_request_with_retry

class GitHubAPIManager:
    """
    GitHubAPIManager handles fetching user details from the GitHub API.
    """
    def __init__(self, auth_manager: GitHubAuthManager):
        """
        Initialize the GitHubAPIManager with an instance of GitHubAuthManager.

        Args:
            auth_manager (GitHubAuthManager): An instance of GitHubAuthManager.
        """
        self.auth_manager = auth_manager

    def get_user_details(self) -> Optional[dict]:
        """
        Get the authenticated user's details from the GitHub API.

        Returns:
            Optional[dict]: The user's details if the token is valid, None otherwise.
        """
        try:
            response = make_request_with_retry('https://api.github.com/user', auth=self.auth_manager)
            self.auth_manager._check_rate_limit(response)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get user details: {response.status_code} {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting user details: {str(e)}")
            return None

    def get_repository_details(self, owner: str, repo: str) -> Optional[dict]:
        """
        Get the details of a repository from the GitHub API.

        Args:
            owner (str): The owner of the repository.
            repo (str): The name of the repository.

        Returns:
            Optional[dict]: The repository details if the token is valid, None otherwise.
        """
        try:
            url = f'https://api.github.com/repos/{owner}/{repo}'
            response = make_request_with_retry(url, auth=self.auth_manager)
            self.auth_manager._check_rate_limit(response)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get repository details: {response.status_code} {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting repository details: {str(e)}")
            return None
