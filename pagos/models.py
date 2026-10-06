from django.db import models

# Create your models here.
from jugadores.models import Jugador

class EstadoPago(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('abonado', 'Abonado'),
        ('cancelado', 'Cancelado'),
    ]
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='estados_pago')
    mes = models.CharField(max_length=20, help_text="Ej: Enero 2026")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    @property
    def valor_abonado(self):
        # Suma todos los abonos registrados para esta mensualidad
        return sum(abono.valor for abono in self.abonos.all())

    @property
    def saldo_pendiente(self):
        return self.valor_total - self.valor_abonado

    def actualizar_estado(self):
        # Esta es la función que decide automáticamente el estado
        if self.valor_abonado >= self.valor_total:
            self.estado = 'cancelado'       # ya pagó todo
        elif self.valor_abonado > 0:
            self.estado = 'abonado'         # pagó una parte
        else:
            self.estado = 'pendiente'       # no ha pagado nada
        self.save()

    def __str__(self):
        return f"{self.jugador.nombre_completo} - {self.mes} ({self.estado})"


class Abono(models.Model):
    # Cada vez que alguien paga (todo o parte), se crea UNO de estos registros
    estado_pago = models.ForeignKey(EstadoPago, on_delete=models.CASCADE, related_name='abonos')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)   # se guarda sola, el día que se registra
    metodo = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"${self.valor} - {self.fecha}"