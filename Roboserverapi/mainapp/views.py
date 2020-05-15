from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .models import RoboUser
from .serializers import RoboUserShowSerializer

'''
class RoboUserShowView(ListAPIView):
	queryset=RoboUser.objects.all()
	serializer_class=RoboUserShowSerializer
'''

	
class RoboUserShowView(APIView):
    def get(self, request):
        user = RoboUser.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = RoboUserShowSerializer(user, many=True)
        return Response({"user": serializer.data})
