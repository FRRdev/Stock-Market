import datetime
from typing import Tuple

from src.user.models import User
from src.product.models import Product
from .models import Board, Bet


async def check_authors_product(user: User, product_pk: int) -> bool:
    """Check that product belongs to user
    """
    product = await Product.objects.get(pk=product_pk)
    if product.user.id == user.id:
        return True
    else:
        return False


async def check_correct_bet(board: Board, bet: float) -> Tuple[bool, str]:
    """Check that bet has correct price
    """
    if await board.board_bets.count() == 0:
        min_price = board.product.start_price
    else:
        last_bet = await Bet.objects.filter(board=board).order_by("-rate").first()
        min_price = last_bet.rate
    if min_price < bet:
        return True, ""
    else:
        error_message = f"Minimal bet should be {min_price}"
        return False, error_message


async def check_correct_bet_date(board: Board) -> Tuple[bool, str]:
    """Check that bet has correct time
    """
    date_of_bet = datetime.datetime.now()
    deadline_time = board.product.deadline_time
    if date_of_bet < deadline_time:
        return True, ""
    else:
        last_bet = await Bet.objects.select_related("user").filter(board=board).order_by("-rate").first()
        name_of_winners = last_bet.user.username
        error_message = f"Board is closed! {name_of_winners} is winner!"
        return False, error_message
