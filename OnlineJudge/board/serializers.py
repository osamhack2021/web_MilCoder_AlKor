from utils.api import UsernameSerializer, serializers

from .models import Article


class Const:
    MAX_TITLE_LEN = 128
    MAX_CONTENT_LEN = 131072


class CreateArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=Const.MAX_TITLE_LEN)
    content = serializers.CharField(max_length=Const.MAX_CONTENT_LEN)


class EditArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=Const.MAX_TITLE_LEN)
    content = serializers.CharField(max_length=Const.MAX_CONTENT_LEN)


class ArticleAdminSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = Article
        fields = "__all__"


class ArticleSerializer(ArticleAdminSerializer):
    pass
