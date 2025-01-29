import datetime
import time
import requests
from requests.auth import AuthBase
from typing import Optional
from dirmapper_core.utils.logger import logger
from ..utils.request_utils import make_request_with_retry

class GitHubAuthManager(AuthBase):
    """
    GitHubAuthManager handles authentication with the GitHub API using an OAuth token.
    """
    def __init__(self, oauth_token: str):
        """
        Initialize the GitHubAuthManager with an OAuth token.

        Args:
            oauth_token (str): The OAuth token provided by the user.
        """
        self.oauth_token = oauth_token

    def __call__(self, r):
        """
        Attach the OAuth token to the request headers.

        Args:
            r (requests.PreparedRequest): The request to modify.

        Returns:
            requests.PreparedRequest: The modified request with the OAuth token.
        """
        r.headers['Authorization'] = f'token {self.oauth_token}'
        return r

    def _check_rate_limit(self, response: requests.Response) -> None:
        """
        Check if the rate limit has been reached and log the error if needed.

        Args:
            response (requests.Response): The response from the GitHub API.

        Raises:
            Exception: If the rate limit has been exceeded.
        """
        if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
            reset_time = response.headers.get('X-RateLimit-Reset')
            if reset_time:
                reset_time = datetime.datetime.fromtimestamp(int(reset_time)).strftime('%Y-%m-%d %H:%M:%S')
            logger.error(f"Rate limit exceeded. Reset time: {reset_time}")
            raise Exception("GitHub API rate limit exceeded.")

    def validate_token(self) -> bool:
        """
        Validate the OAuth token by making a request to the GitHub API.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            response = make_request_with_retry('https://api.github.com/user', auth=self)
            self._check_rate_limit(response)
            if response.status_code == 200:
                logger.info("OAuth token is valid.")
                return True
            else:
                logger.error(f"OAuth token validation failed: {response.status_code} {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error validating OAuth token: {str(e)}")
            return False