from basketapp.models import Basket


def basket(request):
    basket_item = []
    if request.user.is_authenticated:
        basket_item = Basket.get_total_price_and_quantity(request.user)
    return {
        'basket': basket_item,
    }