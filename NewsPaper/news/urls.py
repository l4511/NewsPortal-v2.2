from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, Search, Subscribe


urlpatterns = [
   path('', PostList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('create/<int:pk>', PostUpdate.as_view(), name='post_update'),
   path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
   path('search/', Search.as_view()),
   path('subscribe/', Subscribe.as_view(), name='subscribe'),
   ]
