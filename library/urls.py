from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import (AuthorListView,AuthorCreateView,AuthorRetrieveView,AuthorUpdateView,AuthorDestroyView,
                    CategoryListAPIView,CategoryCreateAPIView,CategoryRetrieveAPIView,CategoryUpdateAPIView,CategoryDeleteAPIView,
                    BookViewSet,BorrowListView,BorrowCreateView,BorrowRetrieveView,BorrowUpdateView,BorrowDestroyView)

router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet)

urlpatterns=[
    path('authors', AuthorListView.as_view()),
    path('authors/create', AuthorCreateView.as_view()),
    path('authors/<int:pk>', AuthorRetrieveView.as_view()),
    path('authors/<int:pk>/update', AuthorUpdateView.as_view()),
    path('authors/<int:pk>/delete', AuthorDestroyView.as_view()),

    path('categories', CategoryListAPIView.as_view()),
    path('categories/create', CategoryCreateAPIView.as_view()),
    path('categories/<int:pk>', CategoryRetrieveAPIView.as_view()),
    path('categories/<int:pk>/update', CategoryUpdateAPIView.as_view()),
    path('categories/<int:pk>/delete', CategoryDeleteAPIView.as_view()),

    path('', include(router.urls)),

    path('borrows', BorrowListView.as_view()),
    path('borrows/create', BorrowCreateView.as_view()),
    path('borrows/<int:pk>', BorrowRetrieveView.as_view()),
    path('borrows/<int:pk>/update', BorrowUpdateView.as_view()),
    path('borrows/<int:pk>/delete', BorrowDestroyView.as_view()),

]