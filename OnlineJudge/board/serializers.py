from utils.api import UsernameSerializer, serializers

from .models import Article, Comment


class Const:
    MAX_TITLE_LEN = 128
    MAX_CONTENT_LEN = 131072


class CreateArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=Const.MAX_TITLE_LEN)
    content = serializers.CharField(max_length=Const.MAX_CONTENT_LEN)
    problem = serializers.CharField(max_length=32, allow_blank=True, allow_null=True)


class RemoveArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ArticleSerializer(serializers.ModelSerializer):
    # TODO: Check User is NULL
    created_by = UsernameSerializer()

    class Meta:
        model = Article
        field = "__all__"


class ArticleListSerializer(ArticleSerializer):
    class Meta:
        model = Article
        exclude = ("content",)


class CreateCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField(max_length=Const.MAX_CONTENT_LEN)


class CommentSerializer(serializers.ModelSerializer):
    # TODO: Check User is NULL
    created_by = UsernameSerializer()

    class Meta:
        model = Comment
        field = "__all__"
