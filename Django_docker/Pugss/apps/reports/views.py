from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .pagination import OptionalPageNumberPagination
from . import models, serializers, filters


# Create your views here.


class RecordViewSet(ReadOnlyModelViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = filters.RecordFilterSet
    pagination_class = OptionalPageNumberPagination

    @action(methods=['GET'], detail=True)
    def report(self, request, *args, **kwargs):
        #  获取模型对象
        record_obj = self.get_object()
        report_obj = record_obj.report
        serializer = serializers.ReportSerializer(instance=report_obj)
        return Response(serializer.data)


class ReportViewSet(ReadOnlyModelViewSet):
    queryset = models.Report.objects.all()
    serializer_class = serializers.ReportSerializer
    permission_classes = [IsAuthenticated]
