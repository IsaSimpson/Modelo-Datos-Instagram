import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    likes = relationship("Like", back_populates="user")
    following = relationship("Follow", foreign_keys='Follow.follower_id', back_populates="follower")
    followers = relationship("Follow", foreign_keys='Follow.followed_id', back_populates="followed")

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    image_url = Column(String(250), nullable=False)
    caption = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    # Relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

class Comment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    
    # Relationships
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Like(Base):
    __tablename__ = 'like'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    
    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

class Follow(Base):
    __tablename__ = 'follow'
    
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'))
    followed_id = Column(Integer, ForeignKey('user.id'))
    
    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
