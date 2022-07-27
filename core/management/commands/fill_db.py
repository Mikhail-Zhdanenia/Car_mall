from django.core.management.base import BaseCommand
from django_countries import data as countries_data

import datetime
import random as r

from faker import Faker
from faker.providers import BaseProvider
from decimal import Decimal

from user.models import UserProfile
from buyer.models import Buyer
from car.models import Car
from supplier.models import Supplier, SupplierGarage
from dealership.models import Dealership
from core.enums import UserRoles, Engine, Transmission, Color


brand_model = {
    'Volvo': ['S40', 'S60', 'S80', 'S90', 'XC40', 'XC60', 'XC80', 'SX90'],
    'Skoda': ['Fabia', 'Octavia', 'Rapid', 'Superb'],
    'Audi': ['80', '100', 'A4', 'A5', 'A7', 'RS4', 'RS5', 'RS7', 'Q5', 'Q7', 'TT', 'TT RS'],
    'BMW': ['i3', 'i5' 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'X5', 'X5 M', 'X6', 'X6 M', 'X7'],
    'Mersedes-Benz': ['190', 'W124', 'CLS,', 'GLS', 'Maybach G 650 Landaulet', 'Maybach GLS', 'Maybach S-Класс'],
    'Honda': ['Civic', 'Civic Type R', 'Integra', 'Accord', 'CR-X', 'CR-Z', 'CR-V'],
    'Mitsubishi': ['Carisma', 'Eclipse', 'Lancer Evolution', 'Sigma', ],
    'Volkswagen': ['Polo', 'Polo GTI', 'Golf', 'Gold GTI', 'Golf R', 'Passat', 'Passat CC', 'Tiguan'],

}


class Provider(BaseProvider):

    def dealer(self):
        dealership_list = ['MegaTrade', 'TechSpec', 'TradeProfi', 'AvtoDom', '4by4group', 'SportAuto', 'VeriDance',
                           'KoolRay', 'North', 'South', 'ProTrade', 'Together company',
                           'HorsMotors', 'TheHorizon', 'Cooperators', 'Simple Auto']

        return r.choice(dealership_list)


def create_characters(brd, eng, trn, clr):

    car_brand = list(set([r.choice(list(brand_model.keys())) for _ in range(brd)]))
    car_model = [brand_model[i] for i in car_brand]
    car_engine = list(set([r.choice(Engine.choices())[0] for _ in range(eng)]))
    car_transmission = list(set([r.choice(Transmission.choices())[0] for _ in range(trn)]))
    car_color = list(set([r.choice(Color.choices())[0] for _ in range(clr)]))

    return {'car_brand': car_brand,
            'car_model': car_model,
            'engine': car_engine,
            'transmission': car_transmission,
            'color': car_color}


def user_spec(usr_role, name):
    """user creating"""
    UserProfile.objects.create(
        username=name,
        email=Faker().email(),
        password='password',
        role=usr_role,
        verifyed_email=r.choice([True, False])
    )


class Command(BaseCommand):

    def handle(self, *args, **options):

        count_cars = 1000
        count_dealership = 10
        count_suppliers = 10
        count_buyers = 10

        '''Create superusers.'''
        if not UserProfile.objects.filter(username__in=('admin')):
            UserProfile.objects.create_superuser('admin', 'admin@mail.ru', 'admin')
            print("===< Created superusers >===")

        '''Clear databases.'''
        UserProfile.objects.filter(is_superuser=False).delete()
        Car.objects.all().delete()


        """Car model pulling"""
        for _ in range(count_cars):
            car = r.choice(list(brand_model.keys()))

            Car.objects.create(
                car_brand=car,
                car_model=r.choice(brand_model[car]),
                engine_type=r.choice(Engine.choices())[0],
                transmission=r.choice(Transmission.choices())[0],
                color=r.choice(Color.choices())[0],
                description=Faker().text(),
            )

        '''Staff.'''
        for i in range(12):
            user_spec(UserRoles.choices()[0][0], str(i) + '_app_user')

        '''Buyer.'''
        for _ in range(count_buyers):
            user_spec(UserRoles.choices()[1][0], Faker().user_name())  # Create buyer user

            Buyer.objects.create(
                user=UserProfile.objects.latest('id'),
                first_name=Faker().first_name(),
                last_name=Faker().last_name(),
                balance=Decimal(str(r.uniform(100000, 1000000))).quantize(Decimal('1.00')),
            )

        '''Supplier model pulling'''
        for _ in range(count_suppliers):
            user_spec(UserRoles.choices()[3][0], Faker().user_name())  # Create supplier user

            Supplier.objects.create(
                user=UserProfile.objects.latest('id'),
                name=Faker().company(),
                year_of_foundation=datetime.date(r.randint(2000, 2022), r.randint(1, 12), r.randint(1, 28)),
            )

        '''Dealership model pulling'''
        f = Faker()
        f.add_provider(Provider)

        for _ in range(count_dealership):
            user_spec(UserRoles.choices()[2][0], Faker().user_name())

            characters_dict = create_characters(brd=5, eng=3, trn=3, clr=10)

            Dealership.objects.create(
                user=UserProfile.objects.latest('id'),
                name=f.dealer(),
                location=r.choice(list(countries_data.COUNTRIES.keys())),
                balance=Decimal(str(r.uniform(150000, 3000000))).quantize(Decimal('1.00')),
                car_characters={                                                               #json field
                    'car_brand': characters_dict['car_brand'],
                    'car_model': characters_dict['car_model'],
                    'engine_type': characters_dict['engine'],
                    'transmission': characters_dict['transmission'],
                    'color': characters_dict['color'],
                }
            )

        '''Supplier cars pulling'''
        for cr in Car.objects.all():
            sup = r.choice(Supplier.objects.all())
            car_price = Decimal(str(r.uniform(1000, 100000))).quantize(Decimal('1.00'))

            SupplierGarage.objects.create(
                car=cr,
                supplier=sup,
                price=car_price,
            )


        print("DATABASE PULL complete! ", end='\n\n')










