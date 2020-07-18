from django import forms
from .models import Post, PostImage

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title','img','price','il','ilce','mahalle','content','mkare','emlak_tipi','oda_sayisi','bina_yasi','kat_sayisi','isitma','esyali','kullanim_durumu','site_icerisinde']
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['rows'] = 4
        self.fields['content'].widget.attrs['cols'] = 50

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.isdigit():
            raise forms.ValidationError('Lütfen Sadece Rakamlardan Oluşan Bir Başlık Girmeyiniz.')

        if '@' in title:
            raise forms.ValidationError('Lütfen @ İşareti Girmeyiniz.')
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if content.isdigit():
            raise forms.ValidationError('Lütfen Sadece Rakamlardan Oluşan Bir İçerik Oluşturmayınız.')
        if len(content) < 20:
            raise forms.ValidationError('Lütfen 20 Karakterden Fazla Karakter Giriniz.')
        return content

class PostImageForm(forms.ModelForm):
    image = forms.ImageField(label = 'Fotoğraf')
    class Meta:
        model = PostImage
        fields = ('image',)