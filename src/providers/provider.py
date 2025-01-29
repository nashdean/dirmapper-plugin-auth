from typing import Optional


class Provider:
    def authenticate(self):
        raise NotImplementedError("Provider must implement the authenticate method.")

    def fetch_directory_structure(self, repo_url: str) -> dict:
        raise NotImplementedError("Provider must implement the fetch_directory_structure method.")

    def validate_token(self) -> bool:
        raise NotImplementedError("Provider must implement the validate_token method.")

    def get_user_details(self) -> Optional[dict]:
        raise NotImplementedError("Provider must implement the get_user_details method.")

    def get_repository_details(self, owner: str, repo: str) -> Optional[dict]:
        raise NotImplementedError("Provider must implement the get_repository_details method.")
