from django import views
from django.shortcuts import render
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import Distance, D
from rest_framework import viewsets, mixins
from rest_framework.generics import ListAPIView, CreateAPIView
from msjs.serializers import MessageSerializer
from msjs.models import Message
import math

class NearMessages(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MessageSerializer
    paginate_by = 100
    http_method_names = ['get',]

    @classmethod
    def get_extra_actions(cls):
        return []

    def get_queryset(self):
        lat = float(self.request.query_params.get('lat'))
        lon = float(self.request.query_params.get('lon'))

        if not lat or not lon:
            return []

        # pnt = Point(lon, lat)
        pnt = GEOSGeometry(f'POINT({lon} {lat})', srid=4326)

        distance_deg = 500 / (111_319.5 * math.cos(lat * (math.pi / 180)))

        queryset = Message.objects.filter(banned=False, active=True, location__distance_lte=(pnt, 300)).order_by('-added')
        return queryset

class UserMessages(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.filter(banned=False, active=False).order_by('-added')
    filter_fields = ['owner__username', ]
    http_method_names = ['get',]

    @classmethod
    def get_extra_actions(cls):
        return []

class NewMessage(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MessageSerializer
    http_method_names = ['post',]

    @classmethod
    def get_extra_actions(cls):
        return []

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            new_point = Point(float(self.request.data.get('lon')), float(self.request.data.get('lat')))
            serializer.save(owner=self.request.user, location=new_point)
        return super().perform_create(serializer)