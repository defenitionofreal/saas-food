from rest_framework import serializers
from apps.que.models import Que


class QueSerializer(serializers.ModelSerializer):
    """ Queue serializer """
    institution = serializers.CharField(source="order.institution.title")

    class Meta:
        model = Que
        fields = "__all__"
