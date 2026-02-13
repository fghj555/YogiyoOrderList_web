#!/usr/bin/env python
"""
실제 요기요 API 엔드포인트 분석 및 테스트
"""
import requests
import json
from datetime import datetime

class YogiyoAPIClient:
    """요기요 API 공식 클라이언트"""
    
    BASE_URL = "https://www.yogiyo.co.kr/api/v1"
    
    def __init__(self):
        self.session = requests.Session()
        # 요기요 모바일 앱 헤더
        self.session.headers.update({
            'x-apikey': 'iphoneap',
            'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2',
            'User-Agent': 'YogiyoAndroid/9.5.0',
            'Accept': 'application/json',
        })
    
    def get_restaurants_by_location(self, lat, lng, items=100, page=0):
        """위치 기반 식당 검색"""
        url = f"{self.BASE_URL}/restaurants-geo/"
        params = {
            'lat': lat,
            'lng': lng,
            'items': items,
            'page': page,
            'order': 'rank',
            'search': ''
        }
        return self._request('GET', url, params=params)
    
    def get_restaurant_detail(self, restaurant_id):
        """식당 상세정보 조회"""
        url = f"{self.BASE_URL}/restaurants/{restaurant_id}/"
        params = {'lat': 37.4979, 'lng': 127.0276}
        return self._request('GET', url, params=params)
    
    def get_restaurant_menu(self, restaurant_id):
        """식당 메뉴 조회"""
        url = f"{self.BASE_URL}/restaurants/{restaurant_id}/menu/"
        params = {
            'add_photo_menu': 'android',
            'add_one_dish_menu': 'true',
            'order_serving_type': 'delivery'
        }
        return self._request('GET', url, params=params)
    
    def get_restaurant_reviews(self, restaurant_id):
        """식당 리뷰 조회"""
        url = f"{self.BASE_URL}/reviews/{restaurant_id}/"
        params = {
            'count': 30,
            'page': 1,
            'sort': 'time',
            'only_photo_review': 'false'
        }
        return self._request('GET', url, params=params)
    
    def search_restaurants(self, keyword, lat, lng):
        """키워드로 식당 검색"""
        url = f"{self.BASE_URL}/restaurants-geo/"
        params = {
            'lat': lat,
            'lng': lng,
            'search': keyword,
            'items': 50,
            'page': 0,
            'order': 'rank'
        }
        return self._request('GET', url, params=params)
    
    def _request(self, method, url, **kwargs):
        """HTTP 요청 실행"""
        try:
            response = self.session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}

def test_yogiyo_api():
    """요기요 API 테스트"""
    print("=" * 80)
    print("🔍 요기요 API 실제 테스트")
    print("=" * 80)
    
    client = YogiyoAPIClient()
    lat, lng = 37.4979, 127.0276  # 강남역
    
    # 테스트 1: 위치 기반 식당 검색
    print(f"\n1️⃣ 위치 기반 식당 검색 (강남역: {lat}, {lng})")
    print("-" * 80)
    result = client.get_restaurants_by_location(lat, lng, items=20)
    
    if 'error' in result:
        print(f"❌ 오류: {result['error']}")
        print(f"상태 코드: {result.get('status_code')}")
    elif 'restaurants' in result:
        restaurants = result['restaurants']
        print(f"✅ 성공! 식당 {len(restaurants)}개 조회")
        
        if restaurants:
            first = restaurants[0]
            print(f"\n첫 번째 식당:")
            print(f"  - ID: {first.get('id')}")
            print(f"  - 이름: {first.get('name')}")
            print(f"  - 평점: {first.get('rating')}")
            print(f"  - 카테고리: {first.get('categories')}")
            print(f"  - 배달비: {first.get('delivery_fee')}")
            
            # 테스트 2: 식당 상세정보
            print(f"\n2️⃣ 식당 상세정보 조회 (ID: {first['id']})")
            print("-" * 80)
            detail = client.get_restaurant_detail(first['id'])
            if 'error' in detail:
                print(f"❌ 오류: {detail['error']}")
            else:
                print(f"✅ 조회 성공")
                print(f"  - 소개: {detail.get('notification')[:50]}...")
            
            # 테스트 3: 메뉴 조회
            print(f"\n3️⃣ 메뉴 조회")
            print("-" * 80)
            menu = client.get_restaurant_menu(first['id'])
            if 'error' in menu:
                print(f"❌ 오류: {menu['error']}")
            elif 'menu_groups' in menu or isinstance(menu, list):
                print(f"✅ 메뉴 조회 성공")
            else:
                print(f"⚠️ 응답 형식: {type(menu).__name__}")
            
            # 테스트 4: 리뷰 조회
            print(f"\n4️⃣ 리뷰 조회")
            print("-" * 80)
            reviews = client.get_restaurant_reviews(first['id'])
            if 'error' in reviews:
                print(f"❌ 오류: {reviews['error']}")
            elif 'results' in reviews:
                print(f"✅ 리뷰 {len(reviews['results'])}개 조회")
            else:
                print(f"⚠️ 응답 형식: {type(reviews).__name__}")
        
        # 테스트 5: 검색
        print(f"\n5️⃣ 키워드 검색 ('치킨')")
        print("-" * 80)
        search_result = client.search_restaurants('치킨', lat, lng)
        if 'error' in search_result:
            print(f"❌ 오류: {search_result['error']}")
        elif 'restaurants' in search_result:
            print(f"✅ 검색 결과 {len(search_result['restaurants'])}개")
        else:
            print(f"⚠️ 응답 형식: {type(search_result).__name__}")
    
    else:
        print(f"⚠️ 예상치 못한 응답 형식")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:500])

if __name__ == '__main__':
    test_yogiyo_api()
