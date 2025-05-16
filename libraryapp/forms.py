from django import forms
from .models import *


class SignUp(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password", "email", "phone")


class SignIn(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)


class ChangeSelfData(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11)


class AddBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "text", "author", "year_of_publication", "genre", "tags", "quantity")


class ChangeBook(forms.Form):
    id = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=1000000)
    author = forms.CharField(max_length=1000)
    year_of_publication = forms.DateField()


class DeleteBook(forms.Form):
    id = forms.CharField(max_length=100)


class AddUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password", "email", "phone")


class ChangeUser(forms.Form):
    old_username = forms.CharField(max_length=64)
    access_level = forms.CharField(max_length=13)


class DeleteUser(forms.Form):
    username = forms.CharField(max_length=64)


class TakeBook(forms.Form):
    book = forms.CharField(max_length=64)
    user = forms.CharField(max_length=64)


class AddComment(forms.ModelForm):
    class Meta:
        model = CommentsAndRating
        fields = ("rating", "comment")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["rating"] != 1 and cleaned_data["rating"] != 2 and cleaned_data["rating"] != 3 and cleaned_data["rating"] != 4 and cleaned_data["rating"] != 5:
            self.add_error("rating", "rating must be between 1 and 5")
        return cleaned_data


class DeleteComment(forms.Form):
    id = forms.IntegerField()
