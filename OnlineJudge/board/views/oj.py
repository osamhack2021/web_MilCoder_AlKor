from account.decorators import login_required
from utils.api import APIView, validate_serializer
from utils.shortcuts import check_is_id

from ..models import Article
from ..serializers import ArticleSerializer, CreateArticleSerializer


class BoardArticleAPI(APIView):
    def get(self, request):
        id = request.GET.get("id")
        if not id or not check_is_id(id):
            return self.error("Invalid parameter, id is required")
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return self.error("Article does not exist")
        data = ContestSerializer(contest).data
        return self.success(data)


class BoardListAPI(APIView):
    def get(self, request):
        articles = Article.objects.all()
        return self.success(self.paginate_data(request, article, ArticleSerializer))


class BoardWriteAPI(APIView):
    @validate_serializer(CreateArticleSerializer)
    @login_required
    def post(self, request):
        data = request.data
        article = Article.objects.create(
            title=data["title"],
            content=data["content"],
            created_by=request.user,
        )
        return self.success({"id": article.id})

