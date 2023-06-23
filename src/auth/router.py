from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import User
from sqlalchemy import select, insert

from database import get_async_session
from auth.schemas import UserCreate, UserLogin

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/register')
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(User.email == user.email)
    result = await session.execute(query)
    if result.fetchall():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This user already exists'
        )

    stmt = insert(User).values(email=user.email, username=user.username, password=user.password)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", 'detail': f'username: {user.username}, email: {user.email}'}


@router.post('/login')
async def login_user(
    user: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(User.password == user.password, User.email == user.email)
    result = await session.execute(query)
    if not result.fetchall():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong email or passwort"
        )
    return {'status': 'success', 'detail': User.email}


