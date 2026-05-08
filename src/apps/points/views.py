from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Container
from .serializers import ContainerSerializer


class ContainerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para consultar contenedores de reciclaje.
    ReadOnly — solo GET en el MVP.
    """
    queryset = Container.objects.select_related(
        "recycling_point",
    ).prefetch_related(
        "waste_subcategories__category",  # evita N+1
    ).order_by("id")

    serializer_class = ContainerSerializer

    # Permite filtrar por ?status=active o ?recycling_point=1
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "recycling_point__name"]

    @action(detail=False, methods=["get"], url_path="by-point/(?P<point_id>[^/.]+)")
    def by_point(self, request, point_id=None):
        """
        GET /api/v1/containers/by-point/1/
        Retorna todos los contenedores de un punto específico.
        """
        containers = self.get_queryset().filter(recycling_point_id=point_id)
        serializer = self.get_serializer(containers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="full")
    def full(self, request):
        """
        GET /api/v1/containers/full/
        Retorna contenedores con fill_level >= 80%.
        """
        containers = self.get_queryset().filter(fill_level__gte=80)
        serializer = self.get_serializer(containers, many=True)
        return Response(serializer.data)