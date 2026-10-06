from rest_framework import serializers
from .models import EstadoPago, Abono

class AbonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abono
        fields = '__all__'

class EstadoPagoSerializer(serializers.ModelSerializer):
    valor_abonado = serializers.ReadOnlyField()
    saldo_pendiente = serializers.ReadOnlyField()
    abonos = AbonoSerializer(many=True, read_only=True)

    class Meta:
        model = EstadoPago
        fields = '__all__'