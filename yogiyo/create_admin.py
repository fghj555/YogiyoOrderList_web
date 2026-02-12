#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yogiyo.settings.dev')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from yogiyo.crawling import Crawling

try:
    c = Crawling()
    users = c.create_users()
    print(f'\n✅ {len(users)}명의 사용자 생성 완료!')
    print('어드민: admin@a.com / 비밀번호: 1111')
    print('테스트 유저 3명 생성됨\n')
except Exception as e:
    print(f'❌ 오류: {e}')
