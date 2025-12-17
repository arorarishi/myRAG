from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base

class ConfigurationItem(Base):
    __tablename__ = "configuration_items"

    id = Column(Integer, primary_key=True, index=True)
    config_name = Column(String, unique=True, index=True)
    config_value = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
