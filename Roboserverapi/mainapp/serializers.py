from rest_framework import serializers
from .models import RoboUser

class RoboUserShowSerializer(serializers.ModelSerializer):
	class Meta:
		model=RoboUser
		fields=[
			'username',
			'userFingerprintId',
			'location',
			'firstname',
			'lastname',
		]