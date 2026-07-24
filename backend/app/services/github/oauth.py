import os
import secrets
import httpx
from backend.app.core.config import CLIENT_ID, CLIENT_SECRET, CALLBACK_URL

valid_states=set()

def build_authorization_url() -> str:
    state=secrets.token_urlsafe(32)
    valid_states.add(state)
    github_url=(f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&scope=repo&redirect_uri={CALLBACK_URL}&state={state}")
    return github_url


def validate_state(state: str) -> bool:
    if state in valid_states:
        valid_states.remove(state)
        return True
    return False

async def exchange_auth_code_for_token(code: str) -> str:
    async with httpx.AsyncClient() as client:
        response=await client.post("https://github.com/login/oauth/access_token", headers={
            "Accept": "application/json"
        },
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": CALLBACK_URL
        })
    response.raise_for_status()
    data = response.json()

    if "access_token" not in data:
        raise Exception(f"GitHub OAuth failed: {data}")

    return data["access_token"]

