from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeview, name='homeview'),
    path('login/', views.loginview, name='loginview'),
    path('logout/', views.logoutview, name='logoutview'),
    path('signup/', views.signupview, name='signupview'),
    path('blog/', views.PostListView.as_view(), name='postlistview'),
    path('blog/<int:pk>/', views.PostDetailView.as_view(), name='postdetailview'),
    path('blog/add-post/', views.AddPostView.as_view(), name='addpostview'),
    path('blog/<int:pk>/update/', views.UpdatePostView.as_view(), name='updatePostView'),
    path('blog/<int:pk>/delete/', views.DeletePostView.as_view(), name='deletePostView'),
    path('blog/<int:pk>/add_comment_like/', views.add_comment_like, name='add_comment_like'),
    
]