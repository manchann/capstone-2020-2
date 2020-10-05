from sqlalchemy import Column, Integer, String, LargeBinary, UniqueConstraint

from db import Base


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=False)  # 파일 이름(확장자포함)
    file = Column(LargeBinary, nullable=False)  # 평준화된 오디오 파일
    url = Column(String, nullable=False, unique=True)
    image_url = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint('name', 'url'),
    )
