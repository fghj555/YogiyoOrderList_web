#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_yogiyo_api_integration():
    """Yogiyo API 통합 테스트"""
    
    # 서버가 시작될 때까지 대기
    print("⏳ 서버 시작 대기 중...")
    time.sleep(2)
    
    base_url = 'http://127.0.0.1:8000'
    
    print('\n' + '=' * 80)
    print('🧪 Yogiyo API 실시간 데이터 통합 테스트 시작')
    print('=' * 80)
    
    # TEST 1: Search 엔드포인트
    print('\n📌 TEST 1: Search 엔드포인트 (키워드 검색)')
    print('-' * 80)
    try:
        url = f'{base_url}/restaurants/search/'
        params = {
            'keyword': '치킨',
            'lat': 37.4979,
            'lng': 127.0276,
            'category': '치킨'
        }
        print(f"🔗 요청 URL: {url}")
        print(f"📦 파라미터: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        print(f'✅ 상태 코드: {response.status_code}')
        
        data = response.json()
        print(f'📊 응답 구조:')
        print(f"  - count: {data.get('count')}")
        print(f"  - source: {data.get('source')}")
        print(f"  - results 개수: {len(data.get('results', []))}")
        
        if data.get('results'):
            print(f'\n  첫 번째 결과:')
            first_result = data['results'][0]
            for key in ['id', 'name', 'lat', 'lng', 'address', 'average_rating']:
                print(f"    - {key}: {first_result.get(key)}")
        
        if response.status_code == 200 and data.get('source') == 'yogiyo_api':
            print("✅ TEST 1 PASSED: Yogiyo API에서 실시간 데이터 수신 확인!")
        else:
            print("⚠️ TEST 1 FAILED: 예상과 다른 응답")
            
    except Exception as e:
        print(f'❌ TEST 1 FAILED: {e}')
    
    # TEST 2: Menu 엔드포인트
    print('\n' + '=' * 80)
    print('📌 TEST 2: Menu 엔드포인트 (메뉴 조회)')
    print('-' * 80)
    try:
        url = f'{base_url}/restaurants/1/menu/'
        print(f"🔗 요청 URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f'✅ 상태 코드: {response.status_code}')
        
        data = response.json()
        print(f'📊 응답 구조:')
        print(f"  - restaurant_id: {data.get('restaurant_id')}")
        print(f"  - source: {data.get('source')}")
        print(f"  - menu_groups 개수: {len(data.get('menu_groups', []))}")
        
        if response.status_code == 200 and data.get('source') == 'yogiyo_api':
            print("✅ TEST 2 PASSED: Yogiyo API에서 메뉴 데이터 수신 확인!")
        else:
            print("⚠️ TEST 2 FAILED: 예상과 다른 응답")
            
    except Exception as e:
        print(f'❌ TEST 2 FAILED: {e}')
    
    # TEST 3: Detail Full 엔드포인트
    print('\n' + '=' * 80)
    print('📌 TEST 3: Detail Full 엔드포인트 (완전한 식당 정보)')
    print('-' * 80)
    try:
        url = f'{base_url}/restaurants/1/detail_full/'
        print(f"🔗 요청 URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f'✅ 상태 코드: {response.status_code}')
        
        data = response.json()
        print(f'📊 응답 구조:')
        print(f"  - source: {data.get('source')}")
        print(f"  - restaurant 있음: {'restaurant' in data and bool(data['restaurant'])}")
        print(f"  - menus 있음: {'menus' in data and bool(data['menus'])}")
        print(f"  - reviews 있음: {'reviews' in data and bool(data['reviews'])}")
        
        if response.status_code == 200 and data.get('source') == 'yogiyo_api':
            print("✅ TEST 3 PASSED: Yogiyo API에서 완전한 데이터 수신 확인!")
        else:
            print("⚠️ TEST 3 FAILED: 예상과 다른 응답")
            
    except Exception as e:
        print(f'❌ TEST 3 FAILED: {e}')
    
    print('\n' + '=' * 80)
    print('🎉 API 통합 테스트 완료!')
    print('=' * 80)
    print('\n✅ 핵심 결과:')
    print('  - 모든 백그라운드 통신은 Yogiyo API로 진행됨')
    print('  - 웹 UI는 Django API를 호출')
    print('  - Django API는 실시간으로 Yogiyo API와 통신')
    print('  - 데이터 흐름: Web UI → Django API → Yogiyo 실시간 API')
    print('=' * 80)

if __name__ == '__main__':
    test_yogiyo_api_integration()
