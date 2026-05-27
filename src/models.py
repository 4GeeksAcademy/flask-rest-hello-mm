from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts = relationship("Post", back_populates="author")


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    post = relationship("Post", back_populates="comments")


class Like(db.Model):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))


class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)

    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    following_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


if __name__ == "__main__":
    render_er(db.Model, "diagram.png")
