from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *


readers = Group.objects.get(name='readers')
librarians = Group.objects.get(name='librarians')
administrators = Group.objects.get(name='administrators')

def sign_up(request):
    form = SignUp()
    if request.method == "POST":
        form = SignUp(data=request.POST)
        if form.is_valid():
            new_user = User(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                Телефон=form.cleaned_data["Телефон"]
            )
            new_user.set_password(
                form.cleaned_data["password"]
            )
            new_user.save()
            new_user.groups.add(readers)
            new_user.save()
            login(request, new_user)
            return redirect("home")
        else:
            return render(request, "sign_up.html", {"form": form})
    return render(request, "sign_up.html", {"form": form})


def sign_in(request):
    form = SignIn()
    if request.method == "POST":
        form = SignIn(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect("home")
            if user is None:
                users = User.objects.all()
                logins = []
                passwords = []
                i = 0
                while i < len(users):
                    logins.append(users[i].username)
                    passwords.append(users[i].password)
                    i = i + 1
                del i
                if form.cleaned_data["username"] not in logins:
                    message = "Логин не зарегистрирован"
                else:
                    message = "Пароль неверный"
                return render(request, "sign_in.html", {"form": form, "message": message})
    return render(request, "sign_in.html", {"form": form})


@login_required
def sign_out(request):
    logout(request)
    return redirect("sign_in")


@login_required
def home(request):
    user = request.user
    access_level = None
    if user.has_perm("libraryapp.view_user") and not user.has_perm("libraryapp.change_user"):
        access_level = "Библиотекарь"
    elif user.has_perm("libraryapp.change_user"):
        access_level = "Администратор"
    else:
        access_level = "Читатель"
    taken_books_1 = TakenBook.objects.all()
    taken_books_2 = []
    i = 0
    while i < len(taken_books_1):
        if taken_books_1[i].user.username == user.username:
            taken_books_2.append(taken_books_1[i])
        i = i + 1
    del i
    form = TakeBook()
    if request.method == "POST":
        form = TakeBook(request.POST)
        if form.is_valid():
            b_1 = form.cleaned_data["book"]
            u_1 = form.cleaned_data["user"]
            b_2 = Book.objects.get(title=b_1)
            u_2 = User.objects.get(username=u_1)
            taken_book = TakenBook(
                book=b_2,
                user=u_2
            )
            taken_book.save()
            return redirect("home")
        else:
            return render(request, "home.html", {"self": user, "taken_books": taken_books_2, "access_level": access_level, "form": form})
    return render(request, "home.html", {"self": user, "taken_books": taken_books_2, "access_level": access_level, "form": form})


@login_required
def change_data(request):
    form = ChangeSelfData()
    if request.method == "POST":
        form = ChangeSelfData(data=request.POST)
        users = User.objects.all()
        i = 0
        usernames = []
        passwords = []
        while i < len(users):
            usernames.append(users[i].username)
            passwords.append(users[i].password)
            i = i + 1
        del i
        if form.is_valid() and (request.POST.get("password") not in passwords or request.POST.get("password") == request.user.password) and (request.POST.get("username") not in usernames or request.POST.get("username") == "username"):
            user = request.user
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.username = form.cleaned_data["username"]
            user.email = form.cleaned_data["email"]
            user.Телефон = form.cleaned_data["Телефон"]
            user.set_password(
                form.cleaned_data["password"]
            )
            user.save()
            login(request, user)
            return redirect("home")
        elif form.is_valid() and ((request.POST.get("password") in passwords and request.POST.get("password") != request.user.password) or (request.POST.get("username") in usernames and request.POST.get("username") != request.user.username)):
            message = "логин или пароль уже существует"
            return render(request, "change_data.html", {"form": form, "message": message})
        else:
            message = "некорректные данные"
            return render(request, "change_data.html", {"form": form, "message": message})
    return render(request, "change_data.html", {"form": form})


@login_required
@permission_required(perm="libraryapp.view_book", raise_exception=True)
def books(request):
    books = Book.objects.all()
    genre_list = ["Action", "Adventure", "Comedy", "Detective", "Fantasy", "Historical", "Historical fiction", "Horror",
                  "Romance", "Satire", "Science fiction", "Cyberpunk", "Speculative", "Thriller", "Other"]
    user = request.user
    access_level = None
    if user.has_perm("libraryapp.view_user") and not user.has_perm("libraryapp.change_user"):
        access_level = "Библиотекарь"
    if user.has_perm("libraryapp.change_user"):
        access_level = "Администратор"
    else:
        access_level = "Читатель"
    return render(request, "books.html", {"books": books, "genre_list": genre_list, "access_level": access_level})



@login_required
@permission_required(perm="libraryapp.view_user", raise_exception=True)
def users(request):
    users = User.objects.all()
    user = request.user
    access_level = None
    if user.has_perm("libraryapp.view_user") and not user.has_perm("libraryapp.change_user"):
        access_level = "Библиотекарь"
    if user.has_perm("libraryapp.change_user"):
        access_level = "Администратор"
    else:
        access_level = "Читатель"
    return render(request, "users.html", {"users": users, "access_level": access_level})


@login_required
@permission_required(perm="libraryapp.view_book", raise_exception=True)
def book(request, id):
    book = Book.objects.get(id=id)
    tags = book.tags.all()
    all_comments = CommentsAndRating.objects.all()[::-1]
    useful_comments = []
    i = 0
    while i < len(all_comments):
        if all_comments[i].book.id == id:
            useful_comments.append(all_comments[i])
        i = i + 1
    user = request.user
    href = False
    if user.has_perm("libraryapp.change_user"):
        href = True
    rating = 0
    quantity = 0
    for comment in useful_comments:
        rating = rating + comment.rating
        quantity = quantity + 1
    if quantity != 0:
        rating = round(rating / quantity, 1)
    else:
        rating = 0
    form = AddComment()
    if request.method == "POST":
        form = AddComment(request.POST)
        if form.is_valid():
            comment = CommentsAndRating(
                rating=form.cleaned_data["rating"],
                comment=form.cleaned_data["comment"],
                book=book,
                user=user,
            )
            comment.save()
            return redirect("book", book.id)
    return render(request, "book.html", {"book": book, "tags": tags, "rating": rating, "comments": useful_comments, "form": form, "href": href})


@login_required
@permission_required(perm="libraryapp.view_user", raise_exception=True)
def user(request, id):
    user = User.objects.get(id=id)
    self = request.user
    taken_books_1 = TakenBook.objects.all()
    taken_books_2 = []
    i = 0
    while i < len(taken_books_1):
        if taken_books_1[i].user.username == user.username:
            taken_books_2.append(taken_books_1[i])
        i = i + 1
    del i
    user_access_level = None
    self_access_level = None
    if user.has_perm("libraryapp.view_user") and not user.has_perm("libraryapp.change_user"):
        user_access_level = "Библиотекарь"
    elif user.has_perm("libraryapp.change_user"):
        user_access_level = "Администратор"
    else:
        user_access_level = "Читатель"
    if self.has_perm("libraryapp.view_user") and not self.has_perm("libraryapp.change_user"):
        self_access_level = "Библиотекарь"
    elif self.has_perm("libraryapp.change_user"):
        self_access_level = "Администратор"
    else:
        self_access_level = "Читатель"
    return render(request, "user.html", {"user": user, "taken_books": taken_books_2, "user_access_level": user_access_level, "self_access_level": self_access_level})


@login_required
@permission_required(perm="libraryapp.add_book", raise_exception=True)
def add_book(request):
    form = AddBook()
    if request.method == "POST":
        form = AddBook(request.POST)
        if form.is_valid():
            form.save()
            return redirect("books")
        else:
            return render(request, "add_book.html", {"form": form})
    return render(request, "add_book.html", {"form": form})


@login_required
@permission_required(perm="libraryapp.change_book", raise_exception=True)
def change_book(request):
    form = ChangeBook()
    if request.method == "POST":
        form = ChangeBook(request.POST)
        if form.is_valid():
            id = form.cleaned_data["id"]
            book = Book.objects.get(id=id)
            book.title = form.cleaned_data["title"]
            book.text = form.cleaned_data["text"]
            book.author = form.cleaned_data["author"]
            book.year_of_publication = form.cleaned_data["year_of_publication"]
            book.genre = form.cleaned_data["genre"]
            book.tags = form.cleaned_data["tags"]
            book.quantity = form.cleaned_data["quantity"]
            book.save()
            return redirect("books")
        else:
            return render(request, "change_book.html", {"form": form})
    return render(request, "change_book.html", {"form": form})


@login_required
@permission_required(perm="libraryapp.delete_book", raise_exception=True)
def delete_book(request):
    form = DeleteBook()
    if request.method == "POST":
        form = DeleteBook(request.POST)
        if form.is_valid():
            id = form.cleaned_data["id"]
            book = Book.objects.get(id=id)
            book.delete()
            return redirect("books")
        else:
            return render(request, "delete_book.html", {"form": form})
    return render(request, "delete_book.html", {"form": form})


@login_required
@permission_required(perm="libraryapp.view_book", raise_exception=True)
def return_book(request, id, id_2, id_3):
    book = Book.objects.get(id=id)
    book.quantity = book.quantity + 1
    book.save()
    taken_book = TakenBook.objects.get(id=id_2)
    taken_book.delete()
    return redirect("user", id_3)


@login_required
def delete_comment(request, book_id, id):
    book = Book.objects.get(id=book_id)
    comment = CommentsAndRating.objects.get(id=id)
    comment.delete()
    return redirect("book", book.id)


@login_required
@permission_required(perm="libraryapp.add_user", raise_exception=True)
def add_user(request):
    form = AddUser()
    if request.method == "POST":
        form = AddUser(request.POST)
        if form.is_valid():
            user = User(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                email=form.cleaned_data["email"],
                Телефон=form.cleaned_data["Телефон"]
            )
            if form.cleaned_data["access_level"] == "librarian":
                user.groups.set([librarians, ])
            if form.cleaned_data["access_level"] == "administrator":
                user.groups.set([administrators, ])
            if form.cleaned_data["access_level"] == "reader":
                user.groups.set([readers, ])
            user.save()
            return redirect("users")
        else:
            return render(request, "add_user.html", {"form": form})
    return render(request, "add_user.html", {"form": form})


@login_required
@permission_required(perm="libraryapp.change_user", raise_exception=True)
def change_user(request):
    form = ChangeUser()
    if request.method == "POST":
        form = ChangeUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data["old_username"]
            user = User.objects.get(username=username)
            if form.cleaned_data["access_level"] == "librarian":
                user.groups.set([librarians, ])
            if form.cleaned_data["access_level"] == "reader":
                user.groups.set([readers, ])
            return redirect("users")
        else:
            return render(request, "change_user.html", {"form": form})
    return render(request, "change_user.html", {"form": form})


@login_required
@permission_required(perm="libraryapp.delete_user", raise_exception=True)
def delete_user(request):
    form = DeleteUser()
    if request.method == "POST":
        form = DeleteUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user = User.objects.get(username=username)
            user.delete()
            return redirect("users")
        else:
            return render(request, "add_user.html", {"form": form})
    return render(request, "add_user.html", {"form": form})
