from rest_framework import viewsets, permissions
from .models import Auditoria
from .serializers import AuditoriaSerializer

class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.all().order_by('-fecha')
    serializer_class = AuditoriaSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = self.queryset
        params = self.request.query_params
        if modelo := params.get('modelo'):
            qs = qs.filter(modelo=modelo)
        if usuario := params.get('usuario'):
            qs = qs.filter(usuario_id=usuario)
        return qs
