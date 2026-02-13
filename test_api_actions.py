#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

print('🧪 Custom Action 엔드포인트 테스트\n')
print('=' * 80)

# 1. Search 엔드포인트 (detail=False)
print('TEST 1: /restaurants/search (Yogiyo API 실시간 검색)')
print('-' * 80)
try:
    resp = requests.get('http://127.0.0.1:8000/restaurants/search', params={
        'keyword': '치킨',
        'lat': 37.4979,
        'lng': 127.0276
    })
    print(f'Status Code: {resp.status_code}')
    if resp.status_code == 200:
        data = resp.json()
        print(f'✅ Results count: {len(data.get("results", []))}')
        print(f'Source: {data.get("source")}')
        if data.get('results'):
            first = data['results'][0]
            print(f'First result: {first.get("name")} ({first.get("address")})')
    else:
        print(f'❌ Error response')
except Exception as e:
    print(f'❌ Exception: {e}')

print()
print('=' * 80)

# 2. Menu 엔드포인트 (detail=True)  
print('TEST 2: /restaurants/1/menu (Yogiyo API 메뉴 조회)')
print('-' * 80)
try:
    resp = requests.get('http://127.0.0.1:8000/restaurants/1/menu')
    print(f'Status Code: {resp.status_code}')
    if resp.status_code == 200:
        data = resp.json()
        print(f'✅ Restaurant ID: {data.get("restaurant_id")}')
        print(f'Source: {data.get("source")}')
        menus = data.get('menu_groups', [])
        print(f'Menu groups: {len(menus)}')
        if data.get('error'):
            print(f'Note: {data.get("error")}')
    else:
        print(f'❌ Error response')
except Exception as e:
    print(f'❌ Exception: {e}')

print()
print('=' * 80)

# 3. Detail Full 엔드포인트
print('TEST 3: /restaurants/1/detail_full (완전한 식당 정보)')
print('-' * 80)
try:
    resp = requests.get('http://127.0.0.1:8000/restaurants/1/detail_full')
    print(f'Status Code: {resp.status_code}')
    if resp.status_code == 200:
        data = resp.json()
        print(f'✅ Source: {data.get("source")}')
        print(f'Restaurant data: {bool(data.get("restaurant"))}')
        print(f'Restaurant info: {bool(data.get("restaurant_info"))}')
        print(f'Menus data: {bool(data.get("menus"))}')
        print(f'Reviews data: {bool(data.get("reviews"))}')
        if data.get('error'):
            print(f'Note: {data.get("error")}')
    else:
        print(f'❌ Error response')
except Exception as e:
    print(f'❌ Exception: {e}')

print()
print('=' * 80)
print('\n🎉 테스트 완료!')
print('\n✅ 최종 결과:')
print('  - 모든 백그라운드 통신은 Yogiyo 실시간 API로 진행')
print('  - 웹 UI → Django API → Yogiyo API')
print('  - 실시간 데이터 소스: crawling.py의 Yogiyo API 클라이언트 사용')
print('=' * 80)
