from django.db import transaction

from entrenadores.models import Entrenador
from jugadores.models import Jugador
from .models import Cruce

# Orden importante: los cuartos se resuelven antes que las semis, y estas antes que la final
ESTRUCTURA = [
    ('cuartos', 1), ('cuartos', 2), ('cuartos', 3), ('cuartos', 4),
    ('semis', 1), ('semis', 2),
    ('final', 1),
]
# De qué cruces salen los dos equipos de cada cruce posterior
ALIMENTA = {
    ('semis', 1): (('cuartos', 1), ('cuartos', 2)),
    ('semis', 2): (('cuartos', 3), ('cuartos', 4)),
    ('final', 1): (('semis', 1), ('semis', 2)),
}
CAMPOS = ['equipo_a', 'equipo_b', 'goles_a', 'goles_b', 'penales_a', 'penales_b']
MARCADOR = ['goles_a', 'goles_b', 'penales_a', 'penales_b']


# ---------- Lógica pura (sin base de datos) ----------

def _ganador(a, b, ga, gb, pa, pb):
    """Devuelve (ganador, estado). Estados: pendiente | empate | jugado."""
    if not a or not b or ga is None or gb is None:
        return '', 'pendiente'
    if ga > gb:
        return a, 'jugado'
    if gb > ga:
        return b, 'jugado'
    if pa is not None and pb is not None and pa != pb:
        return (a if pa > pb else b), 'jugado'
    return '', 'empate'


def resolver(datos):
    """datos: {(ronda, pos): {campos}}. Calcula equipos de rondas posteriores, ganador y estado."""
    res = {}
    for clave in ESTRUCTURA:
        d = datos[clave]
        if clave[0] == 'cuartos':
            a, b = d['equipo_a'], d['equipo_b']
        else:
            ca, cb = ALIMENTA[clave]
            a, b = res[ca]['ganador'], res[cb]['ganador']
        ganador, estado = _ganador(a, b, d['goles_a'], d['goles_b'], d['penales_a'], d['penales_b'])
        res[clave] = {
            'ronda': clave[0], 'posicion': clave[1],
            'equipo_a': a, 'equipo_b': b,
            'goles_a': d['goles_a'], 'goles_b': d['goles_b'],
            'penales_a': d['penales_a'], 'penales_b': d['penales_b'],
            'ganador': ganador, 'estado': estado,
        }
    return res


def _participantes(datos):
    r = resolver(datos)
    return {k: (v['equipo_a'], v['equipo_b']) for k, v in r.items()}


def _num(v):
    if v is None or str(v).strip() == '':
        return None
    try:
        n = int(str(v).strip())
    except ValueError:
        raise ValueError('Los goles y penales deben ser números enteros')
    if n < 0 or n > 99:
        raise ValueError('Los goles y penales deben estar entre 0 y 99')
    return n


def aplicar_entradas(datos, entradas):
    """Aplica los cambios recibidos. Solo toca los campos que vienen en cada entrada."""
    for e in entradas:
        try:
            clave = (e.get('ronda'), int(e.get('posicion')))
        except (TypeError, ValueError):
            raise ValueError('Cruce inválido')
        if clave not in datos:
            raise ValueError('Cruce inválido')
        d = datos[clave]
        if clave[0] == 'cuartos':
            for campo in ('equipo_a', 'equipo_b'):
                if campo in e:
                    d[campo] = (e.get(campo) or '').strip()[:100]
        for campo in MARCADOR:
            if campo in e:
                d[campo] = _num(e.get(campo))
        # Si no hay empate, los penales no cuentan
        if d['goles_a'] is not None and d['goles_b'] is not None and d['goles_a'] != d['goles_b']:
            d['penales_a'] = d['penales_b'] = None

    nombres = [datos[k][c].lower() for k in ESTRUCTURA[:4] for c in ('equipo_a', 'equipo_b') if datos[k][c]]
    if len(nombres) != len(set(nombres)):
        raise ValueError('Hay equipos repetidos en los cuartos de final')


def limpiar_dependientes(datos, antes):
    """Si cambió quién juega una semifinal o la final, se borra su marcador anterior."""
    for clave in ESTRUCTURA[4:]:
        ahora = _participantes(datos)[clave]
        previo = antes[clave]
        if all(previo) and ahora != previo:
            for campo in MARCADOR:
                datos[clave][campo] = None


def limpiar_sin_equipos(datos):
    """No se guardan marcadores de cruces donde todavía no se conocen los dos equipos."""
    for clave in ESTRUCTURA[4:]:
        a, b = _participantes(datos)[clave]
        if not (a and b):
            for campo in MARCADOR:
                datos[clave][campo] = None


# ---------- Base de datos ----------

def asegurar_llave(torneo):
    existentes = {(c.ronda, c.posicion) for c in torneo.cruces.all()}
    for ronda, pos in ESTRUCTURA:
        if (ronda, pos) not in existentes:
            Cruce.objects.create(torneo=torneo, ronda=ronda, posicion=pos)


def _cargar(torneo):
    asegurar_llave(torneo)
    filas = {(c.ronda, c.posicion): c for c in torneo.cruces.all()}
    datos = {k: {campo: getattr(c, campo) for campo in CAMPOS} for k, c in filas.items()}
    return filas, datos


def armar_llave(torneo):
    _, datos = _cargar(torneo)
    res = resolver(datos)
    return {
        'torneo': {'id': torneo.id, 'nombre': torneo.nombre, 'categoria': torneo.categoria.nombre},
        'cruces': [res[k] for k in ESTRUCTURA],
        'campeon': res[('final', 1)]['ganador'],
    }


@transaction.atomic
def guardar_cruces(torneo, entradas):
    filas, datos = _cargar(torneo)
    antes = _participantes(datos)
    aplicar_entradas(datos, entradas)
    limpiar_dependientes(datos, antes)
    limpiar_sin_equipos(datos)
    for k, c in filas.items():
        for campo in CAMPOS:
            setattr(c, campo, datos[k][campo])
        c.save()


# ---------- Permisos ----------

def puede_editar(user, torneo):
    rol = getattr(user, 'rol', None)
    if rol == 'directivo':
        return True
    if rol == 'entrenador':
        return Entrenador.objects.filter(usuario=user, categorias=torneo.categoria).exists()
    return False


def puede_ver(user, torneo):
    if puede_editar(user, torneo):
        return True
    if getattr(user, 'rol', None) == 'padre':
        return Jugador.objects.filter(acudiente=user, categoria=torneo.categoria).exists()
    return False