from pydantic import BaseModel
from typing import Dict, Optional

class SAMLResponse(BaseModel):
    SAMLResponse: str

class UserSession(BaseModel):
    saml_name_id: str
    saml_session_index: str
    attributes: Dict[str, any]
