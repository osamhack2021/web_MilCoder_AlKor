from utils.api import UsernameSerializer, SimpleProblemSerializer, serializers

from .models import Article, Comment


class Const:
    MAX_TITLE_LEN = 128
    MAX_CONTENT_LEN = 131072


class CreateArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=Const.MAX_TITLE_LEN)
    content = serializers.CharField(max_length=Const.MAX_CONTENT_LEN)
    problem_id = serializers.CharField(max_length=32, allow_blank=True, allow_null=True)


class RemoveArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class EditArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=Const.MAX_TITLE_LEN)
    content = serializers.CharField(max_length=Const.MAX_CONTENT_LEN)


class ArticleSerializer(serializers.ModelSerializer):
    # TODO: Check User is NULL
    created_by = UsernameSerializer()

    class Meta:
        model = Article
        fields = "__all__"


class ArticleListSerializer(ArticleSerializer):
    created_by = UsernameSerializer()
    problem = SimpleProblemSerializer()
    class Meta:
        model = Article
        exclude = ("content",)


class CreateCommentSerializer(serializers.Serializer):
    article_id = serializers.IntegerField()
    content = serializers.CharField(max_length=Const.MAX_CONTENT_LEN)


class RemoveCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class CommentSerializer(serializers.ModelSerializer):
    # TODO: Check User is NULL
    created_by = UsernameSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
