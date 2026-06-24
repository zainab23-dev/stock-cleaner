from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Trash
from .serializers import TrashSerializer

class TrashViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trash.objects.filter(restored=False)
    serializer_class = TrashSerializer
    permission_classes = [IsAuthenticated]
