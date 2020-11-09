from rest_framework.serializers import ListSerializer, ModelSerializer

from .models import Deal


class BulkCreateListSerializer(ListSerializer):
    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        return result


class DealsSerializer(ModelSerializer):

    def create(self, validated_data):
        instance = Deal(**validated_data)

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance

    class Meta:
        model = Deal
        fields = ["customer", "item", "total", "quantity", "date"]
        list_serializer_class = BulkCreateListSerializer
