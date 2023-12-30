from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product, Article
from shop.serializers import CategorySerializer, ProductSerializer, ArticleSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        # Resolve category_id if present
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        # Resolve force_inactive if present
        force_inactive = self.request.GET.get('force_inactive')
        if force_inactive is None:
            queryset = queryset.filter(active=True)

        return queryset


class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()

        # Resolve product_id if present
        product_id = self.request.GET.get('category_id')
        if product_id is not None:
            queryset = queryset.filter(product=product_id)

        # Resolve force_inactive if present
        force_inactive = self.request.GET.get('force_inactive')
        if force_inactive is None:
            queryset = queryset.filter(active=True)

        return queryset


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()

        # Resolve force_inactive if present
        force_inactive = self.request.GET.get('force_inactive')
        if force_inactive is None:
            queryset = queryset.filter(active=True)
        return queryset
