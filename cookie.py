# --- Проверка подписи Telegram ---
from datetime import datetime, timedelta
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from jose import JWTError, jwt
import hashlib
import hmac

from database.base import get_db
from env import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def verify_telegram(data: dict, bot_token: str) -> bool:
	hash_to_check = data.pop("hash")
	data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])
	secret_key = hashlib.sha256(bot_token.encode()).digest()
	hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
	return hmac_hash == hash_to_check

def create_access_token(data: dict, expires_delta: timedelta = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

async def get_current_user(token: str, user, db: AsyncSession = Depends(get_db)):
	credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		telegram_id = payload.get("telegram_id")
		if telegram_id is None:
				raise credentials_exception
	except JWTError:
		raise credentials_exception

	if user is None:
		raise credentials_exception
	return user