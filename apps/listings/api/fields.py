import base64
import os
from uuid import uuid4
from tastypie.fields import FileField
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

class Base64FileField(FileField):
    """
    A django-tastypie field for handling file-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.
    Usage:

    class MyResource(ModelResource):
        file_field = Base64FileField("file_field")
        
        class Meta:
            queryset = ModelWithFileField.objects.all()

    In the case of multipart for submission, it would also pass the filename.
    By using a raw post data stream, we have to pass the filename within our
    file_field structure:

    file_field = {
        "name": "myfile.png",
        "file": "longbas64encodedstring",
        "content_type": "image/png" # on hydrate optional
    }
    """
    def dehydrate(self, bundle):
        if not bundle.data.has_key(self.instance_name) and hasattr(bundle.obj, self.instance_name):
            file_field = getattr(bundle.obj, self.instance_name)
            return file_field.url

    def hydrate(self, obj):
        value = super(FileField, self).hydrate(obj)
        if value:
            value = SimpleUploadedFile(str(uuid4()) + '.jpg', base64.b64decode(value), 'image/jpeg')
        return value
