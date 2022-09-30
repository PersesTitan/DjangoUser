import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from blog.models import Blog
from user.models import Member
from user.views import ID_REPOSITORY


# 쿠키에 저장된 멤버 가져오기
def get_member(request):
    user_id = ID_REPOSITORY.get(request.COOKIES.get('id'))
    if user_id is None:
        return redirect("login")
    # Member 값 리턴
    return get_object_or_404(Member, pk=user_id)


# Create your views here.
# title, content
def make_board(board):
    return {"title": board.title, "content": board.content, "vis": board.vis}


# blog-create
@method_decorator(csrf_exempt, name='dispatch')
class Create(View):
    def post(self, request):
        # user.views 에 존재하는 ID_REPOSITORY 불러옴
        member = get_member(request)
        if type(member) != Member:
            return member

        data = json.loads(request.body)
        title = data["title"]
        content = data["content"]
        Blog(
            title=title,
            content=content,
            member=member
        ).save()
        return JsonResponse({"title": title, "content": content}, status=201)


class Find(View):
    # +) 검색 로직
    def get(self, request):
        li = list(map(dict, Blog.objects.values()))
        return JsonResponse({"blog": li}, status=200)


# 1개 찾기 OR 특정 게시판 편집
# /blogs/<id>/
@method_decorator(csrf_exempt, name='dispatch')
class FindOne(View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        return JsonResponse({blog.id: make_board(blog)}, status=200)

    # 편집
    def patch(self, request, blog_id):
        # user.views 에 존재하는 ID_REPOSITORY 불러옴
        member = get_member(request)
        if type(member) != Member:
            return member
        blog = Blog.objects.get(pk=blog_id)
        # Blog 가져오기
        if blog.member == member:
            data = dict(json.loads(request.body))
            title = data.get("title")
            content = data.get("content")
            # 정보 업데이트
            if title is not None:
                blog.title = title
            if content is not None:
                blog.content = content
            blog.save()
            return JsonResponse({"title": title, "content": content}, status=200)
        else:
            return JsonResponse({"error": "수정할 수 없는 계정 입니다."}, status=403)

    # 보이지 않게 처리
    def delete(self, request, blog_id):
        member = get_member(request)
        if type(member) != Member:
            return member
        blog = Blog.objects.get(pk=blog_id)
        if blog.member == member:
            blog.vis = False
            blog.save()
        return JsonResponse({"message": "삭제가 완료되었습니다."}, status=200)
