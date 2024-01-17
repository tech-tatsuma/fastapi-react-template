from database import database
from fastapi import Depends, FastAPI, HttpException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from routers import (

# )
from starlette.middleware.cores import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "develop"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(docs_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", dependencies=[Depends(get_current_username)], include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title=app.title)