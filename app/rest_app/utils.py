import csv
import io

from django.db.models import Sum

from .models import Deal
from .serializers import DealsSerializer


def csv_parser(data):
    decoded_file = data['data'].read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    dict_csv = list(csv.DictReader(io_string))
    serializer = DealsSerializer(data=dict_csv, many=True)

    if serializer.is_valid():
        Deal.objects.all().delete()
        serializer.save()
        return True
    else:
        return False


def get_top_customers():
    # find top 5 customers by spent money
    deals = Deal.objects.values(
                'customer'
            ).annotate(
                spent_money=Sum('total')
            ).order_by(
                '-spent_money'
            )[:5]

    # create list of dictionaries of customers with name, spent money
    # and list of all gems bought by customer
    customers = []
    for deal in deals:
        customer = {'username': deal['customer'],
                    'spent_money': deal['spent_money'],
                    'gems': []
                    }

        # get all gems that customer bought
        customers_from_db = Deal.objects.filter(
                                customer=customer['username']
                            ).values(
                                'item'
                            ).distinct()

        for row in customers_from_db:
            customer['gems'].append(row['item'])

        customers.append(customer)

    result = []
    for customer in customers:
        for gem in customer['gems']:
            gem_has_duplicate = False
            # iterate through every customer gems
            # and compare it with every other customer gem_list
            for temp_customer in customers:
                # ignore if it's a same customer
                if customer['username'] != temp_customer['username']:
                    # if other customer has gem in his list
                    if gem in temp_customer['gems']:
                        # then mark it
                        gem_has_duplicate = True
                        # and exit loop for this gem
                        break
            # if wasn't able to find second gem in any other
            # customer gem list then delete this gem
            if not gem_has_duplicate:
                customer['gems'].remove(gem)

        result.append(customer)

    return result
