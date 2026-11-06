from datetime import datetime

import bcrypt
from sqlalchemy.orm import relationship
from src.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Table, CheckConstraint


space_members = Table(
    "space_members",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id",  ondelete="CASCADE"), primary_key=True),
    Column("space_id", Integer, ForeignKey("spaces.id", ondelete="CASCADE"), primary_key=True)
)

class Todo(Base):

    __tablename__ = "todos"

    __table_args__ = (
        CheckConstraint("(user_id is NULL) <> (space_id is NULL)", name="todo_owner_xor_space"),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=True)
    space_id = Column(Integer, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=True)

    user = relationship("User", back_populates="todos")
    space = relationship("Space", back_populates="todos")


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    is_active = Column(Boolean, default = True, nullable = False)
    created_at = Column(DateTime, default = datetime.now, nullable = False)

    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")
    spaces = relationship("Space", secondary=space_members, back_populates="members")

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Space(Base):

    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    members = relationship("User", secondary=space_members, back_populates="spaces")
    todos = relationship("Todo", back_populates="space", cascade="all, delete-orphan")
    
