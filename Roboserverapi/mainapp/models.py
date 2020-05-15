from django.db import models

# Create your models here.
class Location(models.Model):
	#LocationName=models.CharField(max_length=100)
	PositionX=models.IntegerField()
	PositionY=models.IntegerField()

	def __str__(self):
		return str(self.id)

class RoboUser(models.Model):
	username=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	userFingerprintId=models.IntegerField()
	location=models.OneToOneField(Location,on_delete=models.CASCADE,related_name='location')
	firstname=models.CharField(max_length=100)
	lastname=models.CharField(max_length=100)
	emailid=models.EmailField(max_length=100,blank=True)
	mobileno=models.IntegerField()

	def __str__(self):
		return self.username

class Admin(models.Model):
	username=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	firstname=models.CharField(max_length=100)
	lastname=models.CharField(max_length=100)
	emailid=models.EmailField(max_length=100,blank=True)
	mobileno=models.IntegerField()
	user=models.ManyToManyField(RoboUser,related_name='user')




class Robot(models.Model):
	roboId=models.CharField(max_length=100)
	roboStatus=models.CharField(max_length=100)
	roboPhase=models.CharField(max_length=100)
	roboPositionX=models.IntegerField()
	roboPositionY=models.IntegerField()
	taskId=models.IntegerField()


class Transaction(models.Model):
	senderId=models.OneToOneField(RoboUser,on_delete=models.CASCADE,related_name='sid')
	receiverId=models.OneToOneField(RoboUser,on_delete=models.CASCADE,related_name='rid')
	timeOfTrans=models.DateTimeField(default=None)
	robo=models.OneToOneField(Robot,on_delete=models.CASCADE,related_name='robotid')
	message=models.CharField(max_length=1000)

