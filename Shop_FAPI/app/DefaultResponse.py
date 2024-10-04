from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
from .schemas import User, Product, Order



class DefaultResponse(BaseModel):
    """Стандартный ответ от API."""
    error: bool
    message: Optional[str]
    payload: Optional[list]

