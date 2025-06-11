from django.urls import path
from  myapp import views
urlpatterns = [
    path('',views.home, name = 'home'),
    path('about/',views.about, name = 'about'),
    path('add/', views.add_book, name='add_book'),
    path('register/', views.register, name='register'),  # <-- Add this
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),

]
