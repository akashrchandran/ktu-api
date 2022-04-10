from email import message
from typing import Optional
from fastapi import FastAPI, Query, status
from pydantic import BaseModel
from scraper import scrape_notifications
from fastapi.responses import JSONResponse

tags = [
    {
        "name": "Get Notifications",
        "description": "Get a list of notifications.",
    }
]

app = FastAPI(
    title="KTU API",
    description="**KTU API** get the list of notifications available in **KTU's** official website and return it in JSON format 🚀",
    version="0.0.1",
    contact={
        "name": "Akash R Chandran",
        "url": "https://links.akashrchandran.in/",
        "email": "chandranrakash@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://spdx.org/licenses/MIT.html",
    },
    openapi_tags=tags
)

class Error_Message(BaseModel):
    error: bool
    message: str

class Valid_Message(BaseModel):
    error: bool
    limit: int
    data: dict

@app.get("/get", tags=["Get Notifications"], responses={200: {"model": Valid_Message}, 500: {"model": Error_Message}})
async def get_notifications(limit: Optional[int] = Query(10, description="Limit the number of notifications from site using this parameter")):
    response = scrape_notifications(limit=limit)
    if isinstance(response, list):
        return JSONResponse({'error': False, 'limit': limit, "data": response})
    else:
        return JSONResponse({'error': True, 'message': str(response)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
