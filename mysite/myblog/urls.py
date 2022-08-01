from django.urls import path
from myblog import views
from django.contrib.auth import authenticate,login,logout

app_name='myblog'



urlpatterns =[
    
    path('',views.PostListView.as_view(),name="post_list"),
    path('<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('post/new/',views.CreatePostView.as_view(),name='post_new'),
    path('post/<int:pk>/edit/',views.UpdatePostView.as_view(),name='post_edit'),
    path('post/<int:pk>/delete/',views.DeletePostView.as_view(),name='post_delete'),
    path('drafts/',views.DraftListView.as_view(),name='post_draft_list'),
    path('post/<int:pk>/publish/',views.post_publish,name='post_publish'),
    path('post/<int:pk>/comment/',views.add_comment_to_post,name='add_comment_to_post'),
    path('comment/<int:pk>/approve/',views.comment_approve,name='comment_approve'),
    path('comment/<int:pk>/remove/',views.comment_remove,name='comment_remove'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='user_login'),
    
    
    
    
]