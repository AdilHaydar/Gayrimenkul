import django_filters
from gayrimenkul.models import Post
from user.models import User
from django_filters import DateRangeFilter, NumberFilter, CharFilter,DateFromToRangeFilter, BooleanFilter,Filter

class PostFilter(django_filters.FilterSet):
    start_created_date = DateRangeFilter(field_name = "created_date", lookup_expr="gte")
    #end_created_date = DateRangeFilter(field_name = "created_date", lookup_expr="lte")
    start_price = NumberFilter(field_name='price',lookup_expr="gte")
    end_price = NumberFilter(field_name='price',lookup_expr="lte")
    title = CharFilter(field_name = 'title',lookup_expr='icontains')
    il = CharFilter(field_name = 'il',lookup_expr='icontains')
    ilce = CharFilter(field_name = 'ilce',lookup_expr='icontains')
    mahalle = CharFilter(field_name = 'mahalle',lookup_expr='icontains')
    
    class Meta:
        model = Post
        fields = ['title','price','il','ilce','mahalle','mkare','created_date']
        exclude = ['created_date','price','mkare','title','il','ilce','mahalle']

class UserFilter(django_filters.FilterSet):
    username=Filter(field_name='username',lookup_expr='icontains')
    admin = BooleanFilter(field_name='admin')
    active = BooleanFilter(field_name='active')
    staff = BooleanFilter(field_name='staff')
    timestamp = DateRangeFilter(field_name='timestamp',lookup_expr="gte",label = "Bu Tarihten Sonraki")
    class Meta:
        model = User
        fields = ['username','admin','staff','active','timestamp']
        exclude = ['username','admin','staff','active','timestamp']
