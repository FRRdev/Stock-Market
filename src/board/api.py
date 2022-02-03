import ormar.exceptions
from fastapi import APIRouter, Form, Depends, Path
from fastapi.responses import JSONResponse
from typing import List
import datetime

from src.user.models import User
from src.board.models import Board, Bet
from .schemas import BoardList, BoardCreate, CreateBet, BoardDetail

from src.user.auth import current_active_user
from .services import (
    check_authors_product,
    check_correct_bet,
    check_correct_bet_date
)

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


@board_router.get('/{board_pk}', response_model=BoardDetail)
async def get_board_info(
        board_pk: int = Path(...),
        user: User = Depends(current_active_user)
):
    """Get information about board
    """
    try:
        board = await Board.objects.prefetch_related("board_bets").select_related(
            ["user", "product", Board.board_bets.user]).get(pk=board_pk)
    except ormar.exceptions.NoMatch:
        return JSONResponse({"error": "This Board does not exist"})
    board_info = board.dict()
    deadline_time_board = board.product.deadline_time
    board_info["deadline_time"] = deadline_time_board
    board_info["active"] = True if datetime.datetime.now() < deadline_time_board else False
    return board_info


@board_router.get('/list', response_model=List[BoardList])
async def get_list_boards(
        user: User = Depends(current_active_user)
):
    """Get list boards router
    """
    return await Board.objects.select_related(["user", "product"]).all()


@board_router.post('/bet/{board_pk}', response_model=CreateBet)
async def make_bet(
        board_pk: int,
        bet: float = Form(...),
        user: User = Depends(current_active_user)
):
    """Make bet by board id
    """
    try:
        board = await Board.objects.select_related("product").get(pk=board_pk)
    except ormar.exceptions.NoMatch:
        return JSONResponse({"error": "This Board does not exist"})
    if not await check_authors_product(user, board.product.id):
        correct_bet_price, message = await check_correct_bet(board, bet)
        if correct_bet_price:
            correct_bet_date, message = await check_correct_bet_date(board)
            if correct_bet_date:
                return await Bet.objects.create(board=board_pk, user=user.id, rate=bet)
            else:
                return JSONResponse({"error": message})
        else:
            return JSONResponse({"error": message})
    else:
        return JSONResponse({"error": "You are author of this Board"})
