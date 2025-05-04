# GitHub MCP Server

A Simple custom-built MCP server that provides GitHub integration features through various tools and resources.


## Demo

https://github.com/user-attachments/assets/63b92a95-56f3-4290-9c73-acc4ad407246

## Features

- Get user information and profile details
- List user repositories and followers
- Get repository issues
- Create new issues
- Get commit statuses
- Get owner information
- Resource-based access to GitHub data

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your GitHub token:
```
GITHUB_TOKEN=your_github_token_here
```

You can create a GitHub token at: https://github.com/settings/personal-access-tokens with the following permissions:
- `repo` (Full control of private repositories)
- `read:user` (Read user profile data)
- `user:follow` (Follow and unfollow users)

## Available Tools

- `owner_info()`: Get information about the authenticated GitHub user
- `get_user_info(username)`: Get information about a GitHub user
- `list_followers(username, limit=10)`: List followers for a GitHub user
- `list_repositories(username, limit=5)`: List repositories for a GitHub user
- `get_repo_issues(owner, repo, state="open")`: Get issues for a repository
- `create_issue(owner, repo, title, body, labels=None)`: Create a new issue
- `get_commit_statuses(owner, repo, sha)`: Get commit statuses for a specific commit SHA

## Available Resources

- `github://user/{username}`: Get a user's GitHub profile
- `github://followers/{username}`: List a user's followers
- `github://repos/{username}`: List a user's repositories
- `github://issues/{owner}/{repo}`: Get issues for a repository
- `github://commit-status/{owner}/{repo}/{sha}`: Get commit statuses for a specific commit

## Running the Server

```bash
python server.py
```

## Example Usage

```python
# Get authenticated user information
user_info = owner_info()

# Get user information
user_info = get_user_info("octocat")

# List followers
followers = list_followers("octocat", limit=5)

# List repositories
repos = list_repositories("octocat", limit=3)

# Get repository issues
issues = get_repo_issues("octocat", "Hello-World")

# Create a new issue
new_issue = create_issue(
    "octocat",
    "Hello-World",
    "Bug Report",
    "Found a bug in the code",
    labels=["bug"]
)

# Get commit statuses
statuses = get_commit_statuses("octocat", "Hello-World", "abc123")
```

## Response Format Examples

### User Information
```json
{
    "name": "The Octocat",
    "login": "octocat",
    "bio": "GitHub's mascot",
    "public_repos": 8,
    "followers": 1000,
    "following": 9
}
```

### Repository Information
```json
{
    "name": "Hello-World",
    "description": "My first repository",
    "stars": 100,
    "forks": 50,
    "language": "Python"
}
```

### Issue Information
```json
{
    "number": 1,
    "title": "Bug Report",
    "state": "open",
    "created_at": "2024-05-04T14:35:40.784Z",
    "user": "octocat"
}
```
