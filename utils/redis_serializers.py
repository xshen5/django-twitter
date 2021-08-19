from django.core import serializers
from utils.json_encoder import JSONEncoder

class DjangoModelSerializer:

    @classmethod
    def serialize(cls, instance):
        # in Django, serializer requires to have data with type of QuerySet or list in order to be serialized
        # adding [] to instance to convert it to a list
        return serializers.serialize('json', [instance], cls=JSONEncoder)

    @classmethod
    def deserialize(cls, serialized_data):
        # need to add .object to access the original Model of the object
        # otherwise the deserialize() returns a DeserlializedObject instead of ORM object
        return list(serializers.deserialize('json', serialized_data))[0].object