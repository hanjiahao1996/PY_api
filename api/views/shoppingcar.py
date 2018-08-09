from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
import json
import redis
from django.conf import settings
from rest_framework.parsers import JSONParser,FormParser
from api import models
from api.utils.response import BaseResponse

CONN = redis.Redis(host='192.168.11.147',port=6379)
USER_ID = 1

class ShoppingCarView(ViewSetMixin, APIView):
    def list(self, request, *args, **kwargs):
        """
        查看购物车信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret = {'code': 10000, 'data':None, 'error': None}
        try:
            shopping_car_course_list = []
            pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, '*',)
            user_key_list = CONN.keys(pattern)
            for key in user_key_list:
                temp = {
                    'id': CONN.hget(key, 'id').decode('utf-8'),
                    'name': CONN.hget(key, 'name').decode('utf-8'),
                    'img': CONN.hget(key, 'img').decode('utf-8'),
                    'default_price_id': CONN.hget(key, 'default_price_id'),
                    'price_policy_id': json.loads(CONN.hget(key, 'price_policy_dict'))
                }
                shopping_car_course_list.append(temp)
            ret['date'] = shopping_car_course_list
        except Exception as e:
            ret['code'] = 10005
            ret['error'] = '获取购物车数据失败'

        return Response(ret)
    def create(self,request, *args, **kwargs):
        """
        加入购物车
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        1. 接受用户选中的课程ID和价格策略ID
        2. 判断合法性
            - 课程是否存在？
            - 价格策略是否合法？
        3. 把商品和价格策略信息放入购物车 SHOPPING_CAR

        注意：用户ID=1
        """
        # 1.接受用户选中的课程ID和价格策略ID
        """
            相关问题：
                a. 如果让你编写一个API程序，你需要先做什么？
                    - 业务需求
                    - 统一数据传输格式
                    - 表结构设计
                    - 程序开发
                b. django restful framework的解析器的parser_classes的作用？
                    根据请求中Content-Type请求头的值，选择指定解析对请求体中的数据进行解析。
                    如：
                        请求头中含有Content-type: application/json 则内部使用的是JSONParser，JSONParser可以自动去请求体request.body中
                        获取请求数据，然后进行 字节转字符串、json.loads反序列化；

                c. 支持多个解析器（一般只是使用JSONParser即可）

        """
        course_id = request.data.get('courseid')
        policy_id = request.data.get('policyid')
        # 2. 判断合法性
        #   - 课程是否存在？
        #   - 价格策略是否合法？

        # 2.1 课程是否存在？
        course = models.Course.objects.filter(id=course_id).first()
        if not course:
            return Response({'code': 10001, 'error': '课程不存在'})
        #2.2 价格策略是否合法?
        price_policy_queryset = course.price_policy.all()
        price_policy_dict = {}
        for item in price_policy_queryset:
            temp = {
                'id': item.id,
                'price': item.price,
                'valid_period': item.valid_period,
                'valid_period_display': item.get_valid_period_display()
            }
            price_policy_dict[item.id] = temp
        if policy_id not in price_policy_dict:
            return Response({'code': 10002, 'error': '价格策略别乱改'})
        # 3. 把商品和价格策略信息放入购物车 SHOPPING_CAR
        """
        购物车中要放：
            课程ID
            课程名称
            课程图片
            默认选中的价格策略
            所有价格策略
        {
            1:{
                2:{
                    课程ID
                    课程名称
                    课程图片
                    1
                    所有价格策略
                },
                5:{
                    课程ID
                    课程名称
                    课程图片
                    默认选中的价格策略
                    所有价格策略
                }
            },
            3:{
                2:{
                    课程ID
                    课程名称
                    课程图片
                    默认选中的价格策略
                    所有价格策略
                },
                5:{
                    课程ID
                    课程名称
                    课程图片
                    默认选中的价格策略
                    所有价格策略
                }
            }
        }

        {
            shopping_car_1_1:{
                id:课程ID
                name:课程名称
                img:课程图片
                defaut:默认选中的价格策略
                price_list:所有价格策略
            },
            shopping_car_1_2:{
                id:课程ID
                name:课程名称
                img:课程图片
                defaut:默认选中的价格策略
                price_list:所有价格策略
            },
            shopping_car_1_3:{
                id:课程ID
                name:课程名称
                img:课程图片
                defaut:默认选中的价格策略
                price_list:所有价格策略
            },
            shopping_car_2_3:{
                id:课程ID
                name:课程名称
                img:课程图片
                defaut:默认选中的价格策略
                price_list:所有价格策略
            }
        }

        """
        pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, '*',)
        keys = CONN.keys(pattern)
        if keys and len(keys) >= 1000:
            return Response({'code': 10009, 'error': '购物车已满，请结算后再购买'})

        key = settings.lUFFY_SHOPPING_CAP %(USER_ID, course_id),
        CONN.hset(key, 'id', course_id)
        CONN.hset(key, 'name', course.name)
        CONN.hset(key, 'img', course.course_img)
        CONN.hset(key, 'default_price_id', policy_id)
        CONN.hset(key, 'price_policy_dict', json.dumps(price_policy_dict))

        return Response({'code':10000, 'data': '购买成功'})
    def destory(self, requesst, *args, **kwargs):
        """
        删除购物车中的某个课程
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = BaseResponse()
        try:
            courseid = requesst.GET.get('courseid')
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, courseid,)

            CONN.delete(key)
            response.data = '删除成功'

        except Exception as e:
            response.code = 10006
            response.error = '删除失败'
        return Response(response.dict)

    def update(self, request, *args, **kwargs):
        """
         修改用户选中的价格策略
         :param request:
         :param args:
         :param kwargs:
         :return:
         """
        """
        1. 获取课程ID、要修改的价格策略ID
        2. 校验合法性（去redis中）
        """
        response = BaseResponse()
        try:
            course_id = request.data.get('courseid')
            policy_id = str(request.data.get('policyid')) if request.data.get('policyid') else None

            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id,)

            if not CONN.exists(key):
                response.code = 10007
                response.error = '课程不存在'
                return Response(response.dict)

            price_policy_dict = json.loads(CONN.hget(key, 'price_policy_dict'))
            if policy_id not in price_policy_dict:
                response.code = 10008
                response.error = '价格策略不存在'
                return Response(response.dict)

            CONN.hset(key, 'default_price_id', policy_id)
            CONN.expire(key, 20 * 60)
            response.data = '修改成功'
        except Exception as e:
            response.code = 10009
            response.error = '修改失败'

        return Response(response.dict)
# SHOPPING_CAP = {
#     1:{
#         2:{
#             'title': 'xxxx',
#             'price':1,
#             'price_list':[
#                 {'id': 11},
#                 {'id': 22},
#                 {'id': 33},
#             ]
#         },
#         3: {},
#         5: {},
#     },
#     2:{},
#     3:{}
# }
#
# class ShoppingCarView(ViewSetMixin, APIView):
#     def create(self, request, *args, **kwargs):
#         """
#         加入购物车
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         """
#         1. 接受用户选中的课程ID和价格策略ID
#         2. 判断合法性
#             - 课程是否存在？
#             - 价格策略是否合法？
#         3. 把商品和价格策略信息放入购物车 SHOPPING_CAR
#
#         注意：用户ID=1
#         """
#         return Response({'code': 11111})