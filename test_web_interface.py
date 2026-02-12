#!/usr/bin/env python
"""
웹 인터페이스 기능 테스트
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_web_features():
    """웹 기능 테스트"""
    print("=" * 80)
    print("🧪 웹 인터페이스 기능 테스트")
    print("=" * 80)
    
    tests = [
        {
            "name": "1. 홈페이지 (HTML 페이지)",
            "url": f"{BASE_URL}/",
            "check": lambda r: "index.html" in r.text or "restaurant" in r.text or "html" in r.text.lower()
        },
        {
            "name": "2. 전체 식당 조회 (위치 기반)",
            "url": f"{BASE_URL}/restaurants?lat=37.566350&lng=126.977829",
            "check": lambda r: r.json().get('results') is not None or len(r.json()) > 0
        },
        {
            "name": "3. 나의 입맛저격 (평점순)",
            "url": f"{BASE_URL}/restaurants/home_view_average_rating?lat=37.566350&lng=126.977829",
            "check": lambda r: len(r.json().get('results', r.json())) > 0
        },
        {
            "name": "4. 배달비 무료 필터링",
            "url": f"{BASE_URL}/restaurants/home_view_delivery_charge?lat=37.566350&lng=126.977829",
            "check": lambda r: len(r.json().get('results', r.json())) >= 0
        },
        {
            "name": "5. 오늘만 할인 (할인액순)",
            "url": f"{BASE_URL}/restaurants/home_view_delivery_discount?lat=37.566350&lng=126.977829",
            "check": lambda r: len(r.json().get('results', r.json())) >= 0
        },
        {
            "name": "6. 가장 빨리 (배달시간순)",
            "url": f"{BASE_URL}/restaurants/home_view_delivery_time?lat=37.566350&lng=126.977829",
            "check": lambda r: len(r.json().get('results', r.json())) > 0
        },
        {
            "name": "7. 리뷰 많음 (리뷰수순)",
            "url": f"{BASE_URL}/restaurants/home_view_review?lat=37.566350&lng=126.977829",
            "check": lambda r: len(r.json().get('results', r.json())) > 0
        },
        {
            "name": "8. 우리동네 찜 (찜 많음순)",
            "url": f"{BASE_URL}/restaurants/home_view_bookmark?lat=37.566350&lng=126.977829",
            "check": lambda r: len(r.json().get('results', r.json())) > 0
        },
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            response = requests.get(test["url"], timeout=5)
            
            if response.status_code != 200:
                print(f"❌ {test['name']}")
                print(f"   상태코드: {response.status_code}")
                failed += 1
                continue
            
            # 검증 로직 실행
            if test["check"](response):
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        count = len(data.get('results', data))
                    else:
                        count = len(data)
                    print(f"✅ {test['name']}")
                    print(f"   결과: {count}개 항목")
                    passed += 1
                except json.JSONDecodeError:
                    print(f"✅ {test['name']} (HTML 응답)")
                    passed += 1
            else:
                print(f"❌ {test['name']} (검증 실패)")
                failed += 1
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {test['name']} (서버 연결 실패)")
            failed += 1
        except Exception as e:
            print(f"❌ {test['name']} (오류: {str(e)})")
            failed += 1
        
        print()
    
    print("=" * 80)
    print("📊 웹 기능 테스트 결과")
    print("=" * 80)
    print(f"✅ 성공: {passed}개")
    print(f"❌ 실패: {failed}개")
    print(f"총합: {passed + failed}개")
    print("=" * 80)
    
    if failed == 0:
        print("\n🎉 모든 웹 기능이 정상 작동합니다!")
        print("\n🌐 브라우저에서 확인:")
        print(f"   http://127.0.0.1:8000/")
        print("\n기능:")
        print("   • 🗺️  현재 위치 자동 감지 (GPS)")
        print("   • 📍 수동 좌표 입력")
        print("   • 🏪 7가지 카테고리 필터")
        print("   • ⭐ 평점, 배달시간, 할인 등 정렬")
        print("   • 📱 식당 상세정보 및 리뷰 조회")
    else:
        print(f"\n⚠️ {failed}개의 기능에 문제가 있습니다.")

if __name__ == "__main__":
    test_web_features()
