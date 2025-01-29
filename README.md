# dirmapper-provider

`dirmapper-provider` is a plugin for `dirmapper-core` that focuses on integrating with third-party providers like GitHub. It provides seamless authentication and API interaction capabilities.

## Features

- OAuth token management for GitHub API.
- Rate limit handling and logging.
- Retry mechanism with exponential backoff for transient errors.
- Fetch authenticated user details from GitHub.
- Fetch repository details from GitHub.
- Fetch directory structure from GitHub repositories.

## Installation

To install the plugin, use pip:

```sh
pip install dirmapper-provider
```

## Usage

### GitHub Provider

To use the `GitHubProvider` for interacting with the GitHub API:

```python
from providers.github_provider import GitHubProvider
from service import ProviderManager

# Initialize the GitHubProvider with your OAuth token
provider = GitHubProvider(oauth_token="your_oauth_token")

# Initialize the ProviderManager with the GitHubProvider
manager = ProviderManager(provider)

# Authenticate the provider
if manager.authenticate():
    print("Token is valid")

# Fetch authenticated user details
user_details = manager.get_user_details()
if user_details:
    print(user_details)

# Fetch repository details
repo_details = manager.get_repository_details(owner="owner_name", repo="repo_name")
if repo_details:
    print(repo_details)

# Fetch directory structure
repo_url = "https://github.com/owner_name/repo_name"
directory_structure = manager.fetch_directory_structure(repo_url)
print(directory_structure)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact Nash Dean at nashdean.github@gmail.com.