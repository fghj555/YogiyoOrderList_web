#!/usr/bin/env python
"""
현재 시스템 분석 및 API 엔드포인트 상태 확인
"""
import requests
import json

print("=" * 80)
print("📊 현재 시스템 분석")
print("=" * 80)

BASE_URL = "http://127.0.0.1:8000"

# 테스트할 엔드포인트들
endpoints = {
    "홈페이지": "/",
    "전체 식당": "/restaurants?lat=37.4979&lng=127.0276",
    "평점순": "/restaurants/home_view_average_rating?lat=37.4979&lng=127.0276",
    "배달비무료": "/restaurants/home_view_delivery_charge?lat=37.4979&lng=127.0276",
    "할인": "/restaurants/home_view_delivery_discount?lat=37.4979&lng=127.0276",
    "배달빠름": "/restaurants/home_view_delivery_time?lat=37.4979&lng=127.0276",
    "리뷰많음": "/restaurants/home_view_review?lat=37.4979&lng=127.0276",
    "찜": "/restaurants/home_view_bookmark?lat=37.4979&lng=127.0276",
}

print("\n✅ 현재 작동하는 엔드포인트:")
print("-" * 80)

working = 0
for name, endpoint in endpoints.items():
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            print(f"  ✅ {name:15} {endpoint}")
            working += 1
    except:
        pass

print(f"\n총 {working}개의 엔드포인트가 작동 중입니다.")

# 필요한 추가 기능
print("\n" + "=" * 80)
print("🔧 추가로 필요한 기능")
print("=" * 80)

features = [
    "1. 키워드 검색 (/restaurants/search/?keyword=치킨&lat=&lng=)",
    "2. 메뉴 조회 (/restaurants/{id}/menu/)",
    "3. 메뉴 검색 (/menu/search/?keyword=...)",
    "4. 상세 정보 + 메뉴 한번에 (/restaurants/{id}/detail/)",
    "5. 근처 식당 추천 (/restaurants/nearby/?lat=&lng=&radius=...)",
]

for feature in features:
    print(f"  ⏳ {feature}")

print("\n" + "=" * 80)
print("✨ 개선 계획")
print("=" * 80)
print("""
1️⃣ 검색 기능 강화
   - 키워드 기반 식당 검색
   - 카테고리 필터링
   - 정렬 옵션 (평점, 배달시간, 최소주문금)

2️⃣ 메뉴 시스템
   - 각 식당의 모든 메뉴 조회
   - 메뉴 상세정보 (가격, 설명)
   - 메뉴 검색

3️⃣ 통합 조회
   - 한 번에 식당 + 메뉴 + 리뷰 조회

4️⃣ 실시간 필터링
   - 모든 데이터는 API에서만 - ✅ 이미 구현됨
   - 데이터베이스에서 실시간으로 조회
""")

print("=" * 80)
print("현재 상태: ✅ 웹 인터페이스 ⬌ Django REST API ⬌ 데이터베이스")
print("개선 필요: 더 많은 API 엔드포인트 추가")
print("=" * 80)
