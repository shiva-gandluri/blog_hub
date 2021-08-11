from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        #widgets for assigning specific stylings using css classes
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':"Title",'class': 'form-control input-lg posttitle'}),
            'text': forms.Textarea(attrs={'data-placeholder':"Start Typing...", 'rows': '0', 'cols': '0', 'class': 'medium-editor-textarea editable post-card post-card-body postcontent border-0 bg-white'},  ),
        }
        labels = {
            "title": "",
            "text": ""
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            #'author': forms.TextInput(attrs={'class': 'textinputclass','value': 'request.user'}),
            'text': forms.Textarea(attrs={'data-placeholder':"Start Typing...", 'class': 'medium-editor-textarea editable comment-card comment-card-body postcontent border-0 bg-white'},),
        }
        labels = {
            "text": ""
        }
