from rest_framework import serializers
from items.models import Item, ItemTemplate
from users.models import BaseUser
from characters.models import Character
from characters.services import item_buy, item_sell, item_equip, item_unequip

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from django.http import Http404

from common.utils import get_object

from rest_framework import status
from django.core.exceptions import PermissionDenied


class CharacterListApi(APIView):
    permission_classes = [permissions.AllowAny]

    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        level = serializers.IntegerField()

    def get(self, request):
        characters = Character.objects.rankings()
        data = self.OutputSerializer(characters, many=True).data

        return Response(data)


class CharacterDetailApi(APIView):
    permission_classes = [permissions.AllowAny]

    # class AuthenticatedOutputSerializer(serializers.Serializer):
    #     name = serializers.CharField()
    #     level = serializers.IntegerField()
    #     items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        level = serializers.IntegerField()

    def get(self, request, name):
        character = get_object(
            Character, name__iexact=name)

        if character is None:
            raise Http404

        serializer = self.OutputSerializer(character)

        return Response(serializer.data)


class CharacterItemsListApi(APIView):
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

        container = serializers.CharField()
        has_bonuses = serializers.BooleanField()

    def get(self, request, name):
        character = get_object(
            Character, name__iexact=name)

        if character is None:
            raise Http404

        items = character.items
        data = self.OutputSerializer(items, many=True).data

        return Response(data)


class CharacterItemsEquipApi(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        item_id = serializers.IntegerField()

    def post(self, request, name):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = get_object(
            Item, id=serializer.validated_data['item_id'])

        character = get_object(
            Character, name__iexact=name)

        if item is None or character is None:
            raise Http404

        if request.user.is_authenticated and request.user.character.id == character.id:
            item_equip(
                character=character, item=item)

            return Response(status=status.HTTP_200_OK)
        raise PermissionDenied()


class CharacterItemsUnequipApi(APIView):
    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        item_id = serializers.IntegerField()

    def post(self, request, name):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = get_object(
            Item, id=serializer.validated_data['item_id'])

        character = get_object(
            Character, name__iexact=name)

        if item is None or character is None:
            raise Http404

        if request.user.is_authenticated and request.user.character.id == character.id:
            item_unequip(
                character=character, item=item)

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
