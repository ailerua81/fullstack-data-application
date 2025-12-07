from sqlalchemy import Column, String
import uuid
from sqlalchemy.orm import relationship
from database import BaseSQL

class User(BaseSQL):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String, unique=True)
    password = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    role = Column(String, default="anonyme")  # admin, fondateur, benevole, anonyme

    posts = relationship("Post", back_populates="author")   

    ficheLapin = relationship(
        "FicheLapin",
        back_populates="auteur",
        cascade="all, delete-orphan"
    )

