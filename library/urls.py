from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import (AuthorListView,AuthorCreateView,AuthorRetrieveView,AuthorUpdateView,AuthorDestroyView,
                    CategoryListAPIView,CategoryCreateAPIView,CategoryRetrieveAPIView,CategoryUpdateAPIView,CategoryDeleteAPIView,
                    BookViewSet,BorrowListView,BorrowCreateView,BorrowRetrieveView,BorrowUpdateView,BorrowDestroyView)



router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet,basename='book')

urlpatterns=[
    path('authors', AuthorListView.as_view(), name='author_list'),
    path('authors/create', AuthorCreateView.as_view(), name='author_create'),
    path('authors/<int:pk>', AuthorRetrieveView.as_view(), name='author_detail'),
    path('authors/<int:pk>/update', AuthorUpdateView.as_view(), name='author_update'),
    path('authors/<int:pk>/delete', AuthorDestroyView.as_view(), name='author_delete'),

    path('categories', CategoryListAPIView.as_view(), name='category_list'),
    path('categories/create', CategoryCreateAPIView.as_view(), name='category_create'),
    path('categories/<int:pk>', CategoryRetrieveAPIView.as_view(), name='category_detail'),
    path('categories/<int:pk>/update', CategoryUpdateAPIView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete', CategoryDeleteAPIView.as_view(), name='category_delete'),

    path('', include(router.urls)),

    path('borrows', BorrowListView.as_view(), name='borrow_list'),
    path('borrows/create', BorrowCreateView.as_view(), name='borrow_create'),
    path('borrows/<int:pk>', BorrowRetrieveView.as_view(), name='borrow_detail'),
    path('borrows/<int:pk>/update', BorrowUpdateView.as_view(), name='borrow_update'),
    path('borrows/<int:pk>/delete', BorrowDestroyView.as_view(), name='borrow_delete'),

]