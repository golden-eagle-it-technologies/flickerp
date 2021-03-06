from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from fauth.tests.auth_objects import get_employee
from fauth.tests.check_methods import check_process_view_post, check_template_and_status_code
from fauth.views import login_view, login_page, logout_view
from config.models import Currency

User = get_user_model()


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user_email = "test@something.com"
        self.test_user_password = 'secret123'
        User.objects.create_user(email=self.test_user_email, password=self.test_user_password)

    # Test whether view returns the right status code and template
    def test_login_view_user_not_authenticated(self):
        check_template_and_status_code(self, login_view, "fauth/login.html")

    def test_login_view_user_is_authenticated(self):
        check_process_view_post(self, login_view,
                                payload={'email': self.test_user_email, 'password': self.test_user_password})

    def test_login_page_view_get(self):
        check_template_and_status_code(self, login_page, "fauth/login.html")

    def test_logout_process_view_get(self):
        check_template_and_status_code(self, logout_view, "fauth/login.html")
