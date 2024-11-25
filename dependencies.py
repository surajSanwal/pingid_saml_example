# dependencies.py
from fastapi import Request
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from config import SAMLConfig
import logging

logger = logging.getLogger(__name__)

async def prepare_fastapi_request(request: Request):
    """
    Prepare FastAPI request for python3-saml library
    """
    form_data = await request.form()
    
    return {
        'https': 'on' if request.url.scheme == 'https' else 'off',
        'http_host': request.headers.get('host', ''),
        'script_name': request.url.path,
        'server_port': request.url.port or (443 if request.url.scheme == 'https' else 80),
        'get_data': dict(request.query_params),
        'post_data': dict(form_data),  # Convert form_data to dict
        'query_string': request.url.query
    }

async def init_saml_auth(request: Request):
    """
    Initialize SAML authentication
    """
    try:
        req = await prepare_fastapi_request(request)
        auth = OneLogin_Saml2_Auth(req, SAMLConfig.SAML_SETTINGS)
        return auth
    except Exception as e:
        logger.error(f"Error initializing SAML auth: {str(e)}", exc_info=True)
        raise e
