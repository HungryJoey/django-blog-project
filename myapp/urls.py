from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.BlogPostViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.post_list, name='post_list'),
    path('blog/post/<int:pk>/', views.post_detail, name='post_detail'),
    path('blog/post/new/', views.post_new, name='post_new'),
    path('blog/post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('blog/post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-posts/', views.my_blog_posts, name='my_posts'),
    path('profile/', views.profile, name='profile'),
    path('api/', include(router.urls)),
    path('spa/', views.spa_view, name='spa'),
    path('submissions/', views.view_submissions, name='view_submissions'),
]