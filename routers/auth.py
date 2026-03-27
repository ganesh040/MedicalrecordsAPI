from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from security import authenticate_user, create_access_token, verify_token, get_user

router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ── Login → returns JWT token ─────────────
@router.post("/token")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


# ── Get current user from token ───────────
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    username = verify_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


# ── Protected route — requires login ──────
@router.get("/me")
async def read_me(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return {"username": current_user["username"]}