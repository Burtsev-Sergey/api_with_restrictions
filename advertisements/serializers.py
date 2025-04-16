from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement
from rest_framework.exceptions import ValidationError
from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)

class AdvertisementSerializer(serializers.ModelSerializer):
  """Serializer для объявления."""

  creator = UserSerializer(
    read_only=True,
  )

  class Meta:
    model = Advertisement
    fields = ('id', 'title', 'description', 'creator',
         'status', 'created_at', )

  def create(self, validated_data):
    """Метод для создания объявления"""
    
    validated_data["creator"] = self.context["request"].user
    return super().create(validated_data)

  def validate(self, data):
    """Метод валидации при создании и обновлении объявления.
    Проверка статуса объявления - OPEN или CLOSED и числа не больше 10 со статусом OPEN"""

    request = self.context.get("request")
    user = request.user if request else None

    if not self.instance:
      print(f"Создание нового объявления пользователем: {user}")

    # Проверка при создании нового OPEN объявления
    if not self.instance and data.get('status') == AdvertisementStatusChoices.OPEN:
      open_ads_count = Advertisement.objects.filter(
        creator=user, 
        status=AdvertisementStatusChoices.OPEN
      ).count()
      
      # print(f"Количество открытых объявлений при добавлении: {open_ads_count}")

      if open_ads_count >= 10:
        raise ValidationError("The number of open ads is more than 10. Close one of the ads to post a new one.")

    # Проверка при обновлении, если меняется статус с CLOSED на OPEN
    if self.instance and data.get('status') == AdvertisementStatusChoices.OPEN:
      current_status = self.instance.status
      if current_status == AdvertisementStatusChoices.CLOSED:
        open_ads_count = Advertisement.objects.filter(
          creator=user, 
          status=AdvertisementStatusChoices.OPEN
        ).count()

        # print(f"Количество открытых объявлений при открытии: {open_ads_count}")

        if open_ads_count >= 10:
          raise ValidationError("The number of open ads is more than 10. Close one of the ads to open a new one.")

    return data




# class AdvertisementSerializer(serializers.ModelSerializer):
#     """Serializer для объявления."""

#     creator = UserSerializer(
#         read_only=True,
#     )

#     class Meta:
#         model = Advertisement
#         fields = ('id', 'title', 'description', 'creator',
#                   'status', 'created_at', )

#     def create(self, validated_data):
#         """Метод для создания"""

#         # Простановка значения поля создатель по-умолчанию.
#         # Текущий пользователь является создателем объявления
#         # изменить или переопределить его через API нельзя.
#         # обратите внимание на `context` – он выставляется автоматически
#         # через методы ViewSet.
#         # само поле при этом объявляется как `read_only=True`
#         validated_data["creator"] = self.context["request"].user
#         return super().create(validated_data)

#     def validate(self, data):
#         """Метод для валидации. Вызывается при создании и обновлении."""

#         # TODO: добавьте требуемую валидацию

#         return data
