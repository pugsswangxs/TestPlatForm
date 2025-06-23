from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from . import models, serializers

# Create your views here.
class BugViewSet(ModelViewSet):
    queryset = models.Bug.objects.all()
    serializer_class = serializers.BugSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'interface']


class BugHandlerViewSet(ModelViewSet):
    queryset = models.BugHandle.objects.all()
    serializer_class = serializers.BugHandlerSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['bug']
