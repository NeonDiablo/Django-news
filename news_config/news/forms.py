from django import forms
from captcha.fields import CaptchaField
from .models import Post, Comment


class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, 
                    widget=forms.TextInput({'class':'user_name'}))
    password = forms.CharField(max_length=40, 
                    widget=forms.TextInput({'class':'user_password',
                                            'type':'password'}))
    captcha = CaptchaField()



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=25, 
                    widget=forms.TextInput({'class':'user_name'}))
                    
    password1 = forms.CharField(max_length=25, label='Password',
                    widget=forms.TextInput({'class':'user_password', 
                                            'type':'password'}))


    password2 = forms.CharField(max_length=25, label='Again password',
                    widget=forms.TextInput({'class':'user_password',
                                            'type':'password'}))

    email = forms.EmailField(max_length=25,
                    widget=forms.EmailInput({'class':'email'}))
    
    captcha = CaptchaField()

    
class CreateForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['category','title', 'text']
        
        widgets = {
            'category': forms.Select(attrs={'class':'category'}),
            'title': forms.TextInput(attrs={'class':'title'}),
            'text' : forms.Textarea(attrs={'class':'text'}),
        }

class ChangeForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['category','title', 'text']
        
        widgets = {
            'category': forms.Select(attrs={'class':'category'}),
            'title': forms.Textarea(attrs={'class':'title','cols':'30', 'rows':'5'}),
            'text' : forms.Textarea(attrs={'class':'text', 'cols':'90', 'rows':'20' }),
        }


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form'
            field.widget.attrs['cols'] = 90
            field.widget.attrs['rows'] = 2



class AvatarForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput({'class':'image'}))
