from account.decorators import login_required
from utils.api import APIView, validate_serializer
from utils.shortcuts import check_is_id

from problem.models import Problem
from ..models import Article, Comment
from ..serializers import ArticleSerializer, ArticleListSerializer
from ..serializers import CreateArticleSerializer, RemoveArticleSerializer
from ..serializers import CommentSerializer
from ..serializers import CreateCommentSerializer, RemoveCommentSerializer

class BoardAPI(APIView):
    def get(self, request):
        """
        get an article via id, or get a search result
        """
        id = request.GET.get("id")
        if not id:
            # no id -> do search
            return self._search(request)
        elif not check_is_id(id):
            return self.error("Invalid parameter id")
        try:
            article = Article.objects.get(id=int(id))
        except Article.DoesNotExist:
            return self.error("Article does not exist")
        data = ArticleSerializer(article).data
        return self.success(data)

    def _search(self, request):
        """
        get a list of articles
        """
        articles = Article.objects.all()

        problem_id = request.GET.get("problem_id", "").strip()
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")
            articles = articles.filter(problem=problem)
        
        keyword = request.GET.get("keyword", "").strip()
        if keyword:  
            articles = articles.filter(title__icontians=keyword)
        return self.success(self.paginate_data(request, articles, ArticleListSerializer))


    @validate_serializer(CreateArticleSerializer)
    @login_required
    def post(self, request):
        """
        write new article
        """
        data = request.data
        article = Article.objects.create(
            title=data["title"],
            content=data["content"],
            problem_id=data.get("problem_id", None),
            created_by=request.user,
        )
        return self.success(ArticleSerializer(article).data)

    @validate_serializer(RemoveArticleSerializer)
    @login_required
    def delete(self, request):
        """
        remove an article
        """
        data = request.data
        id = data["id"]
        if not check_is_id(id):
            return self.error("Invalid parameter, id is required")
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return self.error("Article does not exist")

        user = request.user
        if user.is_admin_role() or user.id == article.created_by_id:
            article.delete()
            return self.success({"id": id})

        return self.error("No permission to remove article")


class BoardCommentAPI(APIView):
    def get(self, request):
        """
        get a list of comments using article id
        """
        article_id = request.GET.get("article_id")
        if not article_id or not check_is_id(article_id):
            return self.error("Invalid parameter, article_id is required")
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return self.error("Article does not exist")

        comments = article.comment_set.all()
        return self.success(self.paginate_data(request, comments, CommentSerializer))

    @validate_serializer(CreateCommentSerializer)
    @login_required
    def post(self, request):
        """
        Write a new comment
        """
        data = request.data
        article_id = data["article_id"]
        if not article_id or not check_is_id(article_id):
            return self.error("Invalid parameter, article_id is required")
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return self.error("Article does not exist")

        comment = Comment.objects.create(
            content=data["content"],
            created_by=request.user,
            article=article,
        )
        return self.success(CommentSerializer(comment).data)

    @validate_serializer(RemoveCommentSerializer)
    @login_required
    def delete(self, request):
        """
        remove a comment
        """
        data = request.data
        id = data["id"]
        if not check_is_id(id):
            return self.error("Invalid parameter, id is required")
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return self.error("Comment does not exist")

        user = request.user
        if user.is_admin_role() or user.id == comment.created_by_id:
            comment.delete()
            return self.success({"id": id})

        return self.error("No permission to remove comment")
