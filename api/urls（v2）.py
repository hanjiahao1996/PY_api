from django.conf.urls import url
from api.views import course



urlpatterns = [
    url(r'courses/$',course.CoursesView.as_view({'get': 'list', 'post': 'create'})),
    url(r'courses/(?P<pk>\d+)/$',course.CoursesView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]