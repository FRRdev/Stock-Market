from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse

from src.user.models import User
from src.board.models import Board
from .schemas import BoardCreate

from src.user.auth import current_active_user
from .services import check_authors_product

board_router = APIRouter(prefix="/board", tags=["board"])


@board_router.post('', response_model=BoardCreate)
async def create_board(
        product: int = Form(...),
        user: User = Depends(current_active_user)
):
    """Create board router
    """
    if await check_authors_product(user, product):
        board_exists = await Board.objects.filter(product=product, user=user.id).exists()
        if board_exists:
            return JSONResponse({"error": "Board already exists!"})
        else:
            return await Board.objects.create(product=product, user=user.dict())
    else:
        return JSONResponse({"error": "You are not own this product!"})
