import base64
import os
from uuid import uuid4
from tastypie.fields import FileField
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

class Base64FileField(FileField):
    def dehydrate(self, bundle):
        if not bundle.data.has_key(self.instance_name) and hasattr(bundle.obj, self.instance_name):
            return getattr(bundle.obj, self.instance_name + '_urls')

    def hydrate(self, obj):
        value = super(FileField, self).hydrate(obj)
        if value:
            value = SimpleUploadedFile(str(uuid4()) + '.jpg', base64.b64decode(value), 'image/jpeg')
        return value
