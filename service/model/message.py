
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

Base = declarative_base()


class Message(Base):
    """
    SQLAlchemy model for a message
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sensor_name = Column(String(40))
    value = Column(Integer)
    ts = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"Value: {self.value} for sensor {self.id}:{self.sensor_name}"
            f" on {self.ts}"
        )
