from ..core.config import DOWNLOAD_DIR
from api import download_tarball
from datetime import datetime
from pathlib import Path

def save_tarball(data: bytes):

    download_dir=Path(DOWNLOAD_DIR)
    
