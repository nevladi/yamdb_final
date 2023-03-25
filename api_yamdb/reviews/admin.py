from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = ('username',
                            'email',
                            'role',
                            'bio',)


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = ('username',
                    'email',
                    'role',
                    'bio',
                    'first_name',
                    'last_name',)


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title
        exclude = ('id',
                   'rating',
                   'description',
                   'genre',)
        import_id_fields = ('name',
                            'year',
                            'category',)


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    list_display = ('name',
                    'year',
                    'category',)


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        import_id_fields = ('id',
                            'name',
                            'slug',)


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    list_display = ('name',
                    'slug',)


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        import_id_fields = ('id',
                            'name',
                            'slug',)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = ('name',
                    'slug',)


class GenreTitleResource(resources.ModelResource):
    class Meta:
        model = GenreTitle
        fields = ('id',
                  'title',
                  'genre',)


@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = [GenreTitleResource]
    list_display = ('title',
                    'genre',)


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment
        import_id_fields = ('id',
                            'review',
                            'text',
                            'author',
                            'pub_date',)


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    resource_classes = [CommentResource]
    list_display = ('review',
                    'text',
                    'author',
                    'pub_date')


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        import_id_fields = ('id',
                            'title',
                            'text',
                            'author',
                            'score',
                            'pub_date',)


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]
    list_display = ('title',
                    'text',
                    'author',
                    'score',
                    'pub_date',)
