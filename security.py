from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# ── Config ────────────────────────────────
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ── Password hashing ──────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Password functions ────────────────────
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ── JWT functions ─────────────────────────
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
    
# ── Fake users database ───────────────────
fake_users_db = {
    "john": {
        "username": "john",
        "hashed_password": hash_password("secret123"),
    },
    "jane": {
        "username": "jane",
        "hashed_password": hash_password("password456"),
    }
}

def get_user(username: str) -> dict | None:
    return fake_users_db.get(username)

def authenticate_user(username: str, password: str) -> dict | None:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user