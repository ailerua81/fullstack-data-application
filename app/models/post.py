from sqlalchemy import Column, String, DateTime, ForeignKey
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from database import BaseSQL

class Post(BaseSQL):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String)
    content = Column(String)
    date_creation_post = Column(DateTime, default=datetime.utcnow)

    author_id = Column(String, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    fiche_lapin_id = Column(String, ForeignKey("fiche_lapin.id", ondelete="CASCADE"))
    fiche_lapin = relationship("FicheLapin", back_populates="posts")

    __table_args__ = ()


