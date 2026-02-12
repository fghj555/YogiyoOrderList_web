from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from django.urls import path
from django.views.generic import TemplateView
from django.http import FileResponse
import os

from orders.views import OrderViewSet
from restaurants.views import RestaurantViewSet, MenuViewSet
from restaurants.views import TagViewSet
from reviews.views import OwnerCommentCreateViewSet, ReviewListViewSet, ReviewDestroyViewSet
from reviews.views import ReviewCreateViewSet, OwnerCommentViewSet
from users.views import UserViewSet, BookmarkListViewSet, BookmarkViewSet

def home_view(request):
    """HTML 파일을 직접 서빙"""
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'index.html')
    return FileResponse(open(template_path, 'rb'), content_type='text/html')

router = SimpleRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewDestroyViewSet)
router.register(r'bookmarks', BookmarkListViewSet)
router.register(r'bookmarks', BookmarkViewSet)
router.register(r'tags', TagViewSet)
router.register(r'comments', OwnerCommentViewSet)

""" review create """
review_router = routers.NestedSimpleRouter(router, r'orders', lookup='order')
review_router.register(r'reviews', ReviewCreateViewSet, basename='order_review')
""" review list """
review_list_router = routers.NestedSimpleRouter(router, r'restaurants', lookup='restaurant')
review_list_router.register(r'reviews', ReviewListViewSet, basename='restaurant_review')
"""review_comment create"""
review_comment_router = routers.NestedSimpleRouter(router, r'reviews', lookup='review')
review_comment_router.register(r'comments', OwnerCommentCreateViewSet, basename='review_comment')

urlpatterns = [
    path('', home_view, name='home'),
] + router.urls + review_router.urls + review_list_router.urls + review_comment_router.urls
