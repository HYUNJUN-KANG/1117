from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Todo
from .serializers import TodoSerializer


@api_view(['GET', 'POST'])
def todo_create_read(request):
    # GET: 모든 정보 조회
        # DB에서 모든 정보를 불러온다.
        # DRF를 사용해서 JSON으로 리턴한다.
    if request.method == 'GET':
        print('GET!!!!!!@@!@!@!@@!')
        todos = Todo.objects.all()
        # data를 여러개 받아오므로 serializer에서 many=True 조건 넣어줌
        serializer = TodoSerializer(todos, many=True)
        # DRF를 가지고 리턴을 할 때는 Response 함수 사용
        return Response(serializer.data)

    # POST: 정보를 새롭게 생성
        # 받을 데이터를 검증한다 (validation 한다)
        # DB에 저장한다.
        # 저장된 정보를 JSON 형태로 리턴해준다.
    else:
        serializer = TodoSerializer(data=request.data)
        # 유효성검사에 실패했을 시, 안내성 JSON을 나타내기 위해 raise_exception=True
        if serializer.is_valid(raise_exception=True):
            # 검증에 성공하면 DB에 저장
            serializer.save(user=request.user)
            # created 됐음을 표시하기 위해서 status=status.HTTP_201_CREATED 넣어줌
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def todo_update_delete(request, todo_id):
    
    # PUT: 데이터를 수정
        # 수정되어야 하는 데이터를 DB에서 찾아온다.
        # serializer를 이용해서 수정할 데이터와 수정 값을 담아둔다.
        # serializer를 유효성 검사를 한다.
        # 유효성 검사를 통과하면 DB에 저장하고, 저장된 값을 리턴한다.

    # update와 delete 모두에서 todo를 찾아올 수 있도록 if 문 밖에서 정의
    todo = get_object_or_404(Todo, id=todo_id)
    
    if not request.user.todos.filter(pk=todo_pk).exists():
        return Reponse({'detail': '권한이 없습니다.'})

    if request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # DELETE: 데이터를 삭제
        # DB에서 삭제할 데이터를 가져온다.
        # 삭제한다.
        # 삭제된 데이터의 id를 리턴한다.

    else:  # if request.method == 'DELETE':
        todo.delete()
        context = {
            'id': todo_id,
        }
        return Response(context)