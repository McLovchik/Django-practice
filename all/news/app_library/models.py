from django.db import models
from django.core.validators import MinValueValidator


class Author(models.Model):
    """Модель автора."""
    first_name = models.CharField(max_length=32, verbose_name='имя')
    last_name = models.CharField(max_length=64, verbose_name='фамилия')
    year_of_birth = models.DateTimeField(verbose_name='дата рождения')

    def __str__(self):
        return self.first_name


class Book(models.Model):
    """Модель книги."""
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='автор')
    name = models.CharField(max_length=32, verbose_name='название')
    isbn = models.CharField(max_length=16, unique=True, verbose_name='международный стандартный книжный номер')
    year_of_issue = models.DateTimeField(verbose_name='год выпуска')
    number_of_pages = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='количество страниц')
