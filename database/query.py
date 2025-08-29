from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User

async def get_telegram_user(db: AsyncSession, telegram_id: int):
	result = await db.execute(select(User).where(User.telegram_id == telegram_id))
	return result.scalars().first()

async def create_user(db: AsyncSession, telegram_id: int, first_name: str = None, last_name: str = None, username: str = None):
	user = User(
		telegram_id=telegram_id,
		first_name=first_name,
		last_name=last_name,
		username=username
	)
	db.add(user)
	await db.commit()
	await db.refresh(user)
	return user