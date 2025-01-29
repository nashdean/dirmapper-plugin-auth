from typing import Optional
from .providers.provider import Provider
from .providers.github_provider import GitHubProvider

class ProviderManager:
    def __init__(self, provider: Provider):
        self.provider = provider

    def authenticate(self) -> bool:
        return self.provider.authenticate()

    def fetch_directory_structure(self, repo_url: str) -> dict:
        return self.provider.fetch_directory_structure(repo_url)

    def validate_token(self) -> bool:
        return self.provider.validate_token()

    def get_user_details(self) -> Optional[dict]:
        return self.provider.get_user_details()

    def get_repository_details(self, owner: str, repo: str) -> Optional[dict]:
        return self.provider.get_repository_details(owner, repo)

# Example usage:
# provider = GitHubProvider(oauth_token="your_token_here")
# manager = ProviderManager(provider)
# manager.authenticate()
# user_details = manager.get_user_details()
# repo_details = manager.get_repository_details(owner="owner_name", repo="repo_name")
