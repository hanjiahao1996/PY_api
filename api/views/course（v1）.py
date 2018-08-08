from django.shortcuts import HttpResponse,render
from rest_framework.views import APIView
from rest_framework.versioning import URLPathVersioning
import json
from api import models
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from api.models import CourseCategory,CourseSubCategory,\
    DegreeCourse,Teacher,Scholarship,Course,CourseDetail,OftenAskedQuestion,\
    CourseOutline,CourseChapter,CourseSection,CourseSection,CourseSection
from rest_framework.response import Response
from api import models
from api.serlalizers.course import CourseSerializer, CourseModelSerializer, DegreeCourseSerializer, DegreepriceSerializer
from api.utils.response import BaseResponse
from rest_framework.pagination import PageNumberPagination


class CoursesView(APIView):
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            queryset = models.Course.objects.all()
            page = PageNumberPagination()
            course_list = page.paginate_queryset(queryset, request, self)
            ser = CourseModelSerializer(instance=course_list, many=True)
            ret.data = ser.data
        except Exception as e :
            ret.code = 500
            ret.error = '获取数据失败'

        return Response(ret.dict)

    def post(self, request, *args, **kwargs):
        """
        增加
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

class CourseDetaiView(APIView):
    def get(self, request, pk, *args, **kwargs):
        response = {'code': 1000, 'data': None, 'error': None}
        try:
            course = models.Course.objects.get(id=pk)
            ser = CourseModelSerializer(instance=course)
            response['data'] = ser.data
        except Exception as e:
            response['code'] = 500
            response['error'] = '获取数据失败'
        return Response(response)

    def put(self, request, *args, **kwargs):
        """
        修改
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def delete(self, request, pk, *args, **kwargs):
        """
        删除
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """

class DegreeCourseView(APIView):
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try :
            degree = models.DegreeCourse.objects.all()
            deg = DegreeCourseSerializer(instance=degree,many=True)
            ret.data = deg.data
        except Exception as e:
            # ret = 500
            ret.error = '获取数据失败'
        print(ret.dict)
        return Response(ret.dict)

class DegreeView(APIView):
    def get(self, requet,*args, **kwargs):
        ret = BaseResponse()
        # try :
        degreeprice = models.DegreeCourse.objects.all()
        dege = DegreepriceSerializer(instance=degreeprice, many=True)
        ret.data = dege.data
        # except Exception as e:
        #     # ret = 500
        #     ret.error = '获取数据失败'
        print(ret.dict)
        return Response(ret.dict)
