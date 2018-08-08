from django.conf.urls import url
from api.views import course

urlpatterns = [
    url(r'courses/', course.CoursesView.as_view()),
    url(r'courses/(?P<pk>\d+)/$', course.CourseDetaiView.as_view())
]