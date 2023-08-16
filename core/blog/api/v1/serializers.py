from rest_framework import serializers
from blog.models import Post, Category

# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=250)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name',]


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField()

    # getting date from other tables with their attributes.
    '''
    category = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=Category.objects.all()
    )
    '''
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'snippet' ,'content', 'status', 'category', 'created_date', 'updated_date','relative_url','absolute_url']
        # read_only_fields = ['content',]

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj)
    
    # To separate showing attributes from List and detail
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr["category"] = CategorySerializer(instance.category).data
        repr.pop('snippet', None)
        return repr




