from collections import OrderedDict

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from common.permissions import CanEdit, IsAnonymous, IsModerator, IsOwner
from common.validators import validate_age

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    CategoryValidateSerializer,
    ProductSerializer,
    ProductValidateSerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer,
    ReviewValidateSerializer,
)

PAGE_SIZE = 5


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("total", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )

    def get_page_size(self, request):
        return PAGE_SIZE


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = Category.objects.create(**serializer.validated_data)
        return Response(
            data=CategorySerializer(category).data,
            status=status.HTTP_201_CREATED,
        )


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.name = serializer.validated_data.get("name")
        category.save()

        return Response(data=CategorySerializer(category).data)


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.select_related("category", "owner").prefetch_related("reviews").all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [IsOwner | IsAnonymous | IsModerator]

    def get(self, request, *args, **kwargs):
        products = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(products)
        if page is not None:
            data = ProductWithReviewsSerializer(page, many=True).data
            return self.get_paginated_response(data)

        data = ProductWithReviewsSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        validate_age(request)

        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.create(
            title=serializer.validated_data.get("title"),
            description=serializer.validated_data.get("description"),
            price=serializer.validated_data.get("price"),
            category=serializer.validated_data.get("category"),
            owner=request.user,
        )

        return Response(
            data=ProductSerializer(product).data,
            status=status.HTTP_201_CREATED,
        )


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("category", "owner").prefetch_related("reviews").all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    permission_classes = [(IsOwner & CanEdit) | IsAnonymous | IsModerator]

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        data = ProductWithReviewsSerializer(product).data
        return Response(data=data)

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get("title")
        product.description = serializer.validated_data.get("description")
        product.price = serializer.validated_data.get("price")
        product.category = serializer.validated_data.get("category")
        product.save()

        return Response(data=ProductSerializer(product).data)


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review = Review.objects.create(
            text=serializer.validated_data.get("text"),
            stars=serializer.validated_data.get("stars"),
            product=serializer.validated_data.get("product"),
        )

        return Response(
            data=ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED,
        )


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get("text")
        review.stars = serializer.validated_data.get("stars")
        review.product = serializer.validated_data.get("product")
        review.save()

        return Response(data=ReviewSerializer(review).data)