from django import forms
from markdown import markdown

class ArticleForm(forms.Form):
    title = forms.CharField(
        required=True,
        error_messages={'required': "Title can't be empty"},
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter title',
            'class': "pure-input-1-2",
        })
    )

    content = forms.CharField(
        required=True,
        error_messages={'required': "Content can't be empty"},
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter article',
            'rows': 15,
            'class': "pure-input-1-2",
        })
    )

    def clean_content(self):
        data = self.cleaned_data['content']
        if "[HTML_REMOVED]" in markdown(data, safe_mode=True):
            raise forms.ValidationError("You can't have HTML in content, use markdown syntax instead")
        return data


class EditArticleForm(ArticleForm):
    delete = forms.BooleanField(required=False)