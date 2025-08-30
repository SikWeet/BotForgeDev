from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from cookie import create_access_token, get_current_user, verify_telegram
from database.base import get_db
from database.models import BotMessageTemplate
from database.query import create_user, get_telegram_user
from env import BOT_TOKEN, BOT_USERNAME


router = APIRouter()
templates = Jinja2Templates(directory="src/auth")


@router.get("/", response_class=HTMLResponse)
async def auth_index(request: Request, db: AsyncSession = Depends(get_db)):
	get_current_user()
	return templates.TemplateResponse("auth.html", {"request": request, "bot_username": BOT_USERNAME})

@router.get("/telegram", response_class=HTMLResponse)
async def auth_telegram(request: Request, db: AsyncSession = Depends(get_db)):
	params = dict(request.query_params)
	print("Telegram auth data:", params)
	if not verify_telegram(params.copy(), BOT_TOKEN):
		raise HTTPException(status_code=400, detail="Invalid Telegram data")
	
	telegram_id = int(params["id"])
	user = await get_telegram_user(db, telegram_id)
	if not user:
		await create_user(
			db,
			telegram_id=telegram_id,
			first_name=params.get("first_name"),
			last_name=params.get("last_name"),
			username=params.get("username")
		)

	access_token = create_access_token({"telegram_id": telegram_id})
	return templates.TemplateResponse("index.html", {"request": request, "status": "ok", "token": access_token})