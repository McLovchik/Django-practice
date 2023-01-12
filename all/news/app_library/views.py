from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class AuthorsList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Представление для получения списка авторов и создания нового, а также фильтрации по имени"""
    serializer_class = AuthorSerializer

    def get_queryset(self):
        queryset = Author.objects.all()
        item_first_name = self.request.query_params.get('first_name')
        if item_first_name:
            queryset = queryset.filter(first_name=item_first_name)
        return queryset

    def get(self, request):
        return self.list(request)

    def post(self, request, format=None):
        return self.create(request)


class AuthorDetail(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """Представление для получения детальной информации об авторе, а также для его редактирования и удаления"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BooksList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Представление для получения списка книг и фильтрации по параметрам"""
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        item_name = self.request.query_params.get('name')
        item_author = self.request.query_params.get('author')
        item_number_of_pages = self.request.query_params.get('number_of_pages')
        item_number_of_pages_gt = self.request.query_params.get('number_of_pages__gt')
        item_number_of_pages_lt = self.request.query_params.get('number_of_pages__lt')
        if item_name:
            queryset = queryset.filter(name=item_name)
        elif item_author:
            author = Author.objects.filter(first_name=item_author).first()
            queryset = queryset.filter(author=author)
        elif item_number_of_pages:
            queryset = queryset.filter(number_of_pages=item_number_of_pages)
        elif item_number_of_pages_gt:
            queryset = queryset.filter(number_of_pages__gt=item_number_of_pages_gt)
        elif item_number_of_pages_lt:
            queryset = queryset.filter(number_of_pages__lt=item_number_of_pages_lt)
        return queryset

    def get(self, request):
        return self.list(request)

    def post(self, request, format=None):
        return self.create(request)


class BookDetail(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """Представление для получения детальной информации о книге, а также для её редактирования и удаления"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
