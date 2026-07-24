import httpx
from backend.app.core.config import API

async def list_repositories(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://{API}/user/repos",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
    response.raise_for_status()
    repos = response.json()
    return [
        {
            "id": repo["id"],
            "name": repo["name"],
            "owner": repo["owner"]["login"],
            "private": repo["private"],
            "default_branch": repo["default_branch"],
        }
        for repo in repos
    ]



async def download_tarball(token:str,owner:str,repo:str,branch:str) -> bytes:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response=await client.get(
            f"https://{API}/repos/{owner}/{repo}/tarball/{branch}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
    response.raise_for_status()
    return response.content
    