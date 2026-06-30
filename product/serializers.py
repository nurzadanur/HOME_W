from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title description price category owner reviews rating'.split()
        depth = 1

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
    

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=255)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=255)
    description = serializers.CharField(required=False, default="No description")
    price = serializers.FloatField(min_value=0)
    category = serializers.IntegerField()

    def validate_category(self, category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=1)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product = serializers.IntegerField()

    def validate_product(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')
