import json
import re

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user import models
from user.models import Member


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class Login(View):
    def post(self, request):
        data = json.loads(request.body)
        user_id = data['id']
        password = data['password']
        user = Member.objects.filter(Q(login_id=user_id) & Q(password=password))
        if len(user) == 0:
            raise ValidationError('비밀번호 또는 아이디가 틀렸습니다.')
        # else:
        #     response = HttpResponse("로그인 완료")
        #     response.set_cookie('token', user[0].id)
        return redirect('blogs')

    def get(self, request):
        return render(request, 'login.html')


def make_massage(keyword):
    return f'{keyword}를 공백으로 사용할 수 없습니다.'


# {
#     "id": "1",
#     "password": "12",
#     "password-check": "12",
#     "email": "1@tests.com"
# }
@method_decorator(csrf_exempt, name='dispatch')
class SingUp(View):
    def post(self, request):
        data = json.loads(request.body)
        user_id = data['id'].strip()
        password = data['password'].strip()
        password_check = data['password-check'].strip()
        email = data['email'].strip()
        phone = data['phone'].strip()
        address = data['address'].strip()

        # 비밀번호, 이메일 유효성 검증
        if not user_id:
            raise ValidationError(make_massage('아이디'))
        elif not email:
            raise ValidationError(make_massage('이메일'))
        elif password_check != password:
            raise ValidationError('비밀번호가 일치하지 않습니다.')
        elif not password:
            raise ValidationError(make_massage('비밀번호'))
        elif not re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$").match(email):
            raise ValidationError('이메일의 형식이 일치하지 않습니다.')
        elif not re.compile("^\\d{2,3}-\\d{4}-\\d{4}$").match(phone):
            raise ValidationError('전화번호의 형식이 일치하지 않습니다.')
        elif not re.compile("^\\d{5}$").match(address):
            raise ValidationError('주소는 5자리 입니다.')
        member = models.Member(
            login_id=user_id,
            email=email,
            password=password,
            phone_number=phone,
            address=int(address)
        )
        member.save()
        return JsonResponse({"member": member.id}, status=201)

    def get(self, request):
        return render(request, 'singup.html')


def blank_check(value):
    return (value is not None) and bool(value.strip())


# {
#     "id": "a3",
#     "password": "15",
#     "email": null
# }
@method_decorator(csrf_exempt, name='dispatch')
class Edit(View):
    # @api_view(['PATCH'])
    def patch(self, request, uid):
        member = get_object_or_404(Member, pk=uid)

        data = json.loads(request.body)
        user_id = data['id']
        email = data['email']
        password = data['password']
        phone = data['phone'].strip()
        address = data['address'].strip()

        # 중복은 unique 에 의존
        if blank_check(user_id):
            member.login_id = user_id
        if blank_check(email):
            member.email = email
        if blank_check(password):
            member.password = password
        if blank_check(phone):
            member.phone_number = phone
        if blank_check(address):
            member.address = address
        member.save()
        return JsonResponse({"member": user_id}, status=200)

    # 삭제 기능
    def delete(self, request, uid):
        member = get_object_or_404(Member, pk=uid)
        member.delete()
        return JsonResponse({"message": "삭제 완료"}, status=201)

    def get(self, request, uid):
        member = get_object_or_404(Member, pk=uid)
        return JsonResponse({"id": member.id}, status=200)


class FindMember(View):
    def get(self, request):
        li = list(map(dict, Member.objects.values()))
        return JsonResponse({"members": li}, status=200)
