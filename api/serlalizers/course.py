from rest_framework import serializers
from api import models
class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class CourseModelSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display')
    hours = serializers.CharField(source='coursedetail.hours')
    course_slogan = serializers.CharField(source='coursedatail.course_slogan')

    recommend_courses = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['id', 'name', 'level_name', 'hours', 'course_slogan', 'recommend_courses']

    def get_recommend_courses(self, row):
        recommend_list = row.coursedetail.recommend_courses.all()
        return [{'id': item.id, 'name': item.name} for item in recommend_list]


class DegreeCourseSerializer(serializers.ModelSerializer):
    degreename = serializers.CharField(source='name')
    teachername = serializers.SerializerMethodField()

    class Meta:
        model = models.DegreeCourse
        fields = ['id', 'degreename', 'teachername']

    def get_teachername(self,row):
        techername_list = row.teachers.all()

        return [{'name': item.name} for item in techername_list]



class DegreepriceSerializer(serializers.ModelSerializer):
     degreenmingzi = serializers.CharField(source='name')
     degreenprice = serializers.SerializerMethodField()


     class Meta:
         model = models.DegreeCourse
         fields = ['id', 'degreenmingzi', 'degreenprice']

     def get_degreenprice(self, row):
         price_list = row.scholarship_set.all()

         return [{ 'value': item.value} for item in price_list]
         