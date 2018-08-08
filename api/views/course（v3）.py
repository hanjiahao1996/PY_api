import json
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from rest_framework.pagination import PageNumberPagination

from api import models
from api.serlalizers.course import CourseSerializer,CourseModelSerializer
from api.utils.response import BaseResponse

from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,ListModelMixin
from rest_framework.renderers import JSONRenderer

class CoursesView(ListModelMixin, GenericViewSet):
    queryset = models.Course.objects.all()

    def list(self, request, *args, **kwargs):
        course_list = models.Course.objects.all()
        ser = CourseModelSerializer(instance=course_list, many=True)

        return Response(ser.data)