import requests

def fetch_github_issue(repo_url: str, issue_number: int):
    try:
        repo_path = repo_url.split("github.com/")[-1].strip("/")

        github_api_url = f"https://api.github.com/repos/{repo_path}/issues/{issue_number}"

        response = requests.get(
            github_api_url,
            headers={"Accept": "application/vnd.github.v3+json"}
        )
        response.raise_for_status()
        issue_data = response.json()

        return {
            "title": issue_data.get("title"),
            "body": issue_data.get("body"),
            "comments": issue_data.get("comments"),
            "created_at": issue_data.get("created_at"),
            "user": issue_data.get("user", {}).get("login"),
        }

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"GitHub API error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Internal error: {str(e)}")
