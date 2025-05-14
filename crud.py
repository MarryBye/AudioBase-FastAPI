# Ваші CRUD операції з базою даних.
# C - Create, R - Read, U - Update, D - Delete
# CRUD - Create, Read, Update, Delete
# Тобто функції для роботи із БД.

import models
import schemas

from sqlalchemy.orm import Session

#-----------------------------------------------------------------------------------------------#

def get_authors(db: Session, limit: int = 100):
    return db.query(models.Author).limit(limit).all()

def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_author_by_name(db: Session, nickname: str):
    return db.query(models.Author).filter(models.Author.nickname == nickname).first()

def create_author(db: Session, author: schemas.AuthorCreate):
    
    if get_author_by_name(db, author.nickname):
        return None
    
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    
    return db_author

def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate):
    db_author = get_author_by_id(db, author_id)
    
    if db_author is None:
        return None
    
    for k,v in author.model_dump().items():
        setattr(db_author, k, v) # db_author.k = v
        
    db.commit()
    db.refresh(db_author)
    
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = get_author_by_id(db, author_id)
    
    if db_author is None:
        return None
    
    if db_author:
        db.delete(db_author)
        db.commit()
        
    return db_author

#-----------------------------------------------------------------------------------------------#

def get_tracks(db: Session, limit: int = 100):
    return db.query(models.Track).limit(limit).all()

def get_track(db: Session, track_id: int):
    return db.query(models.Track).filter(models.Track.id == track_id).first()

def get_track_by_name(db: Session, name: str):
    return db.query(models.Track).filter(models.Track.name == name).first()

def get_tracks_by_author(db: Session, author_id: int):
    return db.query(models.Track).filter(models.Track.author_id == author_id).all()

def create_track(db: Session, track: schemas.TrackCreate):
    db_track = models.Track(**track.model_dump())
    
    if get_track_by_name(db, db_track.name):
        return None
    
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    
    return db_track

def update_track(db: Session, track_id: int, track: schemas.TrackUpdate):
    db_track = get_track(db, track_id)
    
    if db_track is None:
        return None
    
    for k, v in track.model_dump().items():
        setattr(db_track, k, v)
        
    db.commit()
    db.refresh(db_track)
    
    return db_track

def delete_track(db: Session, track_id: int):
    db_track = get_track(db, track_id)
    
    if db_track is None:
        return None
    
    db.delete(db_track)
    db.commit()
        
    return db_track

#-----------------------------------------------------------------------------------------------#

def get_users(db: Session, limit: int = 100):
    return db.query(models.User).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    
    if get_user_by_login(db, db_user.login):
        return None
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    
    if db_user is None:
        return None
    
    for k, v in user.model_dump().items():
        setattr(db_user, k, v)
        
    db.commit()
    db.refresh(db_user)
    
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    
    if db_user is None:
        return None
    
    db.delete(db_user)
    db.commit()
    
    return db_user

#-----------------------------------------------------------------------------------------------#

def get_playlists(db: Session, limit: int = 100):
    return db.query(models.PlayList).limit(limit).all()

def get_playlist(db: Session, playlist_id: int):
    return db.query(models.PlayList).filter(models.PlayList.id == playlist_id).first()

def get_user_playlists(db: Session, user_id: int, limit: int = 100):
    return db.query(models.PlayList).filter(models.PlayList.user_id == user_id).limit(limit).all()

def get_playlist_tracks(db: Session, playlist_id: int):
    return db.query(models.PlaylistTrack).filter(models.PlaylistTrack.playlist_id == playlist_id).all()

def create_playlist(db: Session, playlist: schemas.PlayListCreate):
    db_user = get_user(db, playlist.user_id)
    
    if db_user is None:
        return None
    
    db_playlist = models.PlayList(**playlist.model_dump())
    
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    
    return db_playlist

def update_playlist(db: Session, playlist_id: int, playlist: schemas.PlayListUpdate):
    db_playlist = get_playlist(db, playlist_id)
    
    if db_playlist is None:
        return None
    
    for k, v in playlist.model_dump().items():
        setattr(db_playlist, k, v)
        
    db.commit()
    db.refresh(db_playlist)
    
    return db_playlist

def delete_playlist(db: Session, playlist_id: int):
    db_playlist = db.query(models.PlayList).filter(models.PlayList.id == playlist_id).first()
    if db_playlist:
        db.delete(db_playlist)
        db.commit()
    return db_playlist

#-----------------------------------------------------------------------------------------------#

def add_track_to_playlist(db: Session, playlist_id: int, track_id: int):
    db_playlist = get_playlist(db, playlist_id)
    db_track = get_track(db, track_id)
    
    if db_playlist is None:
        return None
    
    if db_track is None:
        return None
    
    db_link = models.PlaylistTrack(playlist_id=playlist_id, track_id=track_id)
    
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link
    
def remove_track_from_playlist(db: Session, playlist_id: int, track_id: int):
    db_link = db.query(models.PlaylistTrack).filter(models.PlaylistTrack.playlist_id == playlist_id, models.PlaylistTrack.track_id == track_id).first()
    
    if db_link is None:
        return None
    
    db.delete(db_link)
    db.commit()
    
    return db_link


