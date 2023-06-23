from fastapi import FastAPI
from music.router import router as router_music
from auth.router import router as router_user

app = FastAPI(
    title='Music Playlist App'
)

app.include_router(router_music)
app.include_router(router_user)


@app.get('/')
def start():
    return {'detail': 'Hello!'}

