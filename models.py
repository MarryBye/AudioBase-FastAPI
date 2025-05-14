# Моделі - те, як дані зберігаються в базі даних. Тут у вигляді класів потрібно описати структуру таблиць.

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base
    
class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True, unique=True)
    
    tracks_connection = relationship("Track", back_populates="authors_connection")
    
class Track(Base):
    __tablename__ = "tracks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    duration = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
    file_name = Column(String)
    
    authors_connection = relationship("Author", back_populates="tracks_connection")
    playlisttracks_connection = relationship("PlaylistTrack", back_populates="track_connection")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    
    playlist_connection = relationship("PlayList", back_populates="user_connection")
    
class PlayList(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    playlisttracks_connection = relationship("PlaylistTrack", back_populates="playlist_connection")
    user_connection = relationship("User", back_populates="playlist_connection")
    
class PlaylistTrack(Base):
    __tablename__ = "playlisttracks"
    
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id"))
    track_id = Column(Integer, ForeignKey("tracks.id"))
    
    playlist_connection = relationship("PlayList", back_populates="playlisttracks_connection")
    track_connection = relationship("Track", back_populates="playlisttracks_connection")