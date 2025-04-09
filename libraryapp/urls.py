from django.urls import path
from .views import *


urlpatterns = [
    path("", sign_in, name="sign_in"),
    path("sign_up/", sign_up, name="sign_up"),
    path("sign_out/", sign_out, name="sign_out"),
    path("home/", home, name="home"),
    path("home/change_data/", change_data, name="change_data"),
    path("books/", books, name="books"),
    path("books/book/<int:id>/", book, name="book"),
    path("books/add_book/", add_book, name="add_book"),
    path("books/change_book/", change_book, name="change_book"),
    path("books/delete_book/", delete_book, name="delete_book"),
    path("books/return_book/<int:id>/<int:id_2>/<int:id_3>/", return_book, name="return_book"),
    path("books/delete_comment/<int:book_id>/<int:id>/", delete_comment, name="delete_comment"),
    path("users/", users, name="users"),
    path("users/user/<int:id>/", user, name="user"),
    path("users/add_user/", add_user, name="add_user"),
    path("users/change_user/", change_user, name="change_user"),
    path("users/delete_user/", delete_user, name="delete_user")
]
