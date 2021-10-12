from django.conf.urls import url

from ..views.oj import BoardArticleAPI
from ..views.oj import BoardListAPI
from ..views.oj import BoardWriteAPI, BoardRemoveAPI

urlpatterns = [
    url(r"^board/?$", BoardArticleAPI.as_view(), name="board_article_api"),
    url(r"^board/list/?$", BoardListAPI.as_view(), name="board_list_api"),
#    url(r"^board/write/?$", BoardWriteAPI.as_view(), name="board_write_api"),
#    url(r"^board/remove/?$", BoardRemoveAPI.as_view(), name="board_remove_api"),
]
