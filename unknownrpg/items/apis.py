from rest_framework import serializers
from .models import Item, ItemTemplate
from users.models import BaseUser
from .services import item_shop_list
from characters.models import Character
from characters.services import item_buy, item_sell

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from common.utils import get_object

from rest_framework import status


class ItemShopListApi(APIView):
    permission_classes = [permissions.AllowAny]

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        level_requirement = serializers.IntegerField()
        min_damage = serializers.IntegerField()
        max_damage = serializers.IntegerField()
        min_armour = serializers.IntegerField()
        max_armour = serializers.IntegerField()
        value = serializers.IntegerField()
        type = serializers.CharField()

    def get(self, request):
        items = item_shop_list()
        data = self.OutputSerializer(items, many=True).data

        return Response(data)


class ItemShopBuyApi(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        character_id = serializers.IntegerField()
        item_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_template = get_object(
            ItemTemplate, id=serializer.validated_data['item_id'])

        character = get_object(
            Character, id=serializer.validated_data['character_id'])

        item_buy(
            character=character, item_template=item_template)

        return Response(status=status.HTTP_200_OK)


class ItemShopSellApi(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        character_id = serializers.IntegerField()
        item_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = get_object(
            Item, id=serializer.validated_data['item_id'])

        character = get_object(
            Character, id=serializer.validated_data['character_id'])

        item_sell(
            character=character, item=item)

        return Response(status=status.HTTP_200_OK)
