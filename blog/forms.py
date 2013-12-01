from django import forms

from blog.models import Article


class BaseArticleForm(forms.Form):
    title = forms.CharField(
        required=True,
        error_messages={'required': "Title can't be empty"},
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter title',
        })
    )

    content = forms.CharField(
        required=True,
        error_messages={'required': "Content can't be empty"},
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter article',
        })
    )

class NewArticleForm(BaseArticleForm):

    def clean_title(self):
        data = self.cleaned_data['title']
        # Check that title is unique, needed for slug uniqueness
        if Article.query(Article.title == data).get():
            raise forms.ValidationError("You already have article with that title")
        return data

class EditArticleForm(BaseArticleForm):
    delete = forms.BooleanField(required=False)