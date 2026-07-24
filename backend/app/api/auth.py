from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from backend.app.core.config import LOGIN_ENDPOINT, CALLBACK_ENDPOINT

from ..services.github.oauth import build_authorization_url, validate_state, exchange_auth_code_for_token
from ..services.github.api import list_repositories


router=APIRouter()

@router.get(LOGIN_ENDPOINT)
def github_login():
    github_url=build_authorization_url()
    return RedirectResponse(github_url)



@router.get(CALLBACK_ENDPOINT)
async def github_callback(request: Request):
    query=request.query_params
    code=query.get("code")
    state=query.get("state")
    if not validate_state(state):
        raise(HTTPException(status_code=400, detail="Invalid state parameter"))
    token=await exchange_auth_code_for_token(code)
    repos=await list_repositories(token)
    return {
        "repositories" : repos
    }


