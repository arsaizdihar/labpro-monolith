from django.test import TestCase
from . import api
from mock import Mock
from users.models import User
from .models import BuyHistory


class ItemViewTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.get_items_catalog = api.get_items_catalog
        self.get_items_count = api.get_items_count
        self.get_item_detail = api.get_item_detail
        self.buy_item = api.buy_item

        api.get_items_catalog = Mock(return_value=(True, {
            "data": [
                {
                    "id": "abc",
                    "nama": "barang 1",
                    "harga": 1000,
                    "stok": 10
                },
                {
                    "id": "abcd",
                    "nama": "barang 2",
                    "harga": 1000,
                    "stok": 10
                }
            ]
        }))

        api.get_item_detail = Mock(return_value=(True, {
            "data": {
                "id": "abc",
                "nama": "barang 1",
                "harga": 1000,
                "stok": 10,
                "kode": "ABC"
            }
        }))

        api.get_items_count = Mock(return_value=(True, {
            "data": 2
        }))

        api.buy_item = Mock(return_value=(True, {
            "data": True
        }))

        User.objects.create_user(
            username="testuser", password="testpassword",
            email="testuser@gmail.com")

        self.client.login(username="testuser", password="testpassword")

    def tearDown(self) -> None:
        super().tearDown()
        api.get_items_catalog = self.get_items_catalog
        api.get_items_count = self.get_items_count
        api.get_item_detail = self.get_item_detail
        api.buy_item = self.buy_item

    def test_catalog(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["items"]), 2)

    def test_detail(self):
        response = self.client.get("/barang/abc/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["item"]["id"], "abc")

    def test_buy_and_history(self):
        response = self.client.post("/barang/abc/", {
            "amount": 1,
            "final": "true"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/history")
        self.assertEqual(api.buy_item.call_count, 1)

        history = BuyHistory.objects.get(user__username="testuser")
        self.assertEqual(history.item_id, "abc")
