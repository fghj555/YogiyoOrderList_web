#!/usr/bin/env python
"""
API 테스트 스크립트: 모든 엔드포인트 확인
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
LAT = 37.566350
LNG = 126.977829

def test_endpoint(name, url):
    """API 엔드포인트 테스트"""
    try:
        response = requests.get(url, timeout=5)
        status = "✅" if response.status_code == 200 else "❌"
        
        # JSON 파싱 시도
        try:
            data = response.json()
            count = len(data.get('results', data)) if isinstance(data, dict) else len(data)
            print(f"{status} [{response.status_code}] {name}: {count}개 결과")
        except:
            print(f"{status} [{response.status_code}] {name}: (JSON 아님)")
        
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(f"❌ [연결실패] {name}: 서버가 실행 중이 아닙니다")
        return False
    except Exception as e:
        print(f"❌ [오류] {name}: {e}")
        return False

def main():
    print("=" * 80)
    print("🧪 YogiYo Clone API 테스트 시작")
    print("=" * 80)
    
    tests = [
        ("홈페이지", f"{BASE_URL}/"),
        ("전체 식당", f"{BASE_URL}/restaurants?lat={LAT}&lng={LNG}"),
        ("나의 입맛저격", f"{BASE_URL}/restaurants/home_view_average_rating?lat={LAT}&lng={LNG}"),
        ("우리동네 찜", f"{BASE_URL}/restaurants/home_view_bookmark?lat={LAT}&lng={LNG}"),
        ("배달비 무료", f"{BASE_URL}/restaurants/home_view_delivery_charge?lat={LAT}&lng={LNG}"),
        ("오늘만 할인", f"{BASE_URL}/restaurants/home_view_delivery_discount?lat={LAT}&lng={LNG}"),
        ("가장 빨리", f"{BASE_URL}/restaurants/home_view_delivery_time?lat={LAT}&lng={LNG}"),
        ("리뷰 많음", f"{BASE_URL}/restaurants/home_view_review?lat={LAT}&lng={LNG}"),
        ("Swagger API", f"{BASE_URL}/swagger/"),
    ]
    
    results = []
    for name, url in tests:
        success = test_endpoint(name, url)
        results.append((name, success))
        print()
    
    print("=" * 80)
    print("📊 테스트 결과 요약")
    print("=" * 80)
    
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    for name, success in results:
        status = "✅ 성공" if success else "❌ 실패"
        print(f"{status}: {name}")
    
    print("=" * 80)
    print(f"총 {total_count}개 중 {success_count}개 성공 ({success_count/total_count*100:.1f}%)")
    print("=" * 80)
    
    if success_count == total_count:
        print("\n🎉 모든 테스트 통과! 서버가 정상 작동 중입니다.")
    else:
        print(f"\n⚠️ {total_count - success_count}개의 테스트가 실패했습니다.")

if __name__ == "__main__":
    main()
