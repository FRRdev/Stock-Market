from src.user.models import User
from src.product.models import Product


async def check_authors_product(user: User, product_pk: int) -> bool:
    """Check that product belongs to user
    """
    product = await Product.objects.get(pk=product_pk)
    if product.user.id == user.id:
        return True
    else:
        return False
