from django.contrib.auth import logout
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ArticleFilter, VideoFilter
from .serializers import *


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = '__all__'



class CategoryRetrieveAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ArticleFilter
    ordering_fields = '__all__'
    search_fields = ('title', 'intro')

    def get_queryset(self):
        return self.queryset.filter(publish=True).order_by('-id')

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='publish',
                in_=openapi.IN_QUERY,
                description="Filter articles by publish status",
                type=openapi.TYPE_BOOLEAN,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TopArticlesListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # def get_queryset(self):
    #     top_news = self.queryset.filter(news_of_the_day=True).order_by('-id')
    #     other_news = self.queryset.filter(news_of_the_day=False).order_by('-views')
    #     return list(top_news) + list(other_news)[:40 - len(top_news)]

    def get_queryset(self):
        # last_10_days = timezone.now() - timedelta(days=10)
        # top_news = self.queryset.filter(news_of_the_day=True, created_at__gte=last_10_days).order_by('-id')
        # other_news = self.queryset.filter(news_of_the_day=False, created_at__gte=last_10_days).order_by('-views')
        # return list(top_news) + list(other_news)[:40 - len(top_news)]
        return self.queryset.filter(news_of_the_day=True)



class ArticleRetrieveAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.views += 1
        instance.save(update_fields=['views'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class VideoListAPIView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = VideoFilter
    ordering_fields = '__all__'
    search_fields = ('title', 'intro')


class VideoRetrieveAPIView(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.views += 1
        instance.save(update_fields=['views'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AdListAPIView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdRetrieveAPIView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class StaffListAPIView(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffPhotoListAPIView(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffPhotoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        photos = [staff.photo.url for staff in queryset if staff.photo]
        return Response(photos)

class CredentialsApiView(APIView):
    def get(self, request):
        credential = Credentials.objects.last()
        serializer = CredentialsSerializer(credential)
        return Response(serializer.data)


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        response = redirect('/')
        response.delete_cookie("Authorization")
        return response