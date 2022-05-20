from django.urls import path
from . import views

urlpatterns = [
    path('',views.IndexView.as_view(),name="IndexView"),
    path('plats/<str:categorie>/',views.PlatView.as_view(),name="PlatView"),
    path('search/',views.search,name="search"),
    path('ContactUs/',views.ContactView.as_view(),name="ContactView"),
    path('About/',views.AboutView.as_view(),name="AboutView"),
    path('Shopping-cart',views.ShoppingCartDetail.as_view(),name="cart"),
    path('detail/<str:plat_id>',views.PlatDetailView.as_view(),name="detail"),
    path('add-to-cart', views.addTocart.as_view(), name="add-to-cart"),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
]