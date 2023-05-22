from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

# from .database import engine


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="false", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    owner_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        Integer,
        ForeignKey("posts.post_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    post = relationship("Post")
    user = relationship("User")


# Create the database using sqlalchemy
# Base.metadata.create_all(bind=engine)
