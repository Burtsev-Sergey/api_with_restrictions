from rest_framework.permissions import IsAuthenticated
from advertisements.permissions import IsAuthorOrReadOnly
from rest_framework.viewsets import ModelViewSet
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_permissions(self):
      """Метод для получения прав на действия с объявлениями."""
      if self.action in ["list", "retrieve"]:
        # Для просматра списка объявлений и выбранного объявления аутентификация не требуется.
        return []

      # Для создания, обновления и удаления включается аутентификация и проверка прав автора.
      return [IsAuthenticated(), IsAuthorOrReadOnly()]

    def perform_create(self, serializer):
      """Метод - создание объявления в базе данных."""
      serializer = AdvertisementSerializer(data=self.request.data, context={'request': self.request})
      serializer.is_valid(raise_exception=True)
      serializer.save()


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для фильтраций."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter
