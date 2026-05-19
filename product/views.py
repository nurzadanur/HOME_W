from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer,
    CategoryValidateSerializer,
    ProductValidateSerializer,
    ReviewValidateSerializer,
)


class CategoryListAPIView(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryValidateSerializer

    def get(self, request):
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        name = serializer.validated_data.get('name')

        category = Category.objects.create(name=name)
        return Response(
            status=status.HTTP_201_CREATED,
            data=CategorySerializer(category).data
        )


class CategoryDetailAPIView(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryValidateSerializer

    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def get(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = CategorySerializer(category).data
        return Response(data=data)

    def delete(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=CategorySerializer(category).data
        )


class ProductListAPIView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductValidateSerializer

    def get(self, request):
        products = Product.objects.prefetch_related('reviews').all()
        data = ProductWithReviewsSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id,
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductWithReviewsSerializer(product).data
        )


class ProductDetailAPIView(GenericAPIView):
    queryset = Product.objects.all() 
    serializer_class = ProductValidateSerializer

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = ProductWithReviewsSerializer(product).data
        return Response(data=data)

    def delete(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductWithReviewsSerializer(product).data
        )


class ReviewListAPIView(GenericAPIView):
    queryset = Review.objects.all() 
    serializer_class = ReviewValidateSerializer

    def get(self, request):
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')

        review = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id,
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewSerializer(review).data
        )


class ReviewDetailAPIView(GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewValidateSerializer

    def get_object(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return None

    def get(self, request, id):
        review = self.get_object(id)
        if not review:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = ReviewSerializer(review).data
        return Response(data=data)

    def delete(self, request, id):
        review = self.get_object(id)
        if not review:
            return Response(status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        review = self.get_object(id)
        if not review:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewSerializer(review).data
        )