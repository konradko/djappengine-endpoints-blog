from django import forms

class ArticleForm(forms.Form):
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

class EditArticleForm(ArticleForm):
    delete = forms.BooleanField(required=False)