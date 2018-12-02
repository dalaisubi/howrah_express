from rest_framework import serializers
from .models import FileUpload, File, Photo
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



class FileListSerializer ( serializers.Serializer ) :
    image = serializers.ListField(
                       child=serializers.FileField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False )
                                )
    def create(self, validated_data):
        blogs=Blogs.objects.latest('created_at')
        image=validated_data.pop('image')
        for img in image:
            photo=Photo.objects.create(image=img,blogs=blogs,**validated_data)
        return photo

class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        read_only_fields = ("blogs",)        