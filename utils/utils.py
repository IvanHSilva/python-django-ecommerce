def formatprice(price):
    return f'R$ {price:.2f}'.replace('.', ',')


def quanttotalcart(cart):
    if cart:
        return sum([item['quant'] for item in cart.values()])
