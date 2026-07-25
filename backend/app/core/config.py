from dotenv import load_dotenv
import os
load_dotenv()
CLIENT_ID=os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET=os.getenv("GITHUB_CLIENT_SECRET")
LOGIN_ENDPOINT = os.getenv("GITHUB_LOGIN_ENDPOINT", "/auth/github/login")
CALLBACK_URL=os.getenv("GITHUB_CALLBACK_URL")
CALLBACK_ENDPOINT=os.getenv("GITHUB_CALLBACK_ENDPOINT","/auth/github/callback")
API=os.getenv("GITHUB_API")
DOWNLOAD_DIR="/tmp/parcel-builds/downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

BUILD_DIR="/tmp/parcel-builds/builds"
if not os.path.exists(BUILD_DIR):
    os.makedirs(BUILD_DIR)

DB_URL=os.getenv("DATABASE_URL")
JWT_SECRET=os.getenv("JWT_SECRET")
JWT_ALGO=os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")