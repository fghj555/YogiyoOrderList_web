#!/usr/bin/env python
"""
실제 서울 지역 식당 데이터 생성 스크립트
- 서울의 실제 좌표 기반
- 실제 식당명, 주소, 카테고리 사용
- 실제 배달비, 배달시간, 할인율 적용
"""
import os
import sys
import django
from datetime import time

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yogiyo.settings.dev')
django.setup()

from restaurants.models import Restaurant, MenuGroup, Menu
from reviews.models import Review
from users.models import User

def create_real_data():
    """서울의 실제 위치 기반 식당 데이터 생성"""
    
    # 기존 데이터 확인
    if Restaurant.objects.count() > 0:
        print(f"⚠️  기존 식당 {Restaurant.objects.count()}개 발견")
        response = input("삭제하고 새로 생성하시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("취소됨")
            return
        Restaurant.objects.all().delete()
        print("✅ 기존 데이터 삭제 완료")
    
    # 테스트 유저
    try:
        user = User.objects.get(email='admin@a.com')
    except User.DoesNotExist:
        user = User.objects.create_user(email='testuser@test.com', password='1111')
    
    # 실제 서울 지역 식당 데이터
    # 좌표는 실제 서울 지역의 위치
    restaurants_data = [
        {
            'name': '신라면우육탕',
            'address': '서울 중구 명동 50-1',
            'categories': ['한식'],
            'lat': 37.5641,  # 명동
            'lng': 126.9819,
            'delivery_charge': 0,
            'delivery_discount': 2000,
            'delivery_time': 25,
            'min_order_price': 10000,
            'average_rating': 4.6,
        },
        {
            'name': '홍콩반점',
            'address': '서울 중구 다동 111',
            'categories': ['중식'],
            'lat': 37.5630,  # 을지로
            'lng': 126.9979,
            'delivery_charge': 1500,
            'delivery_discount': 0,
            'delivery_time': 35,
            'min_order_price': 15000,
            'average_rating': 4.4,
        },
        {
            'name': '치킨마루',
            'address': '서울 강남구 강남역 32-5',
            'categories': ['치킨'],
            'lat': 37.4979,  # 강남역
            'lng': 127.0276,
            'delivery_charge': 0,
            'delivery_discount': 3000,
            'delivery_time': 20,
            'min_order_price': 14000,
            'average_rating': 4.7,
        },
        {
            'name': '도미노피자',
            'address': '서울 서초구 강남역 38-10',
            'categories': ['피자'],
            'lat': 37.4965,  # 강남역 근처
            'lng': 127.0310,
            'delivery_charge': 2000,
            'delivery_discount': 0,
            'delivery_time': 40,
            'min_order_price': 18000,
            'average_rating': 4.5,
        },
        {
            'name': '쌀국수 베트남',
            'address': '서울 마포구 홍대입구 58-12',
            'categories': ['아시안'],
            'lat': 37.5585,  # 홍대
            'lng': 126.9250,
            'delivery_charge': 0,
            'delivery_discount': 1500,
            'delivery_time': 30,
            'min_order_price': 8000,
            'average_rating': 4.3,
        },
        {
            'name': '족발왕',
            'address': '서울 송파구 가락동 15-20',
            'categories': ['족발·보쌈'],
            'lat': 37.4926,  # 가락동
            'lng': 127.1128,
            'delivery_charge': 2500,
            'delivery_discount': 0,
            'delivery_time': 45,
            'min_order_price': 22000,
            'average_rating': 4.8,
        },
        {
            'name': 'BBQ치킨',
            'address': '서울 구로구 구로디지털단지 102-30',
            'categories': ['치킨'],
            'lat': 37.4850,  # 구로디지털단지
            'lng': 126.9020,
            'delivery_charge': 0,
            'delivery_discount': 2500,
            'delivery_time': 18,
            'min_order_price': 13000,
            'average_rating': 4.6,
        },
        {
            'name': '스시마루',
            'address': '서울 중구 명동 3-1',
            'categories': ['일식'],
            'lat': 37.5645,  # 명동
            'lng': 126.9835,
            'delivery_charge': 1000,
            'delivery_discount': 0,
            'delivery_time': 35,
            'min_order_price': 20000,
            'average_rating': 4.7,
        },
        {
            'name': '토스트앤골드',
            'address': '서울 강남구 강남역 20-15',
            'categories': ['카페·디저트'],
            'lat': 37.4972,  # 강남역
            'lng': 127.0285,
            'delivery_charge': 0,
            'delivery_discount': 0,
            'delivery_time': 15,
            'min_order_price': 6000,
            'average_rating': 4.2,
        },
        {
            'name': '버거킹 강남',
            'address': '서울 강남구 테헤란로 12-20',
            'categories': ['패스트푸드'],
            'lat': 37.4980,  # 강남
            'lng': 127.0365,
            'delivery_charge': 1500,
            'delivery_discount': 2000,
            'delivery_time': 12,
            'min_order_price': 5000,
            'average_rating': 4.1,
        },
        {
            'name': '강남오디숯불구이',
            'address': '서울 강남구 압구정로 123-8',
            'categories': ['구이류'],
            'lat': 37.5250,  # 압구정
            'lng': 127.0250,
            'delivery_charge': 3000,
            'delivery_discount': 0,
            'delivery_time': 50,
            'min_order_price': 30000,
            'average_rating': 4.9,
        },
        {
            'name': '김밥천국 서울역점',
            'address': '서울 중구 한강대로 405',
            'categories': ['분식'],
            'lat': 37.5534,  # 서울역
            'lng': 126.9709,
            'delivery_charge': 500,
            'delivery_discount': 0,
            'delivery_time': 15,
            'min_order_price': 4000,
            'average_rating': 4.0,
        },
        {
            'name': '라면공작소',
            'address': '서울 종로구 종로3가 108-10',
            'categories': ['한식'],
            'lat': 37.5707,  # 종로3가
            'lng': 126.9909,
            'delivery_charge': 0,
            'delivery_discount': 1000,
            'delivery_time': 20,
            'min_order_price': 7000,
            'average_rating': 4.4,
        },
        {
            'name': '올리브영 카페',
            'address': '서울 서초구 서초동 1338-8',
            'categories': ['카페·디저트'],
            'lat': 37.4837,  # 서초동
            'lng': 127.0200,
            'delivery_charge': 0,
            'delivery_discount': 0,
            'delivery_time': 18,
            'min_order_price': 5000,
            'average_rating': 4.2,
        },
    ]
    
    print("\n🍴 실제 서울 지역 식당 생성 중...")
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
            closing_time=time(23, 0),
            tel_number='02-1234-5678',
            address=data['address'],
            payment_methods=['신용카드', '현금'],
            business_name=f"{data['name']} 주식회사",
            company_registration_number='123-45-67890',
            origin_information='국내산',
            representative_menus='',
            review_count=0,
            owner_comment_count=0,
        )
        created_restaurants.append(restaurant)
        print(f"  ✅ {restaurant.name:20} | 좌표: ({restaurant.lat:.4f}, {restaurant.lng:.4f}) | 평점: {restaurant.average_rating}")
        
        # 메뉴 생성
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
    print(f"  - 총 식당: {Restaurant.objects.count()}개")
    print(f"  - 메뉴 그룹: {MenuGroup.objects.count()}개")
    print(f"  - 메뉴: {Menu.objects.count()}개")
    print(f"  - 배달비 무료: {Restaurant.objects.filter(delivery_charge=0).count()}개")
    print(f"  - 할인 있음: {Restaurant.objects.filter(delivery_discount__gt=0).count()}개")
    print(f"  - 평점 4.5 이상: {Restaurant.objects.filter(average_rating__gte=4.5).count()}개")
    
    print("\n🗺️  지역 분포:")
    regions = {
        "강남역/강남": Restaurant.objects.filter(lat__lte=37.50, lat__gte=37.49, lng__lte=127.04, lng__gte=127.02).count(),
        "명동/을지로": Restaurant.objects.filter(lat__lte=37.57, lat__gte=37.56, lng__lte=127.00, lng__gte=126.98).count(),
        "홍대": Restaurant.objects.filter(lat__lte=37.56, lat__gte=37.55, lng__lte=126.93, lng__gte=126.92).count(),
        "기타": Restaurant.objects.count() - 12,
    }
    for region, count in regions.items():
        if count > 0:
            print(f"   - {region}: {count}개")

if __name__ == '__main__':
    print("=" * 80)
    print("🍴 실제 서울 지역 식당 데이터 생성")
    print("=" * 80)
    create_real_data()
    print("\n" + "=" * 80)
    print("완료! http://127.0.0.1:8000/ 에서 확인하세요")
    print("=" * 80)
