from django.contrib.contenttypes.models import ContentType

from django.db.models import Q

from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(label='Email Address')
	email2 = serializers.EmailField(label='Confirm Email')
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
			
		]

		extra_kwargs = {'password': 
					   		{'write_only': True}
					   	}

	def validate(self , data):

		return data

	def validate_email2(self,  value):
		data = self.get_initial()
		email1 = data.get('email')
		email2 = data.get('email2')

		if email2 != email1:
			raise ValidationError("Email must match.")

		user_qs = User.objects.filter(email=email2)
		if user_qs.exists():
			raise ValidationError('This user has already registered.')
				
		return value	

	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']
		user_obj = User(
			username = username,
			email = email
			)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data			   	


class UserLoginSerializer(serializers.ModelSerializer):
	token = serializers.CharField(allow_blank=True, read_only=True)
	username = serializers.CharField(allow_blank=True, required=False)
	email = serializers.EmailField(label='Email Address', allow_blank=True, required=False)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
			'token'
			
		]

		extra_kwargs = {'password': 
					   		{'write_only': True}
					   	}

	def validate(self , data):
		email = data.get('email', None)
		username = data.get('username', None)
		password = data['password']
		user_obj = None
		if not username:
			raise ValidationError('A username is required.')

		user = User.objects.filter (
				Q(username=username)
			).distinct()	
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError("Invalid username.")	

		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Incorrect credentials please try again.")
		data['token'] = "Random token"		
		return data
