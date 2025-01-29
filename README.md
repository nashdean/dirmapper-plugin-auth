# dirmapper-plugin-auth

`dirmapper-plugin-auth` is a plugin for `dirmapper-core` that focuses on authentication for third-party providers. It integrates directly with the `dirmapper` logic to provide seamless authentication capabilities.

## Features

- OAuth token management for GitHub API.
- Rate limit handling and logging.
- Retry mechanism with exponential backoff for transient errors.
- Fetch authenticated user details from GitHub.
- Fetch repository details from GitHub.

## Installation

To install the plugin, use pip:

```sh
pip install dirmapper-plugin-auth
```

## Usage

### GitHub Authentication

To use the `GitHubAuthManager` for authenticating with the GitHub API:

```python
from github.auth_manager import GitHubAuthManager, GitHubUserManager

# Initialize the GitHubAuthManager with your OAuth token
auth_manager = GitHubAuthManager(oauth_token="your_oauth_token")

# Validate the OAuth token
if auth_manager.validate_token():
    print("Token is valid")

# Initialize the GitHubUserManager with the auth manager
user_manager = GitHubUserManager(auth_manager=auth_manager)

# Get authenticated user details
user_details = user_manager.get_user_details()
if user_details:
    print(user_details)

# Get repository details
repo_details = user_manager.get_repository_details(owner="owner_name", repo="repo_name")
if repo_details:
    print(repo_details)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact Nash Dean at nashdean.github@gmail.com.