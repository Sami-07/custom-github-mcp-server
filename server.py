# server.py
from mcp.server.fastmcp import FastMCP
from github import Github
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create an MCP server
mcp = FastMCP("GitHub MCP")

# Initialize GitHub client
github_token = os.getenv("GITHUB_TOKEN")

github_client = Github(github_token)


@mcp.tool()
def owner_info() -> Dict:
    """Get information about a GitHub owner"""
    owner= github_client.get_user()
    return {
        "name": owner.name,
        "login": owner.login,
        "followers": owner.followers,
        "following": owner.following,
        "public_repos": owner.public_repos,
        "public_gists": owner.public_gists,
        "followers_url": owner.followers_url,
        "following_url": owner.following_url,
        "repos_url": owner.repos_url,
        "events_url": owner.events_url,
        "received_events_url": owner.received_events_url,
        "type": owner.type,
        "site_admin": owner.site_admin,
        
    }

@mcp.tool()
def get_user_info(username: str) -> Dict:
    """Get information about a GitHub user"""
    user = github_client.get_user(username)
    return {
        "name": user.name,
        "login": user.login,
        "bio": user.bio,
        "public_repos": user.public_repos,
        "followers": user.followers,
        "following": user.following
    }

@mcp.tool()
def list_followers(username: str, limit: int = 10) -> List[str]:
    """List followers for a GitHub user (up to limit)"""
    user = github_client.get_user(username)
    return [f.login for f in user.get_followers()[:limit]]

@mcp.tool()
def list_repositories(username: str, limit: int = 5) -> List[Dict]:
    """List repositories for a GitHub user"""
    user = github_client.get_user(username)
    repos = []
    for repo in user.get_repos()[:limit]:
        repos.append({
            "name": repo.name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language
        })
    return repos

@mcp.tool()
def get_repo_issues(owner: str, repo: str, state: str = "open") -> List[Dict]:
    """Get issues for a repository"""
    repository = github_client.get_repo(f"{owner}/{repo}")
    issues = []
    for issue in repository.get_issues(state=state):
        issues.append({
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "created_at": issue.created_at.isoformat(),
            "user": issue.user.login
        })
    return issues

@mcp.tool()
def create_issue(owner: str, repo: str, title: str, body: str, labels: Optional[List[str]] = None) -> Dict:
    """Create a new issue in a repository"""
    repository = github_client.get_repo(f"{owner}/{repo}")
    issue = repository.create_issue(
        title=title,
        body=body,
        labels=labels or []
    )
    return {
        "number": issue.number,
        "title": issue.title,
        "state": issue.state,
        "url": issue.html_url
    }

@mcp.tool()
def get_commit_statuses(owner: str, repo: str, sha: str) -> List[Dict]:
    """Get commit statuses for a specific commit SHA in a repository"""
    repository = github_client.get_repo(f"{owner}/{repo}")
    statuses = repository.get_commit(sha).get_statuses()
    return [{
        "context": s.context,
        "state": s.state,
        "description": s.description,
        "created_at": s.created_at.isoformat()
    } for s in statuses]

@mcp.resource("github://user/{username}")
def get_user_profile(username: str) -> Dict:
    """Get a user's GitHub profile information"""
    return get_user_info(username)

@mcp.resource("github://followers/{username}")
def get_user_followers(username: str) -> List[str]:
    """List a user's followers"""
    return list_followers(username)

@mcp.resource("github://repos/{username}")
def list_user_repos(username: str) -> List[Dict]:
    """List a user's repositories"""
    return list_repositories(username)

@mcp.resource("github://issues/{owner}/{repo}")
def get_repo_issues_resource(owner: str, repo: str) -> List[Dict]:
    """Get issues for a repository"""
    return get_repo_issues(owner, repo)

@mcp.resource("github://commit-status/{owner}/{repo}/{sha}")
def get_commit_status_resource(owner: str, repo: str, sha: str) -> List[Dict]:
    """Get commit statuses for a specific commit SHA"""
    return get_commit_statuses(owner, repo, sha)