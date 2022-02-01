from typing import List
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Request, Depends
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from src.user.models import User
from .models import Bet,Board

from src.user.auth import current_active_user

board_router = APIRouter(tags=["board"])