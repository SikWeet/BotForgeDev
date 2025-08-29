from fastapi import APIRouter, Form, HTTPException
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates
from h11 import Request
from sqlalchemy.ext.asyncio import AsyncSession
from cookie import create_access_token, get_current_user, verify_telegram
from database.base import get_db
from database.models import BotMessageTemplate, User
from database.query import create_user, get_telegram_user
from env import BOT_TOKEN


router = APIRouter()
templates = Jinja2Templates(directory="src")


@router.get("/profile")
async def profile(request = Request, current_user: User = Depends(get_current_user)):
	return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})