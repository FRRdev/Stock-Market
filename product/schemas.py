from pydantic import BaseModel
import datetime


class UploadProduct(BaseModel):
    name: str
    start_price: float
    deadline_time: datetime.datetime
