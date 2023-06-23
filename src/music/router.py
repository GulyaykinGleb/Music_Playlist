import os

from fastapi import (APIRouter, Depends, Request, Path, HTTPException,
                     File, UploadFile)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from starlette import status
from starlette.responses import FileResponse

from database import get_async_session
from music.models import Music
from music.utils import get_correct_name

router = APIRouter(
    prefix='/user/music',
    tags=['Music']
)


@router.post('/{user_id}/upload')
async def upload_music(
        request: Request,
        user_id: int = Path(),
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_async_session),
):
    if not file.filename.endswith('.mp3'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This isn't a mp3 file"
        )

    result = await session.execute(select(Music.title))
    title = file.filename[:-4]
    all_titles = [music[0] for music in result.fetchall()]
    title: str = get_correct_name(title, all_titles)

    stmt = insert(Music).values(user_id=user_id, title=title, filename=f'{title}.mp3', content=file.file.read())
    await session.execute(stmt)
    await session.commit()

    host = request.url.hostname
    port = request.url.port
    scheme = request.url.scheme
    result = await session.execute(select(Music).where(Music.title == title, Music.user_id == user_id))
    music: Music = result.fetchall()[0][0]
    url = f'{scheme}://{host}:{port}/user/music/{music.user_id}/download?title={music.title}'
    return {"url for downloading": url}


@router.get('/{user_id}/download')
async def download_music(
        title: str,
        user_id: int = Path(),
        session: AsyncSession = Depends(get_async_session),
):
    query = select(Music).where(Music.title == title, Music.user_id == user_id).limit(1)
    result = await session.execute(query)
    if result:
        music = result.fetchall()[0][0]
        with open(f'uploaded_files/{user_id}{music.filename}', 'wb') as file:
            file.write(music.content)
        downloaded_file = FileResponse(
            path=f'uploaded_files/{user_id}{music.filename}',
            filename=music.filename,
            media_type='mp3'
        )
        return downloaded_file
        os.remove(path=f'uploaded_files/{user_id}{music.filename}')
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No such file'
        )


@router.get('/{user_id}/playlist')
async def get_music(
        user_id: int = Path(),
        session: AsyncSession = Depends(get_async_session),
):
    query = select(Music.title).where(Music.user_id == user_id)
    result = await session.execute(query)
    playlist = [music[0] for music in result.fetchall()]
    return {'status': 'success', 'playlist': playlist}
