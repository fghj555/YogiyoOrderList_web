#!/usr/bin/env python
import requests
import json

print("=" * 80)
print("🧪 실시간 API 엔드포인트 테스트")
print("=" * 80)

URL = "http://127.0.0.1:8000/restaurants/realtime/?lat=37.4979&lng=127.0276"

try:
    print(f"\n📍 요청: GET {URL}")
    response = requests.get(URL, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 상태 코드: {response.status_code}")
        print(f"⏰ 타임스탬프: {data.get('timestamp')}")
        restaurants = data.get('restaurants', [])
        print(f"📊 수집된 식당: {len(restaurants)}개")
        print(f"📍 데이터 소스: 외부 API (Google Places + Naver MAP)")
        print("\n첫 번째 식당:")
        if restaurants:
            print(json.dumps(restaurants[0], indent=2, ensure_ascii=False))
    else:
        print(f"❌ 상태 코드: {response.status_code}")
        
except Exception as e:
    print(f"❌ 오류: {e}")

