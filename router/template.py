from fastapi import APIRouter, Form, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import get_db
from database.models import BotMessageTemplate


router = APIRouter()
templates = Jinja2Templates(directory="src")

@router.post("/set_template", response_class=HTMLResponse)
def set_template(bot_id: int = Form(...), 
					feature_name: str = Form(...), 
					template_text: str = Form(...), 
					request = Request,
					db: AsyncSession = Depends(get_db)):
	template = db.query(BotMessageTemplate).filter(
		BotMessageTemplate.bot_id == bot_id,
		BotMessageTemplate.feature_name == feature_name
	).first()
	
	if not template:
		template = BotMessageTemplate(bot_id=bot_id, feature_name=feature_name, template_text=template_text)
		db.add(template)
	else:
		template.template_text = template_text
	
	db.commit()
	return templates.TemplateResponse("template_set.html", {"request": request, "status": "ok", "feature": feature_name, "template": template_text})