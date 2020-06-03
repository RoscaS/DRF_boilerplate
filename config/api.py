from rest_framework import routers

from apps.articles.views import ArticleViewSet
from apps.articles.views import CategoryViewSet

from apps.users.views import UserViewSet


api = routers.DefaultRouter()
api.trailing_slash = '/?'

api.register(r'users', UserViewSet)
api.register(r'articles', ArticleViewSet)
api.register(r'categories', CategoryViewSet)
