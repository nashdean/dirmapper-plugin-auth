import os

class Config:
    GITHUB_OAUTH_TOKEN = os.getenv("GITHUB_OAUTH_TOKEN", "default_token")

# Example usage:
# from .config import Config
# oauth_token = Config.GITHUB_OAUTH_TOKEN
