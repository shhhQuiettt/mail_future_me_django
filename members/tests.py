from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
from . import utils

# Create your tests here.


class TestCustomUser(TestCase):
    def test_new_superuser_when_valid(self):
        UserModel = get_user_model()
        super_user = UserModel.objects.create_superuser(
            email="test@a.pl", first_name="firstname", password="a gdyby tak..."
        )

        self.assertEqual(super_user.email, "test@a.pl")
        self.assertEqual(super_user.first_name, "firstname")
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "test@a.pl (firstname)")

    def test_new_superuser_when_no_email(self):
        UserModel = get_user_model()
        with self.assertRaises(ValueError):
            super_user = UserModel.objects.create_superuser(
                email="", first_name="firstname", password="a gdyby tak..."
            )

    def test_new_user_when_valid(self):
        UserModel = get_user_model()
        user = UserModel.objects.create_user(
            email="dup@test.com", first_name="ala", password="password"
        )
        self.assertEqual(user.email, "dup@test.com")
        self.assertEqual(user.first_name, "ala")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        def test_new_user_when_blank_email(self):
            with self.assertRaises(ValueError):
                super_user = UserModel.objects.create_user(
                    email="", first_name="firstname", password="a gdyby tak..."
                )


class TestAuthentication(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.user = UserModel.objects.create_user(
            email="test@test.pl",
            password="asdf",
            first_name="andrzejek",
            is_active=True,
        )

    def test_login_form(self):
        url = reverse("login")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/login.html")
        self.assertContains(res, "Log in")

    def test_signup_form(self):
        url = reverse("signup")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/signup.html")
        self.assertContains(res, "Sign up")

    def test_password_reset_form_renders(self):
        url = reverse("password_reset")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_reset_form.html")
        self.assertContains(res, "Reset")

    def test_password_reset_form_redirects(self):
        url = reverse("password_reset")
        res = self.client.post(url, data={"email": "a@w.pl"})

        self.assertRedirects(res, reverse("password_reset_done"))

    def test_password_change_redirects_when_not_logged_in(self):
        url = reverse("password_change")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 302)

    def test_password_change_renders_when_logged_in(self):
        url = reverse("password_change")
        # self.client.force_login(self.user)

        # a = self.client.login(email="test@test.pl", password="asdf")
        self.client.force_login(self.user)

        res = self.client.get(url)

        self.assertTemplateUsed("registration/password_change_form")
        self.assertContains(res, "Change password")
        self.assertEqual(res.status_code, 200)


class TestUtils(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.user = UserModel.objects.create_user(
            email="test@test.pl",
            password="asdf",
            first_name="andrzejek",
            is_active=True,
        )

    def test_send_confirmation_mail(self):
        with patch("members.utils.send_mail") as mock_send_email:
            utils.send_confirmation_mail(user=self.user, domain="localhost:8000")
            mock_send_email.assert_called_once()
