from pydantic import BaseModel
from typing import Optional, Dict

class ConfigItemCreate(BaseModel):
    config_name: str
    config_value: Optional[str] = None
    is_active: bool = True

class ConfigItemResponse(ConfigItemCreate):
    id: int

    class Config:
        from_attributes = True

class ConfigurationCreate(BaseModel):
    """Frontend sends all configs as a dictionary"""
    configs: Dict[str, Optional[str]]

class ConfigurationResponse(BaseModel):
    """Response with all active configs"""
    configs: Dict[str, Optional[str]]
