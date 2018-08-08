from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response

SHOPPING_CAP = {
    1:{
        2:{
            'title': 'xxxx',
            'price':1,
            'price_list':[
                {'id': 11},
                {'id': 22},
                {'id': 33},
            ]
        },
        3: {},
        5: {},
    },
    2:{},
    3:{}
}

class ShoppingCarView(ViewSetMixin, APIView):
    def create(self, request, *args, **kwargs):
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
        return Response({'code': 11111})