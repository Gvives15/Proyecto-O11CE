from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_dni(self, value: str) -> str:
        qs = Cliente.objects.filter(dni=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Cliente con este DNI ya existe.')
        return value

    def validate_email(self, value: str) -> str:
        qs = Cliente.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Cliente con este email ya existe.')
        return value
