from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from jugadores.models import Jugador
from pagos.models import EstadoPago
from entrenadores.models import Entrenador
from entrenamientos.models import Entrenamiento
from asistencia.models import Asistencia
from categorias.models import Categoria
from torneos.models import Torneo
from notificaciones.models import Notificacion
from django.contrib import messages
from escuelas.models import Escuela, FotoInstalacion
from escuelas.forms import EscuelaForm, FotoInstalacionForm
from usuarios.models import Usuario
from usuarios.forms import UsuarioCreateForm, UsuarioEditForm

@login_required
def dashboard(request):
    if request.user.rol == 'entrenador':
        return redirect('dashboard_entrenador')
    elif request.user.rol == 'padre':
        return redirect('mi_estado_cuenta')
    elif request.user.rol != 'directivo':
        return redirect('login')

    total_jugadores = Jugador.objects.filter(activo=True).count()
    pendientes = EstadoPago.objects.filter(estado='pendiente').count()
    abonados = EstadoPago.objects.filter(estado='abonado').count()
    cancelados = EstadoPago.objects.filter(estado='cancelado').count()

    return render(request, 'dashboard.html', {
        'total_jugadores': total_jugadores,
        'pendientes': pendientes,
        'abonados': abonados,
        'cancelados': cancelados,
    })

@login_required
def lista_jugadores(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    jugadores = Jugador.objects.all()
    return render(request, 'lista_jugadores.html', {'jugadores': jugadores})


@login_required
def lista_pagos(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    estados = EstadoPago.objects.all()
    return render(request, 'lista_pagos.html', {'estados': estados})

@login_required
def lista_categorias(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})


@login_required
def lista_entrenadores(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    entrenadores = Entrenador.objects.all()
    return render(request, 'lista_entrenadores.html', {'entrenadores': entrenadores})


@login_required
def lista_entrenamientos(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    entrenamientos = Entrenamiento.objects.all()
    return render(request, 'lista_entrenamientos.html', {'entrenamientos': entrenamientos})


@login_required
def lista_torneos(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    torneos = Torneo.objects.all()
    return render(request, 'lista_torneos.html', {'torneos': torneos})


@login_required
def lista_notificaciones(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    notificaciones = Notificacion.objects.all()
    return render(request, 'lista_notificaciones.html', {'notificaciones': notificaciones})


@login_required
def dashboard_entrenador(request):
    if request.user.rol != 'entrenador':
        return redirect('dashboard')

    entrenador = get_object_or_404(Entrenador, usuario=request.user)
    categorias = entrenador.categorias.all()
    jugadores = Jugador.objects.filter(categoria__in=categorias)
    entrenamientos = Entrenamiento.objects.filter(entrenador=entrenador)
    asistencias = Asistencia.objects.filter(jugador__categoria__in=categorias)
    escuela = Escuela.objects.first()  # ajusta esto si manejas varias escuelas

    return render(request, 'dashboard_entrenador.html', {
        'entrenador': entrenador,
        'categorias': categorias,
        'jugadores': jugadores,
        'entrenamientos': entrenamientos,
        'asistencias': asistencias,
        'escuela': escuela,
    })

@login_required
def pasar_asistencia(request):
    if request.user.rol != 'entrenador':
        return redirect('dashboard')
    entrenador = get_object_or_404(Entrenador, usuario=request.user)
    entrenamientos = Entrenamiento.objects.filter(entrenador=entrenador)

    entrenamiento_id = request.GET.get('entrenamiento')
    jugadores = []
    entrenamiento_actual = None

    if entrenamiento_id:
        entrenamiento_actual = get_object_or_404(Entrenamiento, id=entrenamiento_id)
        jugadores = Jugador.objects.filter(categoria=entrenamiento_actual.categoria)

        if request.method == 'POST':
            for jugador in jugadores:
                presente = request.POST.get(f'presente_{jugador.id}') == 'on'
                Asistencia.objects.update_or_create(
                    entrenamiento=entrenamiento_actual,
                    jugador=jugador,
                    defaults={'presente': presente}
                )
            return redirect('pasar_asistencia')

    return render(request, 'pasar_asistencia.html', {
        'entrenamientos': entrenamientos,
        'entrenamiento_actual': entrenamiento_actual,
        'jugadores': jugadores,
    })


@login_required
def mi_estado_cuenta(request):
    if request.user.rol != 'padre':
        return redirect('dashboard')
    estados = EstadoPago.objects.filter(jugador__acudiente=request.user)
    return render(request, 'mi_estado_cuenta.html', {'estados': estados})


@login_required
def asistencia_hijo(request):
    if request.user.rol != 'padre':
        return redirect('dashboard')
    registros = Asistencia.objects.filter(jugador__acudiente=request.user)
    return render(request, 'asistencia_hijo.html', {'registros': registros})

@login_required
def lista_escuelas(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    escuelas = Escuela.objects.all()
    return render(request, 'lista_escuelas.html', {'escuelas': escuelas})


@login_required
def crear_escuela(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    if request.method == 'POST':
        form = EscuelaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escuela creada correctamente.')
            return redirect('lista_escuelas')
    else:
        form = EscuelaForm()
    return render(request, 'form_escuela.html', {'form': form})


@login_required
def editar_escuela(request, escuela_id):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    escuela = get_object_or_404(Escuela, id=escuela_id)
    if request.method == 'POST':
        form = EscuelaForm(request.POST, request.FILES, instance=escuela)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escuela actualizada.')
            return redirect('lista_escuelas')
    else:
        form = EscuelaForm(instance=escuela)
    return render(request, 'form_escuela.html', {'form': form})


@login_required
def lista_usuarios(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    usuarios = Usuario.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})


@login_required
def crear_usuario(request):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioCreateForm()
    return render(request, 'form_usuario.html', {'form': form, 'modo': 'crear'})


@login_required
def editar_usuario(request, usuario_id):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'form_usuario.html', {'form': form, 'modo': 'editar'})

@login_required
def mis_entrenamientos_hijo(request):
    if request.user.rol != 'padre':
        return redirect('dashboard')

    jugadores = Jugador.objects.filter(acudiente=request.user)
    categorias = jugadores.values_list('categoria', flat=True)

    entrenamientos = Entrenamiento.objects.filter(categoria__in=categorias)
    torneos = Torneo.objects.filter(categoria__in=categorias)

    return render(request, 'entrenamientos_hijo.html', {
        'jugadores': jugadores,
        'entrenamientos': entrenamientos,
        'torneos': torneos,
    })

@login_required
def mis_notificaciones(request):
    if request.user.rol != 'padre':
        return redirect('dashboard')

    notificaciones = Notificacion.objects.filter(destinatario=request.user)
    return render(request, 'mis_notificaciones.html', {'notificaciones': notificaciones})

from usuarios.forms import NotificacionForm

@login_required
def notificaciones_entrenador(request):
    if request.user.rol != 'entrenador':
        return redirect('dashboard')

    entrenador = get_object_or_404(Entrenador, usuario=request.user)
    categorias = entrenador.categorias.all()
    jugadores = Jugador.objects.filter(categoria__in=categorias)
    padres_ids = jugadores.values_list('acudiente', flat=True)

    enviadas = Notificacion.objects.filter(destinatario__in=padres_ids)
    return render(request, 'notificaciones_entrenador.html', {'enviadas': enviadas})


@login_required
def enviar_notificacion(request):
    if request.user.rol not in ['entrenador', 'directivo']:
        return redirect('dashboard')

    entrenador = Entrenador.objects.filter(usuario=request.user).first()
    if entrenador:
        categorias = entrenador.categorias.all()
        jugadores = Jugador.objects.filter(categoria__in=categorias)
        padres_ids = jugadores.values_list('acudiente', flat=True)
        queryset_padres = Usuario.objects.filter(id__in=padres_ids)
    else:
        queryset_padres = Usuario.objects.filter(rol='padre')

    if request.method == 'POST':
        form = NotificacionForm(request.POST)
        form.fields['destinatario'].queryset = queryset_padres
        if form.is_valid():
            Notificacion.objects.create(
                destinatario=form.cleaned_data['destinatario'],
                titulo=form.cleaned_data['titulo'],
                mensaje=form.cleaned_data['mensaje'],
            )
            messages.success(request, 'Notificación enviada correctamente.')
            return redirect('notificaciones_entrenador')
    else:
        form = NotificacionForm()
        form.fields['destinatario'].queryset = queryset_padres

    return render(request, 'form_notificacion.html', {'form': form})


@login_required
def info_escuela(request):
    escuela = request.user.escuela or Escuela.objects.first()
    fotos = escuela.fotos.all() if escuela else []
    return render(request, 'info_escuela.html', {'escuela': escuela, 'fotos': fotos})


@login_required
def fotos_escuela(request, escuela_id):
    if request.user.rol != 'directivo':
        return redirect('dashboard')
    escuela = get_object_or_404(Escuela, id=escuela_id)
    if request.method == 'POST':
        form = FotoInstalacionForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.escuela = escuela
            foto.save()
            messages.success(request, 'Foto agregada correctamente.')
            return redirect('fotos_escuela', escuela_id=escuela.id)
    else:
        form = FotoInstalacionForm()
    return render(request, 'fotos_escuela.html', {
        'escuela': escuela,
        'fotos': escuela.fotos.all(),
        'form': form,
    })

@login_required
def eliminar_foto(request, foto_id):
    if request.user.rol != 'directivo' or request.method != 'POST':
        return redirect('dashboard')
    foto = get_object_or_404(FotoInstalacion, id=foto_id)
    escuela_id = foto.escuela_id
    foto.delete()
    messages.success(request, 'Foto eliminada.')
    return redirect('fotos_escuela', escuela_id=escuela_id)