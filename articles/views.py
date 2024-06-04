from django.db.models import Prefetch, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from django.db.models import Count, Avg, F, ExpressionWrapper, fields
from django.utils import timezone

from articles.filters import ArticleFilter
from articles.models.activities import Comment, Rating
from articles.models.articles import Article
from articles import serializers


class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

    def get_queryset(self):
        """Думается мне, что немного оптимизации с такой не простой структурой БД, не помешает"""
        queryset = self.queryset.select_related('author').prefetch_related(
            Prefetch('comments', queryset=Comment.objects.select_related('source')),
            Prefetch('ratings', queryset=Rating.objects.select_related('source')),
            'tags'
        )
        return queryset


class ArticleListStatsView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleListStatsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

    def get_queryset(self):
        current_date = timezone.now().date()

        queryset = self.queryset
        queryset = self._optimization_queryset(queryset)
        queryset = queryset.annotate(
            count_comments=Count('comments'),
            count_ratings=Count('ratings'),
            average_rating=Avg('ratings__rate'),
            author_age=ExpressionWrapper(
                current_date.year - F('author__dob__year') -
                ((current_date.month, current_date.day) < (F('author__dob__month'), F('author__dob__day'))),
                output_field=fields.IntegerField()
            ),
            author_age_in_publish=ExpressionWrapper(
                F('publish_date__year') - F('author__dob__year') -
                ((F('publish_date__month'), F('publish_date__day')) < (F('author__dob__month'), F('author__dob__day'))),
                output_field=fields.IntegerField()
            ),
            count_activities=Count('comments') + Count('ratings')
        )
        return queryset

    def _optimization_queryset(self, queryset: QuerySet) -> QuerySet:
        """Оптимизация queryset для уменьшения нагрузки на БД"""
        queryset = self.queryset.select_related('author').prefetch_related(
            Prefetch('comments', queryset=Comment.objects.select_related('source')),
            Prefetch('ratings', queryset=Rating.objects.select_related('source')),
            'tags'
        ).only(
            'id', 'title', 'text', 'publish_date', 'author__id', 'author__dob',
            'comments__id', 'ratings__id', 'ratings__rate',
            'comments__source__code', 'ratings__source__code',
        )
        return queryset
