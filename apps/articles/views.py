from rest_framework import viewsets

from apps.articles.serializers import ArticleSerializer, CategorySerializer
from apps.articles.models import Article, Category


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        return super().create(request, args, kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



