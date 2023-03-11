from sqlalchemy import Column, Integer, String
from app.domain.base import Base


class Usuario(Base):
    """Modelo de tabla de usuario"""

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
