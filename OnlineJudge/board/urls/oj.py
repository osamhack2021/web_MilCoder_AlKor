from django.conf.urls import url

from ..views.oj import BoardAPI, BoardListAPI

urlpatterns = [
    url(r"^board/?$", BoardAPI.as_view(), name="board_api"),
    url(r"^board/list/?$", BoardListAPI.as_view(), name="board_list_api"),
]

