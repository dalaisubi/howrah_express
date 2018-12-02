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
        fields = ('file', 'remark', 'timestamp', 'level', 'owner')


class TestSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return "hey manjul"

    class Meta:
        model = File
        fields = ('data', 'id')    