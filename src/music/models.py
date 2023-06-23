from sqlalchemy import Integer, Column, String, ForeignKey, LargeBinary

from database import Base


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=False)
