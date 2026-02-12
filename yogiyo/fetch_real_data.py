#!/usr/bin/env python
"""
실제 요기요 API에서 데이터 크롤링 및 DB 저장
"""
import os
import sys
import django
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yogiyo.settings.dev')
django.setup()

from yogiyo.crawling import Crawling

def main():
    print("=" * 80)
    print("🔄 요기요 API에서 실제 데이터 크롤링 시작")
    print("=" * 80)
    print(f"\n⏰ 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📍 크롤링 지역: 서울 강남역 주변 (37.545133, 127.057129)")
    print("🍽️  대상: 상위 450개 식당")
    
    try:
        print("\n" + "=" * 80)
        print("1️⃣ 웹에서 식당 목록 조회 중...")
        print("=" * 80)
        
        crawling = Crawling()
        
        # Step 1: 식당 ID 리스트 가져오기
        print("📋 GET /api/v1/restaurants-geo/ 호출 중...")
        list_info_dict = crawling.get_page_id_list()
        restaurant_count = len(list_info_dict)
        print(f"✅ {restaurant_count}개의 식당 ID 수집 완료")
        
        # Step 2: 각 식당 상세 정보 수집
        print("\n" + "=" * 80)
        print("2️⃣ 각 식당의 상세 정보 및 메뉴 조회 중...")
        print("=" * 80)
        print(f"이 과정은 시간이 걸릴 수 있습니다 (~{restaurant_count * 3}초)...")
        
        crawling.dict_to_json_file(list_info_dict)
        print(f"✅ yogiyo_data_for_parsing.json 파일 생성 완료")
        
        # Step 3: 데이터 파싱 및 DB 저장
        print("\n" + "=" * 80)
        print("3️⃣ 데이터베이스에 저장 중...")
        print("=" * 80)
        
        crawling.json_parsing()
        
        print("\n" + "=" * 80)
        print("✅ 모든 데이터 수집 및 저장 완료!")
        print("=" * 80)
        
        # 최종 통계
        from restaurants.models import Restaurant
        from reviews.models import Review
        from restaurants.models import Menu
        
        print("\n📊 최종 통계:")
        print(f"  - 저장된 식당: {Restaurant.objects.count()}개")
        print(f"  - 저장된 메뉴: {Menu.objects.count()}개")
        print(f"  - 저장된 리뷰: {Review.objects.count()}개")
        
        print(f"\n⏰ 완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n🌐 웹 브라우저에서 확인: http://127.0.0.1:8000/")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
