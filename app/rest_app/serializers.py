from rest_framework.serializers import ModelSerializer
from .models import Deal

class DealsSerializer(ModelSerializer):
	class Meta:
		model = Deal
		fields = ["customer", "item", "total", "quantity", "date"]