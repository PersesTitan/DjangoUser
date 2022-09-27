from unittest import TestCase

from user.models import Member
from django.test import Client

client = Client()


class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        count = 5
        for author_id in range(count):
            Member.objects.create(
                login_id=f"Tester{author_id}",
                password="1234",
                email=f"{author_id}@test.com",
                phone_number=f"010-{author_id}111-{author_id}111",
                address=f"0000{author_id}",
                name="Tester"
            )

    def test_view_singup(self):
        request = client.get("/singup/")
        self.assertEqual(request.status_code, 200)

    def test_view_find_member(self):
        request = client.get("/find/")
        self.assertEqual(request.status_code, 200)


