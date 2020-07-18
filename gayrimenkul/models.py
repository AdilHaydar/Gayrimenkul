from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

# Create your models here.
def upload_to(instance,filename):
    return '%s/%s/%s'%('gayrimenkul',instance.slug,filename)
    
age_list = (
    ("0-1","0-1"),
    ("2-5","2-5"),
    ("6-10","6-10"),
    ("11-15","11-15"),
    ("16-20","16-20"),
    ("21-25","21-25"),
    ("+25","+25")
)


esya_list = (
    ("Evet","Evet"),
    ("Hayır","Hayır"),
    ("Kısmen","Kısmen"),
)

kullanim_list = (
    ("Uygun","Uygun"),
    ("Ufak Tadilat Gerekiyor","Ufak Tadilat Gerekiyor"),
    ("Tadilat Gerekiyor","Tadilat Gerekiyor"),
    ("Değil","Değil")
)
site_list = (
    ("Evet","Evet"),
    ("Hayır","Hayır")
)
class Post(models.Model):
    seller = models.ForeignKey('user.User',blank=False,null=False,verbose_name="İlan Sahibi",on_delete=models.CASCADE)
    mkare = models.CharField(max_length=10,verbose_name = "Metre Kare")
    title = models.CharField(max_length=120,blank=False,verbose_name="Başlık",help_text="Başlık Giriniz.")
    slug = models.SlugField(max_length=122,default='',unique=True,null=False,verbose_name='Slug Alanı',editable=False)
    price = models.FloatField(blank=False,verbose_name="Fiyat")
    il = models.CharField(max_length=20,verbose_name="İl")
    ilce = models.CharField(max_length=50,verbose_name="İlçe")
    mahalle = models.CharField(max_length=70,verbose_name="Mahalle")
    emlak_tipi = models.CharField(max_length=30,verbose_name = "Emlak Tipi")
    oda_sayisi = models.CharField(max_length=10,verbose_name = "Oda Sayısı")
    bina_yasi = models.CharField(max_length=6,choices=age_list,verbose_name = "Bina Yaşı")
    kat_sayisi = models.CharField(max_length=5,verbose_name = "Kat Sayısı")
    isitma = models.CharField(max_length=50,verbose_name = "Isıtma")
    esyali = models.CharField(max_length=10,choices = esya_list,verbose_name = "Eşyalı")
    kullanim_durumu = models.CharField(max_length=30,choices=kullanim_list,verbose_name = "Kullanım Durumu")
    site_icerisinde = models.CharField(max_length=10,choices=site_list,verbose_name="Site İçerisinde")
    content = RichTextField(verbose_name="Detay")
    img = models.ImageField(blank=False,verbose_name='Thumbnail',upload_to=upload_to)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s"%(self.title)

    def get_image_or_default(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
        return ''

    def save(self, *args, **kwargs):
        if self.slug == '':
            index=1
            new_slug = slugify(self.title)
            self.slug=self.unique_slug(new_slug=new_slug,orjinal_slug=new_slug,index=index)
        super(Post, self).save(*args,**kwargs)
    
    def get_slug(self):
        return self.slug
    
    def unique_slug(self,new_slug,orjinal_slug,index):
        if Post.objects.filter(slug=new_slug):
            new_slug = '%s-%s'%(orjinal_slug,index)
            index += 1
            return self.unique_slug(new_slug=new_slug,orjinal_slug=orjinal_slug,index=index)
        return new_slug
    
    class Meta:
        verbose_name = 'Gönderilerim'
        verbose_name_plural = 'Gönderilerim'
        ordering = ['-created_date']

def get_image_filename(instance, filename):
    slug = instance.post.get_slug()
    return "%s/%s/%s" % ('gayrimenkul',slug, filename)  

class PostImage(models.Model):
    post = models.ForeignKey(Post, default= None, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True ,verbose_name='Fotoğraf',upload_to=get_image_filename)

    class Meta:
        verbose_name = 'Fotoğraflar'
        verbose_name_plural = 'Fotoğraflar'
        ordering = ['-post']
