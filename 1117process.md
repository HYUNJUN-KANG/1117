#### 첫번째, django-admin startproject 이름





# App: Todos

1) 기본셋팅

 * 앱 생성 `python manage.py startapp todos`

 * settings에 app 등록

 * url 분리

    * server의 url

       * ```python
         from django.contrib import admin
         from django.urls import path, include
         urlpatterns = [
             path('admin/', admin.site.urls),
             path('todos/', include('todos.urls')),
         ]
         ```

    * todos의 url

       * ```python
         from django.urls import path
         
         from . import views
         
         app_name = 'todos'
         urlpatterns = [
             
         ]
         ```

2) modeling

* ```python
  from django.db import models
  
  class Todo(models.Model):
      title = models.CharField(max_length=200)
      created = models.BooleanField(default=False)
  ```

3) DRF 사용준비

* pip install djangorestframework
* settings.py에 installed_APP에 'rest_framework' 등록

4) Serializer (DRF를 통해 API server 만들 준비 끝)

* todos파일에 serializers.py 생성

* ```python
  from rest_framework import serializers
  from .models import Todo
  
  class TodoSerializer(serializers.ModelSerializer):
      class Meta:
          model = Todo
          fields = '__all__'
  ```



## todo_create_read

#### (urls 먼저 수정하고 views 수정 / get: Read , post: Create)

#### 1) todos의 urls.py

```python
from django.urls import path
from . import views

app_name = 'todos'
urlpatterns = [
    path('', views.todo_list_create),
]
```



#### 2) todos의 views.py

#### 	* Todo의 모든 list를 보여주는 R

#### 	* Todo를 생성할 수 있는 C

```python
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Todo
from .serializers import TodoSerializer

@api_view(['GET', 'POST'])
def todo_list_create(request):
    # GET: 모든 정보 조회
        # DB에서 모든 정보를 불러온다.
        # DRF를 사용해서 JSON으로 리턴한다.
        
    if request.method == 'GET':
        todos = Todo.objects.all()
        # data를 여러개 받아오므로 serializer에서 many=True 조건 넣어줌
        serializer = TodoSerializer(todos, many=True)
        # DRF를 가지고 리턴을 할 때는 Response 함수 사용
        return Response(serializer.data)
	
    # POST: 정보를 새롭게 생성
        # 받을 데이터를 검증한다 (validation 한다)
        # DB에 저장한다.
        # 저장된 정보를 JSON 형태로 리턴해준다.
        # 추가정보를 전달하고 싶을 땐 status를 추가한다.
        
    else:
        serializer = TodoSerializer(data=request.data)
        # 유효성검사에 실패했을 시, 안내성 JSON을 나타내기 위해 raise_exception=True
        if serializer.is_valid(raise_exception=True):
            # 검증에 성공하면 DB에 저장
            serializer.save(user=request.user)
            # created 됐음을 표시하기 위해서 status=status.HTTP_201_CREATED 넣어줌
            return Response(serializer.data, status=status.HTTP_201_CREATED)

```



#### 

## todo_update_delete

#### 1) todos의 urls.py의 path설정

```python
from django.urls import path

from . import views

app_name = 'todos'
urlpatterns = [
    path('', views.todo_create_read, name='todo_cr'),
    path('<int:todo_id>/', views.todo_update_delete, name='todo_ud'),
]
```

#### 2) views.py 설정

#### 	* PUT: return 수정된 data

#### 	* DELETE: return 삭제된 data의 id

```python
from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Todo
from .serializers import TodoSerializer


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
```





# Vue

* `vue create client`

  

#### 1) router 추가

`vue add router`

home과 about 관련된 것 지우기

#### router - index.js

```js
import Vue from 'vue'
import VueRouter from 'vue-router'
import TodoList from '@/views/TodoList'

Vue.use(VueRouter)

const routes = [
  {
    path: '/todos',
    name: 'TodoList',
    component: TodoList
  },
 
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
```



#### 2) HOME.vue, About.vue 삭제

#### 3) TodoList.vue, TodoCreate.vue, component 생성

#### * TodoList.vue

```vue
<template>
  <div>
    <ul>
      <li></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'TodoList',
  data: function () {
    return {
	  todos: [],
    }
  },
  methods: {
    getTodo: function () {

    }
  }
}
</script>

<style>

</style>
```



#### * TodoCreate.vue

```vue
<template>
  <div id="app">
    <div></div>
  </div>
</template>

<script>
export default {
  name: 'CreateTodo',
  data: function () {
    return {
      title: '',
    }
  },
  methods: {
    createTodo: function () {
  
    }
  }
}
</script>

<style>

</style>
```





### TodoCreate.vue 설정

`npm i axios`: axios 설치

#### 1) TodoCreate.vue

```vue
<template>
  <div>
    Todo Create
    <input type="text" v-model="inputData" @keydown.enter="createTodo">
    <button @click="createTodo">+</button>
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'TodoCreate',
  data: function () {
    return {
      inputData: '',
    }
  },
  methods: {
    createTodo: function () {
      const sendData = {
        title: this.inputData,
      }
      axios.post('http://127.0.0.1:8000/todos/', data)
        .then(res => {
          console.log(res.data)
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style>

</style>
```



### cors

`pip install django-cors-headers` : cors 설치

#### server의 settings.py

```py
INSTALLED_APPS = [
'corsheaders',
]

MIDDLEWARE = [
    # django cors middleware setting
    'corsheaders.middleware.CorsMiddleware',
]

# Access-Control-Allow-Origin: * 

# 특정 Origin만 선택적으로 허용
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]

# 모든 Origin 허용
# CORS_ORIGIN_ALLOW_ALL = True
```



#### TodoList.vue  설정

```vue
<template>
  <div>
    Todo List
    <ul>
      <li v-for="(todo, idx) in todos" :key="idx">{{ todo.title }}</li>
    </ul>
    
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TodoList',
  data: function () {
    return {
      todos: []
    }
  },
  methods: {
    getTodos: function () {
      axios.get('http://127.0.0.1:8000/todos/')
        .then(res => {
          console.log(res.data)
          this.todos = res.data
        })
        .catch(err => {
          console.error(err)
        })
    }
  },
  created: function () {
    this.getTodos() 
  },
  
  methods: {
    getTodo: function () {

    }
  }
}
</script>

<style>

</style>
```



#### create 시키면 input 창이 비어있도록 + todolist에 넘겨주기 위해 TodoCreate.vue 수정

```vue
<template>
  <div>
    Todo Create
    <input type="text" v-model="inputData" @keydown.enter="createTodo">
    <button @click="createTodo">+</button>
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'TodoCreate',
  data: function () {
    return {
      inputData: '',
    }
  },
  methods: {
    createTodo: function () {
      const sendData = {
        title: this.inputData,
      }
      axios.post('http://127.0.0.1:8000/todos/', sendData)
        .then(res => {
          console.log(res.data)
          // input data를 지워줘서 사용자에게 변화를 확인시켜줌
          this.inputData = ''
          // 할 일을 등록하게 되면 자동으로 todolist로 넘겨서 확인할 수 있게 함
          this.$router.push({name: 'TodoList'})
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style>

</style>
```



#### update, delete 설정

```vue
<template>
  <div>
    Todo List
    <ul>
      <li
      :class="{ completed: todo.completed}"
      v-for="(todo, idx) in todos" 
      :key="idx"
      >
        <span @click="updateComplete(todo)">{{ todo.title }}</span>
        <button @click="deleteTodo(todo)">DEL</button>
      </li>
    </ul>
    
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TodoList',
  data: function () {
    return {
      todos: []
    }
  },
  methods: {
    getTodos: function () {
      axios.get('http://127.0.0.1:8000/todos/')
        .then(res => {
          console.log(res.data)
          this.todos = res.data
        })
        .catch(err => {
          console.error(err)
        })
    },

    updateComplete (todo) {
     
      todo.completed = !todo.completed
      
      // template literal을 사용하려면 ` 을 사용해야한다.
      axios.put(`http://127.0.0.1:8000/todos/${todo.id}/`, todo)
        .then(res => {
          console.log(res.data)
          // todos에서 해당 아이템을 삭제
          const deleteIdx = this.todos.findIndex(todo => {
            return todo.id === res.data.id
          })
          // 해당 index에서 하나의 데이터를 삭제한다.
          this.todos.splice(deleteIdx, 1)
        })
        .catch(err => {
          console.error(err)
        })
    },

    deleteTodo (todo) {
      axios.delete(`http://127.0.0.1:8000/todos/${todo.id}`)
        .then(res => {
          console.log(res.data)
        })
        .catch(err => {
          console.error(err)
        })
    }
  },
  created: function () {
    this.getTodos() 
  },
  
  methods: {
    getTodo: function () {

    }
  }
}
</script>

<style>
  .completed {
    text-decoration: line-through;
    color: lightgray;
  }
</style>
```



# jwt

`pip install djangorestframework-jwt`





