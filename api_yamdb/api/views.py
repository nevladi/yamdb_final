from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import AnonReadOnly, IsAdmin, IsAdminModeratorOwnerOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleReadSerializer, TitleRecSerializer,
                          TokenSerializer, UserSerializer)


class SignupAPIView(APIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User,
                                 username=data['username'],
                                 password=data['password'])
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'token': str(refresh.access_token)
            }, status=status.HTTP_200_OK
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        instance = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        serializer = self.get_serializer(
            instance,
            request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=instance.role, partial=True)
        return Response(serializer.data)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin | AnonReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data["name"], slug=self.request.data["slug"]
        )

    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        serializer.delete()


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin | AnonReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data["name"], slug=self.request.data["slug"]
        )

    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Genre, slug=self.kwargs.get("slug"))
        serializer.delete()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdmin | AnonReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleRecSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
