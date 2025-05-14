# Існуючі шляхи на сторінки додатку. Можуть бути й повноцінні сторінки, так й сторінки для обробки запитів.

import models
import schemas
import crud

from fastapi import HTTPException, APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from hashing import hash_password, verify_password
from tokens import create_access_token, decode_access_token

main_router = APIRouter()
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#-----------------------------------------------------------------------------------------------#

# Функція, яка отримує дані користувача з токена
# Вона використовується для перевірки токена при доступі до захищених маршрутів
# Сторінки, які вимагають авторизації використовують аргумент
# current_user: models.User = Depends(get_current_user)
# для отримання даних користувача
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Недійсний токен")
    
    user_id = int(payload.get("sub"))
    user = crud.get_user(db, user_id)
    
    if user is None:
        raise HTTPException(status_code=401, detail="Користувач не знайдений")
    
    return user

#-----------------------------------------------------------------------------------------------#

@main_router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request})

#-----------------------------------------------------------------------------------------------#

@main_router.post("/register", response_model=schemas.User)
def register(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    result = crud.create_user(db, user)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Користувач вже існує!")
    
    return result

@main_router.post("/login")
def login(request: Request, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    result = crud.get_user_by_login(db, form_data.username)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Невірний логін або пароль!")
    
    if not verify_password(form_data.password, result.password):
        raise HTTPException(status_code=400, detail="Невірний логін або пароль!")

    access_token = create_access_token(data={"sub": str(result.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}

#-----------------------------------------------------------------------------------------------#

@main_router.post("/add_author", response_model=schemas.Author)
def add_author(request: Request, author: schemas.AuthorCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.create_author(db, author)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Автор вже існує!")
    
    return result

@main_router.get("/get_authors", response_model=list[schemas.Author])
def get_authors(request: Request, db: Session = Depends(get_db)):
    return crud.get_authors(db)

@main_router.get("/get_author/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)
    
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден!")
    
    return author

@main_router.put("/update_author/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.update_author(db, author_id, author)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Автор не найден!")

    return result

@main_router.delete("/del_author/{author_id}")
def del_author(request: Request, author_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.delete_author(db, author_id)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Автор не найден!")
    
    return result

#-----------------------------------------------------------------------------------------------#
    
@main_router.post("/add_track", response_model=schemas.Track)
def add_track(request: Request, track: schemas.TrackCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.create_track(db, track)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Трек вже існує!")
    
    return result

@main_router.get("/get_tracks", response_model=list[schemas.Track])
def get_tracks(request: Request, db: Session = Depends(get_db)):
    return crud.get_tracks(db)

@main_router.get("/get_track/{track_id}", response_model=schemas.Track)
def get_track(request: Request, track_id: int, db: Session = Depends(get_db)):
    result = crud.get_track(db, track_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Трек не найден!")
    
    return result 

@main_router.get("/get_tracks_by_author/{author_id}", response_model=list[schemas.Track])
def get_tracks_by_author(request: Request, author_id: int, db: Session = Depends(get_db)):
    return crud.get_tracks_by_author(db, author_id)

@main_router.put("/update_track/{track_id}", response_model=schemas.Track)
def update_track(track_id: int, track: schemas.TrackUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.update_track(db, track_id, track)

    if result is None:
        raise HTTPException(status_code=404, detail="Трек не найден!")

    return result

@main_router.delete("/del_track/{track_id}")
def delete_track(request: Request, track_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.delete_track(db, track_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Трек не найден!")
    
    return result

#-----------------------------------------------------------------------------------------------#

@main_router.post("/add_playlist", response_model=schemas.PlayList)
def add_playlist(playlist: schemas.PlayListCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.create_playlist(db, playlist)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Нема такого користувача!")
    
    return result

@main_router.get("/get_playlists", response_model=list[schemas.PlayList])
def get_playlists(db: Session = Depends(get_db)):
    return crud.get_playlists(db)

@main_router.get("/get_playlist/{playlist_id}", response_model=schemas.PlayList)
def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    result = crud.get_playlist(db, playlist_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Плейлист не найден!")
    
    return result

@main_router.get("/get_playlists_by_user/{user_id}", response_model=list[schemas.PlayList])
def get_playlists_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_playlists(db, user_id)

@main_router.put("/update_playlist/{playlist_id}", response_model=schemas.PlayList)
def update_playlist(playlist_id: int, playlist: schemas.PlayListUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.update_playlist(db, playlist_id, playlist)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Плейлист не найден!")
    
    return result

@main_router.delete("/del_playlist/{playlist_id}")
def delete_playlist(playlist_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.delete_playlist(db, playlist_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Плейлист не найден!")

    return result

#-----------------------------------------------------------------------------------------------#

@main_router.post("/add_track_to_playlist", response_model=schemas.PlaylistTrack)
def add_track_to_playlist(link: schemas.PlaylistTrackCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.add_track_to_playlist(db, link.playlist_id, link.track_id)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Невозможно добавить трек.")
    
    return result

@main_router.get("/get_playlist_tracks/{playlist_id}", response_model=list[schemas.PlaylistTrack])
def get_playlist_tracks(playlist_id: int, db: Session = Depends(get_db)):
    return crud.get_playlist_tracks(db, playlist_id)

@main_router.delete("/remove_from_playlist/{link_id}")
def remove_from_playlist(link_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = crud.remove_from_playlist(db, link_id)
    
    if result is None:
        return HTTPException(status_code=404, detail="Связь плейлиста и трека не найдена!")
    
    return result

#-----------------------------------------------------------------------------------------------#