# Схеми - це структури даних, які описують, як виглядають дані в запитах та відповідях API.
# Простими словами - як ви побачите дані після запиту до API. Тобто не у вигляді словника,
# а у вигляді об'єкта з атрибутами. Також корисно для валідації даних.

from pydantic import BaseModel, Field

class AuthorBase(BaseModel):
    nickname: str
    
class AuthorCreate(AuthorBase):
    pass

class AuthorDelete(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    
    class Config:
        from_attributes = True
        
class TrackBase(BaseModel):
    name: str
    duration: int
    author_id: int
    file_name: str
    
class TrackCreate(TrackBase):
    pass

class TrackDelete(TrackBase):
    pass

class TrackUpdate(TrackBase):
    pass

class Track(TrackBase):
    id: int
    
    class Config:
        from_attributes = True
        
class UserBase(BaseModel):
    login: str
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserLogin(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        
class PlayListBase(BaseModel):
    name: str
    user_id: int

class PlayListCreate(PlayListBase):
    pass

class PlayListUpdate(PlayListBase):
    pass

class PlayList(PlayListBase):
    id: int

    class Config:
        from_attributes = True
        
class PlaylistTrackBase(BaseModel):
    playlist_id: int
    track_id: int

class PlaylistTrackCreate(PlaylistTrackBase):
    pass

class PlaylistTrack(PlaylistTrackBase):
    id: int

    class Config:
        from_attributes = True