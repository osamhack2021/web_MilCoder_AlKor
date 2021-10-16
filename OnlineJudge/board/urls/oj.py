from django.conf.urls import url

from ..views.oj import BoardAPI
from ..views.oj import BoardCommentAPI

urlpatterns = [
    url(r"^board/?$", BoardAPI.as_view(), name="board_api"),
    url(r"^board/comment/?$", BoardCommentAPI.as_view(), name="board_comment_api")
]
