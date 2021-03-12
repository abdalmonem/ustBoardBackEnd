
# Pagination method
def pagination(model, page_num, url):
    data = model
    page_num = int(page_num)
    amount = 10
    total = len(model)
    position = -1
    if (total / amount) % 2 == 0:
        pages = round(total / amount)
    else:
        pages = round(total / amount) + 1
        
    json_obj = {
        'page_num': page_num,
        'pages': pages,
        'amount': amount,
        'next': '',
        'previous': '',
        'data': {}
    }
    if page_num == 1:
        position = page_num - 1
        until = position + amount
        json_obj['data'] = data[position: until]
        json_obj['previous'] = ''
        json_obj['next'] = url + '?page_num={}&amount={}'.format(page_num + 1, amount)
    elif page_num > 1 and page_num == pages:
        position = (page_num * 10) - amount
        until = position + amount
        json_obj['data'] = data[((position - 1) - amount ): until]
        json_obj['next'] = ''
        json_obj['previous'] = url + '?page_num={}&amount={}'.format(page_num - 1, amount)
    else:
        position = (page_num * 10) - amount
        until = position + amount
        json_obj['data'] = data[((position - 1) - amount ): until]
        json_obj['previous'] = url + '?page_num={}&amount={}'.format(page_num - 1, amount)
        json_obj['next'] = url + '?page_num={}&amount={}'.format(page_num + 1, amount)
    json_obj['data'] = data[position: until]
    return json_obj

