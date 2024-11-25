# main.py
import logging
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
import uvicorn
from typing import Optional
import json

from dependencies import init_saml_auth
from models import SAMLResponse, UserSession
from config import SAMLConfig

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI SAML SSO")
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key",  # Change this to a secure secret key
    session_cookie="session"
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.debug("Handling index route request")
    try:
        user_data = request.session.get("user_data")
        logger.info(f"User data from session: {'Present' if user_data else 'None'}")
        
        response = templates.TemplateResponse(
            "index.html",
            {"request": request, "user": user_data}
        )
        logger.debug("Successfully rendered index template")
        return response
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/saml/metadata")
async def metadata():
    logger.debug("Generating SAML metadata")
    try:
        saml_settings = OneLogin_Saml2_Settings(settings=SAMLConfig.SAML_SETTINGS, sp_validation_only=True)
        metadata = saml_settings.get_sp_metadata()
        errors = saml_settings.validate_metadata(metadata)

        if len(errors) == 0:
            logger.info("SAML metadata generated successfully")
            return Response(
                content=metadata,
                media_type="text/xml"
            )
        else:
            logger.error(f"SAML metadata validation errors: {errors}")
            raise HTTPException(status_code=500, detail=', '.join(errors))
    except Exception as e:
        logger.error(f"Error generating SAML metadata: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/saml/login")
async def login(request: Request, auth: OneLogin_Saml2_Auth = Depends(init_saml_auth)):
    logger.debug("Initiating SAML login")
    try:
        login_url = auth.login()
        logger.info(f"Generated SAML login URL: {login_url}")
        return RedirectResponse(url=login_url)
    except Exception as e:
        logger.error(f"Error during SAML login: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/saml/acs")
async def acs(
    request: Request,
    auth: OneLogin_Saml2_Auth = Depends(init_saml_auth)
):
    logger.debug("Processing SAML assertion")
    try:
        # Process the SAML response
        auth.process_response()
        errors = auth.get_errors()

        if errors:
            logger.error(f"SAML assertion errors: {errors}")
            raise HTTPException(status_code=400, detail="Invalid SAML response")

        if not auth.is_authenticated():
            logger.error("SAML authentication failed")
            raise HTTPException(status_code=401, detail="Authentication failed")

        # Retrieve user data from the SAML response
        saml_name_id = auth.get_nameid()
        saml_session_index = auth.get_session_index()
        attributes = auth.get_attributes()

        if not saml_name_id or not saml_session_index:
            logger.error("SAML response missing required user identifiers")
            raise HTTPException(status_code=400, detail="Incomplete SAML response")

        # Create a session for the authenticated user
        user_session = UserSession(
            saml_name_id=saml_name_id,
            saml_session_index=saml_session_index,
            attributes=attributes,
        )
        request.session["user_data"] = user_session.dict()

        logger.info(f"User {saml_name_id} successfully authenticated")
        
        # Redirect after successful authentication
        redirect_url = "/"  # This can be configurable
        return RedirectResponse(url=redirect_url, status_code=303)

    except OneLogin_Saml2_Error as saml_error:
        logger.error(f"SAML processing error: {saml_error}", exc_info=True)
        raise HTTPException(status_code=400, detail="SAML processing error")
    except Exception as e:
        logger.error(f"Unexpected error processing SAML assertion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/saml/sls")
async def sls(
    request: Request,
    auth: OneLogin_Saml2_Auth = Depends(init_saml_auth)
):
    logger.debug("Processing single logout service request")
    try:
        url = auth.process_slo()
        errors = auth.get_errors()
        if errors:
            logger.error(f"SLO errors: {errors}")
            raise HTTPException(status_code=400, detail=f"SLO Error: {', '.join(errors)}")
        
        request.session.clear()
        logger.info("Single logout completed successfully")
        return RedirectResponse(url=url if url else "/")
    except Exception as e:
        logger.error(f"Error during single logout: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/saml/logout")
async def logout(
    request: Request,
    auth: OneLogin_Saml2_Auth = Depends(init_saml_auth)
):
    logger.debug("Initiating logout process")
    try:
        user_data = request.session.get("user_data")
        if not user_data:
            logger.info("No active session found during logout")
            return RedirectResponse(url="/")
        
        name_id = user_data.get("saml_name_id")
        session_index = user_data.get("saml_session_index")
        logout_url = auth.logout(
            name_id=name_id,
            session_index=session_index
        )
        logger.info(f"Generated logout URL: {logout_url}")
        return RedirectResponse(url=logout_url)
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Add global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error": str(exc)},
        status_code=500
    )

if __name__ == "__main__":
    logger.info("Starting FastAPI SAML SSO application")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
