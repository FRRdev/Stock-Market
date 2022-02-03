from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str = None


class UploadVideo(BaseModel):
    title: str
    description: str


class Message(BaseModel):
    message: str


class GetListVideo(BaseModel):
    id: int
    title: str
    description: str


class GetVideo(GetListVideo):
    user: User
