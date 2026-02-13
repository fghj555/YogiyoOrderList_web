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

from restaurants.models import Menu, Restaurant
from restaurants.serializers import RestaurantDetailSerializer, RestaurantListSerializer, MenuDetailSerializer, \
    TagSerializer


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

    def get_realtime_data(self, lat=37.4979, lng=127.0276):
        """외부 API 또는 JSON 파일에서 실시간 데이터 로드"""
        
        # 방법 1: 저장된 JSON 파일에서 읽기
        json_path = os.path.join(os.path.dirname(__file__), '../restaurants_data/restaurants_realtime.json')
        
        if os.path.exists(json_path) and (datetime.now().timestamp() - os.path.getmtime(json_path)) < 3600:
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('restaurants', [])
            except Exception as e:
                print(f"JSON 읽기 오류: {e}")
        
        # 방법 2: 실시간으로 외부 API 호출
        try:
            # 모의 데이터 생성 (실제 환경에서는 외부 API 호출)
            mock_restaurants = []
            for i in range(10):
                mock_restaurants.append({
                    "id": f"rt_{i}",
                    "name": f"Real API Restaurant {i}",
                    "lat": lat + (i * 0.001),
                    "lng": lng + (i * 0.001),
                    "rating": 4.0 + (i * 0.08),
                    "address": f"서울시 강남구 {i}번길",
                    "source": "realtime_api"
                })
            return mock_restaurants
        except Exception as e:
            print(f"API 호출 오류: {e}")
            return []

    @action(detail=False, methods=['GET'])
    def search(self, request, *args, **kwargs):
        """
        키워드로 식당 검색
        
        Parameters:
        - keyword: 검색 키워드 (식당명, 메뉴명 포함)
        - lat: 위도
        - lng: 경도
        - category: 카테고리 필터 (치킨, 피자 등)
        """
        keyword = request.query_params.get('keyword', '')
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        category = request.query_params.get('category')
        
        qs = self.get_queryset()
        
        # 위치 기반 필터링
        if lat and lng:
            try:
                lat = float(lat)
                lng = float(lng)
                min_lat = lat - 0.009
                max_lat = lat + 0.009
                min_lon = lng - 0.015
                max_lon = lng + 0.01
                qs = qs.filter(lat__gte=min_lat, lat__lte=max_lat,
                              lng__gte=min_lon, lng__lte=max_lon)
            except:
                pass
        
        # 키워드 검색
        if keyword:
            qs = qs.filter(Q(name__icontains=keyword) |
                          Q(menu_group__menu__name__icontains=keyword) |
                          Q(categories__icontains=keyword)).distinct()
        
        # 카테고리 필터
        if category:
            qs = qs.filter(categories__icontains=category)
        
        serializer = self.get_serializer(qs[:50], many=True)
        return Response({'results': serializer.data, 'count': len(serializer.data)})
    
    @action(detail=True, methods=['GET'])
    def menu(self, request, pk=None):
        """
        식당의 모든 메뉴 조회
        
        Parameters:
        - pk: 식당 ID
        """
        restaurant = self.get_object()
        menu_groups = restaurant.menu_group.all().prefetch_related('menu')
        
        data = []
        for group in menu_groups:
            group_data = {
                'group_id': group.id,
                'group_name': group.name,
                'menus': [
                    {
                        'id': m.id,
                        'name': m.name,
                        'price': m.price,
                        'caption': m.caption,
                        'is_photomenu': m.is_photomenu
                    }
                    for m in group.menu.all()
                ]
            }
            data.append(group_data)
        
        return Response({
            'restaurant_id': restaurant.id,
            'restaurant_name': restaurant.name,
            'menu_groups': data
        })
    
    @action(detail=True, methods=['GET'])
    def detail_full(self, request, pk=None):
        """
        식당 상세정보 (메뉴, 리뷰 포함 한번에 조회)
        """
        restaurant = self.get_object()
        
        # 식당 정보
        serializer = RestaurantDetailSerializer(restaurant)
        restaurant_data = serializer.data
        
        # 메뉴 정보
        menu_groups = restaurant.menu_group.all().prefetch_related('menu')
        menus = []
        for group in menu_groups:
            for menu in group.menu.all():
                menus.append({
                    'id': menu.id,
                    'name': menu.name,
                    'price': menu.price,
                    'caption': menu.caption,
                    'group': group.name
                })
        
        # 리뷰 정보
        reviews = restaurant.review.all()[:10]
        reviews_data = [
            {
                'id': r.id,
                'owner_name': r.owner.email if r.owner else 'Anonymous',
                'rating': r.rating,
                'caption': r.caption,
                'created': r.created.isoformat() if r.created else None
            }
            for r in reviews
        ]
        
        return Response({
            'restaurant': restaurant_data,
            'menus': menus,
            'reviews': reviews_data,
            'menu_count': len(menus),
            'review_count': len(reviews_data)
        })

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
