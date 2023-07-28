from django.test import TestCase
from .models import User


class AuthViewTest(TestCase):
    def test_register(self):
        get_response = self.client.get("/register/")
        self.assertEqual(get_response.status_code, 200)
        post_reponse = self.client.post("/register/", {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password1": "test1234",
            "password2": "test1234"
        })
        self.assertEqual(post_reponse.status_code, 302)
        self.assertIsNotNone(post_reponse.cookies.get("access_token"))
        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@gmail.com")

    def test_register_failed(self):
        response = self.client.post("/register/", {
            "username": "testuser",
            "email": "testuser@gmail.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["form"].errors["password1"])

    def test_login(self):
        response_get = self.client.get("/login/")
        self.assertEqual(response_get.status_code, 200)

        User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="test1234"
        )

        response_post = self.client.post("/login/", {
            "username": "testuser",
            "password": "test1234"
        })

        self.assertEqual(response_post.status_code, 302)
        self.assertIsNotNone(response_post.cookies.get("access_token"))

    def test_login_failed(self):
        response = self.client.post("/login/", {
            "username": "testuser",
            "password": "test1234"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["form"].errors["__all__"])
