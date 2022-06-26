def formatprice(price):
    return f'R$ {price:.2f}'.replace('.', ',')


def quanttotalcart(cart):
    if cart:
        return sum([item['quant'] for item in cart.values()])


def totalcart(cart):
    if cart:
        return sum([
            item.get('promo')
            if item.get('promo') else item.get('price')
            for item in cart.values()
        ])
