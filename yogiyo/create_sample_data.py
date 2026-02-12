#!/usr/bin/env python
"""
테스트용 샘플 식당 데이터 생성 스크립트
"""
import os
import sys
import django
from datetime import time

# Django 설정
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yogiyo.settings.dev')
django.setup()

from restaurants.models import Restaurant, MenuGroup, Menu
from users.models import User

def create_sample_data():
    """서울시청 근처 샘플 식당 10개 생성"""
    
    # 기존 데이터 확인
    if Restaurant.objects.count() > 0:
        print(f"⚠️  기존 식당 {Restaurant.objects.count()}개 발견")
        response = input("기존 데이터를 삭제하고 새로 생성하시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("취소됨")
            return
        Restaurant.objects.all().delete()
        print("✅ 기존 데이터 삭제 완료")
    
    # 테스트 유저 생성
    try:
        user = User.objects.get(email='admin@a.com')
    except User.DoesNotExist:
        user = User.objects.create_user(email='testuser@test.com', password='1111')
    
    # 서울시청 좌표: 37.566350, 126.977829
    base_lat = 37.566350
    base_lng = 126.977829
    
    restaurants_data = [
        {
            'name': '맛있는 치킨',
            'categories': ['치킨'],
            'lat': base_lat + 0.001,
            'lng': base_lng + 0.001,
            'delivery_charge': 0,
            'delivery_discount': 3000,
            'delivery_time': 30,
            'min_order_price': 15000,
            'average_rating': 4.5,
        },
        {
            'name': '피자천국',
            'categories': ['피자'],
            'lat': base_lat - 0.001,
            'lng': base_lng + 0.001,
            'delivery_charge': 2000,
            'delivery_discount': 0,
            'delivery_time': 40,
            'min_order_price': 20000,
            'average_rating': 4.8,
        },
        {
            'name': '중국집',
            'categories': ['중식'],
            'lat': base_lat + 0.002,
            'lng': base_lng - 0.001,
            'delivery_charge': 0,
            'delivery_discount': 2000,
            'delivery_time': 25,
            'min_order_price': 12000,
            'average_rating': 4.2,
        },
        {
            'name': '분식왕국',
            'categories': ['분식'],
            'lat': base_lat - 0.002,
            'lng': base_lng - 0.001,
            'delivery_charge': 1000,
            'delivery_discount': 0,
            'delivery_time': 20,
            'min_order_price': 8000,
            'average_rating': 4.0,
        },
        {
            'name': '돈까스하우스',
            'categories': ['일식'],
            'lat': base_lat + 0.003,
            'lng': base_lng,
            'delivery_charge': 0,
            'delivery_discount': 1000,
            'delivery_time': 35,
            'min_order_price': 10000,
            'average_rating': 4.6,
        },
        {
            'name': '족발보쌈',
            'categories': ['족발·보쌈'],
            'lat': base_lat - 0.003,
            'lng': base_lng,
            'delivery_charge': 3000,
            'delivery_discount': 0,
            'delivery_time': 45,
            'min_order_price': 25000,
            'average_rating': 4.7,
        },
        {
            'name': '한식당',
            'categories': ['한식'],
            'lat': base_lat,
            'lng': base_lng + 0.002,
            'delivery_charge': 0,
            'delivery_discount': 0,
            'delivery_time': 30,
            'min_order_price': 15000,
            'average_rating': 3.9,
        },
        {
            'name': '버거킹',
            'categories': ['패스트푸드'],
            'lat': base_lat,
            'lng': base_lng - 0.002,
            'delivery_charge': 2000,
            'delivery_discount': 1500,
            'delivery_time': 15,
            'min_order_price': 5000,
            'average_rating': 4.3,
        },
        {
            'name': '카페베네',
            'categories': ['카페·디저트'],
            'lat': base_lat + 0.001,
            'lng': base_lng - 0.001,
            'delivery_charge': 0,
            'delivery_discount': 0,
            'delivery_time': 20,
            'min_order_price': 6000,
            'average_rating': 4.1,
        },
        {
            'name': '야식천국',
            'categories': ['야식'],
            'lat': base_lat - 0.001,
            'lng': base_lng - 0.001,
            'delivery_charge': 1000,
            'delivery_discount': 2000,
            'delivery_time': 25,
            'min_order_price': 12000,
            'average_rating': 4.4,
        }
    ]
    
    print("\n식당 생성 중...")
    created_restaurants = []
    
    for data in restaurants_data:
        restaurant = Restaurant.objects.create(
            name=data['name'],
            categories=data['categories'],
            lat=data['lat'],
            lng=data['lng'],
            delivery_charge=data['delivery_charge'],
            delivery_discount=data['delivery_discount'],
            delivery_time=data['delivery_time'],
            min_order_price=data['min_order_price'],
            average_rating=data['average_rating'],
            average_taste=data['average_rating'],
            average_delivery=data['average_rating'],
            average_amount=data['average_rating'],
            notification=f"{data['name']}에 오신 것을 환영합니다!",
            opening_time=time(9, 0),
            closing_time=time(22, 0),
            tel_number='02-1234-5678',
            address='서울특별시 중구 세종대로 110',
            payment_methods=['신용카드', '현금'],
            business_name=f"{data['name']} 주식회사",
            company_registration_number='123-45-67890',
            origin_information='국내산',
            representative_menus='',
            review_count=0,
            owner_comment_count=0,
        )
        created_restaurants.append(restaurant)
        print(f"  ✅ {restaurant.name} (평점: {restaurant.average_rating})")
        
        # 메뉴 그룹 및 메뉴 생성
        menu_group = MenuGroup.objects.create(
            restaurant=restaurant,
            name='인기메뉴'
        )
        
        Menu.objects.create(
            menu_group=menu_group,
            name=f'{data["name"]} 시그니처',
            price=data['min_order_price'],
            caption='가장 인기있는 메뉴입니다'
        )
    
    print(f"\n✅ 총 {len(created_restaurants)}개 식당 생성 완료!")
    
    # 통계
    print("\n📊 생성된 데이터 통계:")
    print(f"  - 식당: {Restaurant.objects.count()}개")
    print(f"  - 메뉴 그룹: {MenuGroup.objects.count()}개")
    print(f"  - 메뉴: {Menu.objects.count()}개")
    print(f"  - 배달비 무료: {Restaurant.objects.filter(delivery_charge=0).count()}개")
    print(f"  - 할인 있음: {Restaurant.objects.filter(delivery_discount__gt=0).count()}개")
    print(f"  - 평점 4.0 이상: {Restaurant.objects.filter(average_rating__gte=4.0).count()}개")

if __name__ == '__main__':
    print("=" * 80)
    print("🍔 샘플 식당 데이터 생성")
    print("=" * 80)
    create_sample_data()
    print("\n" + "=" * 80)
    print("완료! http://127.0.0.1:8000/ 에서 확인하세요")
    print("=" * 80)
