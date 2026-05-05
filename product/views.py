from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductWithReviewsSerializer


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    data = CategorySerializer(categories, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_detail(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = CategorySerializer(category, many=False).data
    return Response(data=data)


@api_view(['GET'])
def product_list_with_reviews(request):
    products = Product.objects.prefetch_related('reviews').all()
    data = ProductWithReviewsSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    from .serializers import ReviewSerializer
    data = ReviewSerializer(reviews, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    from .serializers import ReviewSerializer
    data = ReviewSerializer(review, many=False).data
    return Response(data=data)