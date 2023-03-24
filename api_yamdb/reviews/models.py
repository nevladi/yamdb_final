from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = (
    (USER, 'User'),
    (MODERATOR, 'Moderator'),
    (ADMIN, 'Admin'),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=255,
        unique=True,
    )
    firstname = models.CharField(
        'Фамилия',
        max_length=40,
        null=True,
        blank=True
    )
    lastname = models.CharField(
        'Имя',
        max_length=40,
        null=True,
        blank=True
    )
    bio = models.TextField('Биография',null=True, blank=True)
    role = models.TextField(
        default='user',
        choices=ROLES,
        blank=True
    )
    object = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        "Категория произведения",
        max_length=256,
        unique=True,
        help_text="Введите категорию произведения.",
    )
    slug = models.SlugField(
        "URL",
        unique=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        "Название жанра",
        max_length=256,
        unique=True,
        help_text="Введите название жанра",
    )
    slug = models.SlugField(
        "URL",
        unique=True,
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        "Название произведения",
        max_length=200,
        help_text="Введите название произведения",
    )
    year = models.PositiveSmallIntegerField(
        "Год выпуска",
        null=True,
        blank=True,
        help_text="Год выпуска",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="title",
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        through='GenreTitle'
    )
    description = models.TextField(blank=True, verbose_name='description')

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["name"]

    @property
    def rating(self):
        rating = self.reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return (
                round(rating)
                if isinstance(rating, int)
                else float(f'{rating:.2f}')
            )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="Жанр"
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение"
    )

    class Meta:
        verbose_name = "Произведение и жанр"
        verbose_name_plural = "Произведения и жанры"


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
        related_name='reviews'
    )
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Рейтинг произведений"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_review'
            )
        ]
        ordering = ("-pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзыв"

    def __str__(self):
        return f'{self.text}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
        related_name='comments'
    )
    text = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["pub_date"]

    def __str__(self):
        return f'{self.text}'
