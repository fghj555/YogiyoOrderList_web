#!/usr/bin/env python
"""
실시간 API 데이터 수집 (외부 데이터 → JSON 저장)
"""
import os
import sys
import json
import requests
from datetime import datetime
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yogiyo.settings.dev')
django.setup()

class RealTimeRestaurantFetcher:
    """실시간으로 외부 API에서 식당 정보 수집"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'restaurants_data')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def fetch_from_google_places(self, lat, lng, radius=1000):
        """Google Places API에서 데이터 수집 (테스트용 모의 데이터)"""
        print(f"📍 Google Places API 시뮬레이션 (좌표: {lat}, {lng})")
        
        # 실제 Google Places API URL:
        # https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=restaurant&key={API_KEY}
        
        # 현재는 모의 데이터로 시뮬레이션
        mock_data = {
            "status": "OK",
            "results": [
                {
                    "place_id": f"place_{i}",
                    "name": f"Restaurant {i}",
                    "geometry": {"location": {"lat": lat + (i*0.001), "lng": lng + (i*0.001)}},
                    "rating": 4.0 + (i * 0.1),
                    "user_ratings_total": 100 + (i * 10),
                } for i in range(10)
            ]
        }
        return mock_data
    
    def fetch_from_naver_api(self, lat, lng, keyword="음식점"):
        """Naver MAP API에서 데이터 수집 (테스트용)"""
        print(f"🗺️  Naver MAP API 호출 (키워드: {keyword})")
        
        # 실제 Naver API:
        # https://openapi.naver.com/v1/search/local.json?query={keyword}&display=20
        
        mock_data = {
            "lastBuildDate": datetime.now().isoformat(),
            "total": 20,
            "start": 1,
            "display": 20,
            "items": [
                {
                    "title": f"<b>{keyword}</b> #{i}",
                    "link": f"https://map.naver.com/place/{i}",
                    "category": "음식점 > 한식",
                    "description": "",
                    "telephone": "02-1234-5678",
                    "address": f"서울특별시 강남구 {i}번길",
                    "roadAddress": f"서울특별시 강남구 테헤란로 {100+i}",
                    "mapx": int((lng + (i*0.001)) * 10000000),
                    "mapy": int((lat + (i*0.001)) * 10000000),
                } for i in range(10)
            ]
        }
        return mock_data
    
    def fetch_and_save_json(self, lat=37.4979, lng=127.0276, filename="restaurants_realtime.json"):
        """외부 API에서 데이터 수집 후 JSON으로 저장"""
        
        print("\n" + "=" * 80)
        print("🔄 실시간 데이터 수집 중...")
        print("=" * 80)
        print(f"⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📍 위치: ({lat}, {lng})")
        
        try:
            # Step 1: 외부 API에서 데이터 수집
            print("\n📡 외부 API 호출 중...")
            google_data = self.fetch_from_google_places(lat, lng)
            naver_data = self.fetch_from_naver_api(lat, lng)
            
            # Step 2: 데이터 통합 및 정규화
            print("📝 데이터 통합 중...")
            integrated_data = {
                "timestamp": datetime.now().isoformat(),
                "location": {"lat": lat, "lng": lng},
                "sources": {
                    "google_places": google_data,
                    "naver_map": naver_data,
                },
                "restaurants": self._normalize_data(google_data, naver_data)
            }
            
            # Step 3: JSON으로 저장
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(integrated_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ JSON 저장 완료: {filepath}")
            print(f"📊 저장된 식당 수: {len(integrated_data['restaurants'])}개")
            
            return filepath
            
        except Exception as e:
            print(f"❌ 오류: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _normalize_data(self, google_data, naver_data):
        """외부 API 데이터를 통일된 형식으로 변환"""
        normalized = []
        
        # Google Places 데이터 정규화
        for item in google_data.get('results', []):
            normalized.append({
                "id": item.get('place_id'),
                "name": item.get('name'),
                "lat": item.get('geometry', {}).get('location', {}).get('lat'),
                "lng": item.get('geometry', {}).get('location', {}).get('lng'),
                "rating": item.get('rating'),
                "user_ratings": item.get('user_ratings_total'),
                "source": "google_places"
            })
        
        # Naver 데이터 정규화
        for item in naver_data.get('items', []):
            # 좌표 변환 (Naver는 다른 좌표계 사용)
            naver_lng = item.get('mapx', 0) / 10000000
            naver_lat = item.get('mapy', 0) / 10000000
            
            normalized.append({
                "id": item.get('link', '').split('/')[-1],
                "name": item.get('title', '').replace('<b>', '').replace('</b>', ''),
                "lat": naver_lat,
                "lng": naver_lng,
                "address": item.get('roadAddress') or item.get('address'),
                "telephone": item.get('telephone'),
                "source": "naver_map"
            })
        
        return normalized

def main():
    fetcher = RealTimeRestaurantFetcher()
    
    # 강남역 좌표에서 실시간 데이터 수집
    filepath = fetcher.fetch_and_save_json(
        lat=37.4979, 
        lng=127.0276,
        filename="restaurants_realtime.json"
    )
    
    if filepath:
        print("\n" + "=" * 80)
        print("✅ 완료!")
        print("=" * 80)
        print(f"\n📁 저장 위치: {filepath}")
        print("\n웹 API 엔드포인트에서 이 JSON 데이터를 동적으로 제공합니다:")
        print("   http://127.0.0.1:8000/api/v1/restaurants-realtime/")

if __name__ == '__main__':
    main()
