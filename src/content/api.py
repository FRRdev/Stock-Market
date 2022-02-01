from typing import List
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Request, Depends
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from src.user.models import User
from .schemas import GetListVideo, UploadVideo
from .models import Video
from .services import save_video, open_file

from src.user.auth import current_active_user

video_router = APIRouter(tags=["video"])
templates = Jinja2Templates(directory="templates")


@video_router.post('/', response_model=UploadVideo)
async def create_video(
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
        product: int = Form(...),
        user: User = Depends(current_active_user)
):
    return await save_video(user, product, file, title, description, background_tasks)


@video_router.get("/user/{user_pk}", response_model=List[GetListVideo])
async def get_list_video(user_pk: str):
    video_list = await Video.objects.filter(user=user_pk).all()
    return video_list


@video_router.get("/video/{video_pk}")
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response


@video_router.get("/index/{video_pk}", response_class=HTMLResponse)
async def get_video(request: Request, video_pk: int):
    return templates.TemplateResponse("index.html", {"request": request, "path": video_pk})


@video_router.get("/404", response_class=HTMLResponse)
async def error_404(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})


@video_router.post("/{video_pk}", status_code=201)
async def add_like(video_pk: int, user: User = Depends(current_active_user)):
    _video = await Video.objects.select_related("like_user").get(pk=video_pk)
    _user = await User.objects.get(id=user.id)
    if _user in _video.like_user:
        _video.like_count -= 1
        await _video.like_user.remove(_user)
    else:
        _video.like_count += 1
        await _video.like_user.add(_user)
    await _video.update()
    return _video.like_count

# @video_router.post('/img', status_code=201)
# async def upload_image(files: List[UploadFile] = File(...)):
#     for img in files:
#         with open(f'{img.filename}', 'wb') as buffer:
#             shutil.copyfileobj(img.file, buffer)
#     return {'file_name': 'Good'}
