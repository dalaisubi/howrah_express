from rest_framework import serializers
from .models import FileUpload, File
from rest_framework.fields import CurrentUserDefault

class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = FileUpload
        read_only_fields = ('created', 'datafile', 'owner')


class FileSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.user.id')
	class Meta():
		model = File
		fields = ('file', 'remark', 'timestamp', 'owner')