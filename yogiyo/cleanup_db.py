#!/usr/bin/env python
"""
데이터베이스 초기화 - 모든 더미 데이터 삭제
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yogiyo.settings.dev')
django.setup()

from restaurants.models import Restaurant

print("=" * 80)
print("🧹 데이터베이스 초기화")
print("=" * 80)

count = Restaurant.objects.count()
if count > 0:
    print(f"\n삭제 중: {count}개의 식당 데이터...")
    Restaurant.objects.all().delete()
    print(f"✅ 완료! {count}개의 모든 데이터 삭제됨")
else:
    print("✅ 데이터베이스가 이미 비어있습니다")

print(f"\n📊 현재 데이터베이스 상태:")
print(f"  - 식당 수: {Restaurant.objects.count()}")

print("\n" + "=" * 80)
print("이제 API 호출로만 데이터를 불러옵니다!")
print("http://127.0.0.1:8000/ 에서 실시간 API 통신을 확인하세요")
print("=" * 80)
