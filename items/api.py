from service.api import ServiceRequest


def get_items_catalog(page: int):
    return ServiceRequest.get('/barang', params={'page': page, 'limit': 10})


def get_items_count():
    return ServiceRequest.get('/barang/count')


def get_item_detail(item_id: str):
    return ServiceRequest.get(f'/barang/{item_id}')


def buy_item(item_id: str, quantity: int):
    return ServiceRequest.post(f'/barang/{item_id}/buy', data={'total': quantity})
