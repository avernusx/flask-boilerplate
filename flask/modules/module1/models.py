from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class TestClass(Base):
    __tablename__ = 'test'
    id = Column(UUID,
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    test = Column(String())