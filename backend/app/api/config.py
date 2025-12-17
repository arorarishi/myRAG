from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import configuration, schemas
from typing import Dict, Optional

router = APIRouter()

@router.post("/config", response_model=schemas.ConfigurationResponse)
def save_configuration(config: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    """Save or update RAG configuration (key-value pairs)"""
    
    # Iterate through all config items from frontend
    for config_name, config_value in config.configs.items():
        # Check if this config item exists
        db_item = db.query(configuration.ConfigurationItem).filter(
            configuration.ConfigurationItem.config_name == config_name
        ).first()
        
        if db_item:
            # Update existing item
            db_item.config_value = config_value
            db_item.is_active = True
        else:
            # Create new item
            db_item = configuration.ConfigurationItem(
                config_name=config_name,
                config_value=config_value,
                is_active=True
            )
            db.add(db_item)
    
    db.commit()
    
    # Return all active configs
    active_items = db.query(configuration.ConfigurationItem).filter(
        configuration.ConfigurationItem.is_active == True
    ).all()
    
    result_configs = {item.config_name: item.config_value for item in active_items}
    return {"configs": result_configs}

@router.get("/config", response_model=schemas.ConfigurationResponse)
def get_configuration(db: Session = Depends(get_db)):
    """Get all active configuration items"""
    active_items = db.query(configuration.ConfigurationItem).filter(
        configuration.ConfigurationItem.is_active == True
    ).all()
    
    if not active_items:
        # Return empty configs if none exist
        return {"configs": {}}
    
    result_configs = {item.config_name: item.config_value for item in active_items}
    return {"configs": result_configs}

@router.get("/config/all", response_model=Dict[str, dict])
def get_all_configurations(db: Session = Depends(get_db)):
    """Get all configuration items (active and inactive) - useful for admin"""
    all_items = db.query(configuration.ConfigurationItem).all()
    
    result = {
        item.config_name: {
            "value": item.config_value,
            "is_active": item.is_active,
            "id": item.id
        }
        for item in all_items
    }
    
    return result
