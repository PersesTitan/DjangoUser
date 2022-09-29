import json
import random
from unittest import TestCase

from blog.models import Blog
from color_print import p
from user.models import Member
from django.test import Client

from user.tests.test_models import count

client = Client()


class ViewTest(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     count = 100
    #     for author_id in range(count):
    #         Member.objects.create(
    #             login_id=f"Tester{author_id}",
    #             password="1234",
    #             email=f"{author_id}@test.com",
    #             phone_number=f"010-{author_id}111-{author_id}111",
    #             address=f"0000{author_id}",
    #             name="Tester"
    #         )

    @classmethod
    def setUpClass(cls):
        # 데이터 삭제 로직
        Member.objects.all().delete()
        Blog.objects.all().delete()

        rand = lambda: random.randint(0, 9)
        count = 10
        for author_id in range(count):
            phone_random1 = f"{rand()}{rand()}{rand()}{rand()}"
            phone_random2 = f"{rand()}{rand()}{rand()}{rand()}"
            address_random = f"{rand()}{rand()}{rand()}{rand()}{rand()}"

            member = Member.objects.create(
                login_id=f"Tester{author_id}",
                password="1234",
                email=f"{author_id}@test.com",
                phone_number=f"010-{phone_random1}-{phone_random2}",
                address=f"{address_random}",
                name="Tester"
            )

            Blog.objects.create(
                title=f"Test{author_id}",
                content=f"content{author_id}",
                member=member
            )

    def test_view_singup(self):
        request = client.get("/singup/")
        self.assertEqual(request.status_code, 200)

    def test_view_find_member(self):
        request = client.get("/members/")
        print()
        message = "Member List"
        count.log(p.auto_hr(message))
        print("\n".join(str(request.content)[16:-4].split("}, {")))
        self.assertEqual(request.status_code, 200)

    # 데이터 불러오는 로직
    def test_view_find_blog(self):
        request = client.get("/blogs/")
        print()
        message = "Blog List"
        count.log(p.auto_hr(message))
        print("\n".join(str(request.content)[13:-4].split("}, {")))
        self.assertEqual(request.status_code, 200)

    # 게시판
    def test_check_member(self):
        request = client.get("/members/")
        data = json.loads(request.content)
        for i in data["members"]:
            member_id = i["id"]
            request = client.get("/users/" + str(member_id) + "/")
            self.assertEqual(request.status_code, 200)
        self.assertEqual(request.status_code, 200)


    # 데이터 삭제 로직
    @classmethod
    def tearDownClass(cls):
        Member.objects.all().delete()
        Blog.objects.all().delete()
