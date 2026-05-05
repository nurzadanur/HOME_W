from rest_framework import serializers
from .models import Category, Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title price reviews rating'.split()

    def get_rating(self, product):
        reviews = product.reviews.all()
        if not reviews:
            return None
        return round(sum(r.stars for r in reviews) / len(reviews), 1)


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, category):
        return category.products_count()