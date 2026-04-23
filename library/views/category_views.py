from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from library.models import Category
from library.serializers.category_serializer import CategorySerializer
from library.permissions import IsAdminOrReadOnly
from library.filters.category_filter import CategoryFilter
from library.utils import success_response, error_response

from django_filters.rest_framework import DjangoFilterBackend



class CategoryBaseAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None


class CategoryListAPIView(CategoryBaseAPIView):
    filterset_class = CategoryFilter
    search_fields = ('name',)
    ordering_fields = ('name', 'id',)


    def get(self, request):
        categories = Category.objects.all()
        filter_backend = DjangoFilterBackend()
        categories = filter_backend.filter_queryset(request,categories,self,)


        search_backend = SearchFilter()
        categories = search_backend.filter_queryset(request,categories,self,)

        ordering_backend = OrderingFilter()
        categories = ordering_backend.filter_queryset(request,categories,self,)

        paginator = PageNumberPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



class CategoryCreateAPIView(CategoryBaseAPIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryRetrieveAPIView(CategoryBaseAPIView):
    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class CategoryUpdateAPIView(CategoryBaseAPIView):
    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteAPIView(CategoryBaseAPIView):
    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return success_response( None, {"deleted": "Category deleted successfully"}, status.HTTP_204_NO_CONTENT,)