from django.urls import path,include
from .views import user_login
from .views import dashboard,register,edit,user_list,user_detail,user_follow
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('edit/',edit,name='edit'),
    path('user/<username>',user_detail,name='user_detail'),
    path('users/',user_list,name='user_list'),
    path('users/follow',user_follow,name='user_follow')


]
# url(r'^users/$', views.user_list, name='user_list'),
# url(r'^users/follow/$', views.user_follow, name='user_follow'),
# url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail')