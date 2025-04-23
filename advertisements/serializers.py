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
    
    request = self.context['request']
    user = request.user

  # Получаем предполагаемый статус объявления (с учётом update)
    new_status = data.get('status', getattr(self.instance, 'status', None))

    if new_status == AdvertisementStatusChoices.OPEN:
    # Исключаем текущее объявление из подсчёта, если обновляем
      ads = Advertisement.objects.filter(creator=user, status=AdvertisementStatusChoices.OPEN)
      if self.instance:
        ads = ads.exclude(id=self.instance.id)
      if ads.count() >= 10:
        raise ValidationError("The number of open ads is 10. Close or delete one of the ads to post a new one.")
    return data