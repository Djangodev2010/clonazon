from django.urls import path
from .views import HomeView, ProductDetail, SearchView, RegisterView, CategoryProductView, ReviewWriteView, AllReviewView, ProfileView, LoginView, AddToCartView
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

#Create your urls here
app_name = 'e_commerce'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('product-detail/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('search-product/', SearchView.as_view(), name='search_product'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login-out/', LogoutView.as_view(), name='logout'),
    path('c/<str:cate_name>', CategoryProductView.as_view(), name='cate_view'),
    path('<str:slug>/write-review/', ReviewWriteView.as_view(), name='write_review'),
    path('<int:id>/all-reviews', AllReviewView.as_view(), name='all_reviews'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('<str:name>/add-to-cart', AddToCartView.as_view(), name='add_to_cart')
]
