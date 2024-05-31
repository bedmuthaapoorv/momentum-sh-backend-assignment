from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests

app=FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class RepoInput(BaseModel):
    repo_url: HttpUrl

@app.post("/repos/")
async def analyze_repo(repo: RepoInput):
    repo_url = repo.repo_url
    # Example logic: Extract owner and repo name from URL
    try:
        owner, repo_name = repo_url.path.strip("/").split("/")[-2:]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL format")

    # Example: Fetch repository data from GitHub API
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    response = requests.get(api_url)

    if response.status_code == 200:
        repo_data = response.json()
        return {
            "full_name": repo_data["full_name"],
            "description": repo_data["description"],
            "clone_url": repo_data["clone_url"],
            "stars": repo_data["stargazers_count"],
            "forks": repo_data["forks_count"],
            "open_issues": repo_data["open_issues_count"]
        }
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch repository data from GitHub")
