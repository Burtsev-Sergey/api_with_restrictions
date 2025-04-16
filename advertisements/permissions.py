from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
  """Разрешение, позволяющее редактировать объект только его автору."""

  def has_object_permission(self, request, view, obj):
    # Разрешаем чтение любому пользователю - возвращаем True для безопасных методов.
    if request.method in ('GET', 'HEAD', 'OPTIONS'):
      return True

    # Если это небезопасный метод PUT, PATCH, DELETE - проверка пользователь автор или нет.
    return obj.creator == request.user
