from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from taggit.models import Tag
import json
import os
import requests
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

from restaurants.models import Menu, Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantListSerializer, MenuDetailSerializer, \
    TagSerializer


class YogiyoAPIClient:
    """Yogiyo API와 통신하는 클라이언트"""
    
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({
            'x-apikey': 'iphoneap',
            'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2',
            'User-Agent': 'Mozilla/5.0'
        })
        self.base_url = 'https://www.yogiyo.co.kr/api/v1'
        
    def get_response_json(self, url, timeout=10):
        """API 요청 → JSON 반환"""
        try:
            r = self.s.get(url, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"❌ API 호출 오류 ({url}): {e}")
            return None
    
    def get_restaurants_list(self, lat=37.545133, lng=127.057129, items=50, page=0):
        """식당 목록 조회"""
        url = f'{self.base_url}/restaurants-geo/?items={items}&lat={lat}&lng={lng}&order=rank&page={page}&search='
        return self.get_response_json(url)
    
    def get_restaurant_detail(self, page_id, lat=37.545133, lng=127.057129):
        """식당 상세정보"""
        url = f'{self.base_url}/restaurants/{page_id}/?lat={lat}&lng={lng}'
        return self.get_response_json(url)
    
    def get_restaurant_info(self, page_id):
        """식당 추가정보"""
        url = f'{self.base_url}/restaurants/{page_id}/info/'
        return self.get_response_json(url)
    
    def get_menu(self, page_id):
        """메뉴 조회"""
        url = f'{self.base_url}/restaurants/{page_id}/menu/?add_photo_menu=android&add_one_dish_menu=true&order_serving_type=delivery'
        return self.get_response_json(url)
    
    def get_reviews(self, page_id, count=30, page=1):
        """리뷰 조회"""
        url = f'{self.base_url}/reviews/{page_id}/?count={count}&only_photo_review=false&page={page}&sort=time'
        return self.get_response_json(url)
    
    def get_avg_rating(self, page_id):
        """평균 평점"""
        url = f'https://www.yogiyo.co.kr/review/restaurant/{page_id}/avgrating/'
        return self.get_response_json(url)


class MenuViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """
    menu 디테일 조회


    menu id를 통해서 디테일 조회
    """
    queryset = Menu.objects.all().prefetch_related('option_group__option')
    serializer_class = MenuDetailSerializer
    permission_classes = [AllowAny]


class RestaurantFilter(filters.FilterSet):
    payment_methods = filters.CharFilter(lookup_expr='icontains')
    categories = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Restaurant
        fields = ['payment_methods', 'categories']


class RestaurantViewSet(ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = RestaurantFilter
    ordering_fields = ['average_rating', 'delivery_charge', 'min_order_price', 'delivery_time', 'review_count',
                       'owner_comment_count']
    ordering = ('id',)
    permission_classes = [AllowAny]
    HOME_VIEW_PAGE_SIZE = 20
    _yogiyo_client = None
    
    @property
    def yogiyo_client(self):
        """Yogiyo API 클라이언트 lazy-load"""
        if self._yogiyo_client is None:
            self._yogiyo_client = YogiyoAPIClient()
        return self._yogiyo_client

    def get_realtime_data(self, lat=37.4979, lng=127.0276):
        """실제 Yogiyo API에서 실시간 데이터 로드"""
        print(f"🔄 Yogiyo API에서 실시간 데이터 조회 중... (위도: {lat}, 경도: {lng})")
        
        try:
            # 실제 Yogiyo API에서 식당 목록 조회
            response = self.yogiyo_client.get_restaurants_list(lat=lat, lng=lng, items=50, page=0)
            
            if response and 'restaurants' in response:
                restaurants = response['restaurants']
                print(f"✅ {len(restaurants)}개의 식당을 조회했습니다")
                return restaurants
            else:
                print(f"⚠️ API 응답이 예상과 다릅니다: {response}")
                return []
                
        except Exception as e:
            print(f"❌ 실시간 데이터 조회 오류: {e}")
            return []
    
    def format_yogiyo_restaurant(self, restaurant_data):
        """Yogiyo API 응답을 표준 형식으로 변환"""
        
        # 기본 정보
        formatted = {
            'id': restaurant_data.get('id'),
            'name': restaurant_data.get('name'),
            'lat': restaurant_data.get('lat'),
            'lng': restaurant_data.get('lng'),
            'address': restaurant_data.get('address'),
            'min_order_price': restaurant_data.get('min_order_amount', 0),
            'delivery_charge': restaurant_data.get('delivery_fee'),
            'delivery_time': restaurant_data.get('estimated_delivery_time'),
            'average_rating': restaurant_data.get('avg_rating', 0),
            'review_count': restaurant_data.get('review_count', 0),
            'image': restaurant_data.get('logo_url'),
            'categories': ','.join(restaurant_data.get('categories', [])) if restaurant_data.get('categories') else '',
            'payment_methods': ','.join(restaurant_data.get('payment_methods', [])),
        }
        
        return formatted

    @action(detail=False, methods=['GET'])
    def search(self, request, *args, **kwargs):
        """
        Yogiyo API에서 키워드로 식당 검색
        
        Parameters:
        - keyword: 검색 키워드 (식당명)
        - lat: 위도
        - lng: 경도
        - category: 카테고리 필터 (치킨, 피자 등)
        """
        keyword = request.query_params.get('keyword', '')
        lat = request.query_params.get('lat', 37.4979)
        lng = request.query_params.get('lng', 127.0276)
        category = request.query_params.get('category')
        
        try:
            lat = float(lat)
            lng = float(lng)
        except:
            lat = 37.4979
            lng = 127.0276
        
        print(f"🔍 검색 요청: 키워드='{keyword}', 위치=({lat}, {lng})")
        
        # Yogiyo API에서 실시간 검색 데이터 조회
        realtime_restaurants = self.get_realtime_data(lat=lat, lng=lng)
        
        results = []
        
        if realtime_restaurants:
            for restaurant_data in realtime_restaurants:
                # 제목으로 키워드 필터링
                name = restaurant_data.get('name', '').lower()
                if keyword and keyword.lower() not in name:
                    continue
                
                # 카테고리 필터링
                if category:
                    categories = restaurant_data.get('categories', [])
                    if not any(category.lower() in cat.lower() for cat in categories):
                        continue
                
                formatted = self.format_yogiyo_restaurant(restaurant_data)
                results.append(formatted)
        
        print(f"✅ {len(results)}개의 검색 결과")
        return Response({'results': results[:50], 'count': len(results[:50]), 'source': 'yogiyo_api'})
    
    @action(detail=True, methods=['GET'])
    def menu(self, request, pk=None):
        """
        Yogiyo API에서 식당의 모든 메뉴 조회
        
        Parameters:
        - pk: 식당 ID (Yogiyo 식당 ID)
        """
        print(f"📋 메뉴 조회 요청: 식당 ID={pk}")
        
        try:
            # Yogiyo API에서 메뉴 데이터 직접 조회
            menu_data = self.yogiyo_client.get_menu(pk)
            
            if menu_data:
                print(f"✅ Yogiyo API에서 메뉴 데이터 조회 성공")
                return Response({
                    'restaurant_id': pk,
                    'menu_groups': menu_data.get('menu_groups', []),
                    'source': 'yogiyo_api'
                })
            else:
                print(f"⚠️ API 응답이 없음")
                return Response({
                    'restaurant_id': pk,
                    'menu_groups': [],
                    'error': 'API 응답 없음',
                    'source': 'yogiyo_api'
                })
        except Exception as e:
            print(f"❌ 메뉴 조회 오류: {e}")
            return Response({
                'restaurant_id': pk,
                'menu_groups': [],
                'error': str(e),
                'source': 'yogiyo_api'
            }, status=500)
    
    @action(detail=True, methods=['GET'])
    def detail_full(self, request, pk=None):
        """
        Yogiyo API에서 식당 상세정보 (식당정보, 메뉴, 리뷰 한번에 조회)
        """
        print(f"🏪 상세정보 조회 요청: 식당 ID={pk}")
        
        try:
            # Yogiyo API에서 식당 상세정보 조회
            restaurant_data = self.yogiyo_client.get_restaurant_detail(pk)
            restaurant_info = self.yogiyo_client.get_restaurant_info(pk)
            menu_data = self.yogiyo_client.get_menu(pk)
            reviews_data = self.yogiyo_client.get_reviews(pk)
            
            print(f"✅ Yogiyo API\uc5d0\uc11c \ubaa8\ub4e0 \ub370\uc774\ud130 \uc870\ud68c \uc131\uacf5")
            
            return Response({
                'restaurant': restaurant_data if restaurant_data else {},
                'restaurant_info': restaurant_info if restaurant_info else {},
                'menus': menu_data if menu_data else {},
                'reviews': reviews_data if reviews_data else {},
                'source': 'yogiyo_api'
            })
            
        except Exception as e:
            print(f"❌ 상세정보 조회 오류: {e}")
            return Response({
                'error': str(e),
                'source': 'yogiyo_api'
            }, status=500)

    def retrieve(self, request, *args, **kwargs):
        """
        레스토랑 디테일 조회


        레스토랑 pk로 레스토랑 디테일 조회
        """
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        레스토랑 리스트 조회


        현재 위치로부터 일정 거리의 있는 레스토랑만 조회

        [parameter]
        payment_methods : CASH, CREDIT_CARD, YOGIYO_PAY
        categories : 1인분 주문, 프랜차이즈, 치킨, 피자/양식, 중국집,
                     한식, 일식/돈까스, 족발/보쌈, 야식, 분식, 카페/디저트, 편의점/마트
        ordering : average_rating, delivery_charge, min_order_price, delivery_time, review_count,
                   owner_comment_count
        """
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.filter_by_distance_manual(qs)
        qs = self.filter_by_search(qs)
        if self.action == 'list':
            return qs.prefetch_related('bookmark')
        if self.action == 'retrieve':
            return qs.prefetch_related('menu_group__menu')
        return qs

    def filter_by_search(self, qs):
        search = self.request.query_params.get('search')
        if search:
            qs = Restaurant.objects.filter(Q(name__icontains=search) |
                                           Q(menu_group__menu__name__icontains=search) |
                                           Q(tags__name__icontains=search)).distinct()
        return qs

    def filter_by_distance_manual(self, qs):
        """좌표 기준 반경 1km 쿼리"""
        data = self.request.query_params
        if self.action == 'list':
            lat = data.get('lat')
            lng = data.get('lng')
            if lat and lng:
                lat = float(lat)
                lng = float(lng)
                min_lat = lat - 0.009
                max_lat = lat + 0.009
                min_lon = lng - 0.015
                max_lon = lng + 0.01

                # 최소, 최대 위경도를 1km씩 설정해서 쿼리
                qs = qs.filter(lat__gte=min_lat, lat__lte=max_lat,
                               lng__gte=min_lon, lng__lte=max_lon)
        return qs

    @action(detail=False, methods=['GET'])
    def home_view_average_rating(self, request, *args, **kwargs):
        """
        나의 입맛저격


        별점순으로 정렬
        """
        qs = self.get_queryset().order_by('-average_rating').filter(average_rating__gte=4)
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_bookmark(self, request, *args, **kwargs):
        """
        우리동네 찜 많은 음식점


        찜 개수 순으로 정렬
        """
        qs = self.get_queryset().order_by('-bookmark')
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_delivery_discount(self, request, *args, **kwargs):
        """
        오늘만 할인


        할인이 0원이 아닌 매장"""
        qs = self.get_queryset().filter(delivery_discount__gt=0)
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_delivery_charge(self, request, *args, **kwargs):
        """
        배달비 무료


        배달비 0원
        """
        qs = self.get_queryset().filter(delivery_charge=0)
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_review(self, request, *args, **kwargs):
        """
        최근 7일동안 리뷰가 많아요


        리뷰 개수 순으로 정렬
        """
        qs = self.get_queryset().order_by('-review_count')
        return self.home_view_results(qs)

    @action(detail=False, methods=['GET'])
    def home_view_delivery_time(self, request, *args, **kwargs):
        """
        가장 빨리 배달돼요


        배달 시간순으로 정렬
        """
        qs = self.get_queryset().order_by('delivery_time')
        return self.home_view_results(qs)

    def home_view_results(self, qs):
        serializer = self.get_serializer(qs[:self.HOME_VIEW_PAGE_SIZE], many=True)
        return Response({'results': serializer.data})


class TagViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    검색 자동완성 조회


    레스토랑의 태그 검색
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_search = self.request.query_params.get('name')
        if tag_search:
            queryset = queryset.filter(name__icontains=tag_search)
        elif tag_search == '' or tag_search is None:
            queryset = []
        return queryset[:10]
