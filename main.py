from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database.base import Base, engine, get_db
from router import auth, profile, template

app = FastAPI(title="BotForge")
app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

@app.on_event("startup")
async def startup():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(template.router, prefix="/template", tags=["template"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])