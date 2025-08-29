from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from cookie import create_access_token, verify_telegram
from database.base import get_db
from database.models import BotMessageTemplate
from database.query import create_user, get_telegram_user
from env import BOT_TOKEN


router = APIRouter()
templates = Jinja2Templates(directory="src")


@router.get("/", response_class=HTMLResponse)
async def auth_index(request: Request, db: AsyncSession = Depends(get_db)):
	return templates.TemplateResponse("auth.html", {"request": request})

@router.post("/telegram", response_class=HTMLResponse)
async def auth_telegram(request: Request, db: AsyncSession = Depends(get_db)):
	form = await request.form()
	data = dict(form)
	if not verify_telegram(data.copy(), BOT_TOKEN):
		raise HTTPException(status_code=400, detail="Invalid Telegram data")
	
	telegram_id = int(data["id"])
	user = await get_telegram_user(db, telegram_id)
	if not user:
		await create_user(
			db,
			telegram_id=telegram_id,
			first_name=data.get("first_name"),
			last_name=data.get("last_name"),
			username=data.get("username")
		)

	access_token = create_access_token({"telegram_id": telegram_id})
	return templates.TemplateResponse("auth.html", {"request": request, "status": "ok", "token": access_token})