#from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import csv
import io
from .serializers import DealsSerializer
from .models import Deal
from django.db.models import Sum
from django.views.decorators.cache import cache_control

class UploadData(APIView):
	parser_classes = (MultiPartParser,)

	def post(self, request, format=None):
		decoded_file = request.data['data'].read().decode('utf-8')
		io_string = io.StringIO(decoded_file)
		dict_csv = list(csv.DictReader(io_string))

		serializer = DealsSerializer(data=dict_csv, many=True)

		if serializer.is_valid():
			Deal.objects.all().delete()
			serializer.save()
			return Response('Файл был обработан без ошибок', status=status.HTTP_200_OK)
		else:
			return Response('Error, Desc:' + str(serializer.errors) + '- в процессе обработки файла произошла ошибка', status=status.HTTP_400_BAD_REQUEST)

class GetData(APIView):

	@cache_control(must_revalidate=True, max_age=3600)
	def get(self, request, format=None):
		#find top 5 customers by spent money
		deals = Deal.objects.values('customer').annotate(spent_money=Sum('total')).order_by('-spent_money')[:5]
		
		#create list of dictionaries of customers with name, spent money 
		#and list of all gems bought by customer
		customers = []
		for deal in deals: 
			customer = {'customer':deal['customer'], 'spent_money': deal['spent_money'], 'gems':[]}

			#get all gems that customer bought
			customers_from_db = Deal.objects.filter(customer=customer['customer']).values('item').distinct()
			for row in customers_from_db:
				customer['gems'].append(row['item'])
			customers.append(customer)

		result = []
		for customer in customers:
			for gem in customer['gems']:
				gem_has_duplicate = False
				#iterate through every customer gems
				#and compare it with every other customer gem_list	
				for c in customers:
					#ignore if it's a same customer
					if customer['customer'] != c['customer']:
						#if other customer has gem in his list
						if gem in c['gems']:
							#then mark it
							gem_has_duplicate = True
							#and exit loop for this gem
							break
				#if wasn't able to find second gem in any other
				#customer gem list then delete this gem
				if not gem_has_duplicate:
					customer['gems'].remove(gem)
			result.append(customer)

		return Response(result, status=status.HTTP_200_OK)