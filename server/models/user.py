from server.db import db
from .base import BaseModel


class User(BaseModel):
    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(80), unique=True, nullable=False)
    password: str = db.Column(db.String(255), nullable=False)
    conversations = db.relationship("Conversation", back_populates="user")

    def as_dict(self):
        return {"id": self.id, "email": self.email}