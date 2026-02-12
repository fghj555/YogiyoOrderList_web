#!/usr/bin/env python
"""
요기요 API 응답 확인 및 디버깅
"""
import requests
import json

def test_api():
    print("=" * 80)
    print("🔍 요기요 API 테스트")
    print("=" * 80)
    
    # API 헤더 설정 (요기요 모바일 앱처럼)
    headers = {
        'x-apikey': 'iphoneap',
        'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
    }
    
    lat = 37.545133
    lng = 127.057129
    
    url = f'https://www.yogiyo.co.kr/api/v1/restaurants-geo/?items=450&lat={lat}&lng={lng}&order=rank&page=0&search='
    
    print(f"\n📍 요청 URL: {url}")
    print(f"🔐 헤더: API Key 포함")
    
    try:
        print("\n⏳ API 호출 중...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"✅ 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📄 응답 키: {list(data.keys())}")
            
            if 'restaurants' in data:
                print(f"✅ 'restaurants' 키 발견!")
                print(f"📊 식당 수: {len(data['restaurants'])}")
                if len(data['restaurants']) > 0:
                    print(f"\n첫 번째 식당 정보:")
                    first = data['restaurants'][0]
                    print(f"  - ID: {first.get('id')}")
                    print(f"  - 이름: {first.get('name')}")
                    print(f"  - 평점: {first.get('rating')}")
            else:
                print(f"❌ 'restaurants' 키 없음")
                print(f"응답 내용 (처음 500자):")
                print(json.dumps(data, ensure_ascii=False)[:500])
        else:
            print(f"❌ 오류 상태 코드: {response.status_code}")
            print(f"응답: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == '__main__':
    test_api()
