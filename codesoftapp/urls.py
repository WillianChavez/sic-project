from django.urls import path
from . import views
urlpatterns = [
    ##login
    path('', views.inicio, name='inicio'),
    path('login', views.inicio),
    path('logout', views.logout_view),

    ##catalogo de cuentas
    path('catalogo_cuentas', views.catalogo),

    ##control de costos
    path('control_costos', views.control),
    path('costos_indirectos_fabricacion', views.indirectos),
    path('mano_de_obra_directa', views.manoobra),

    ##estados financieros
    path('estados_financieros', views.estados),

    path('balance_comprobacion', views.comprobacion, name='balance_comprobacion'),
    path('ajustes', views.ajustes),
    path('balance_ajustado', views.ajustado),
    path('estado_resultados', views.resultados, name='estado_resultados'),
    path('estado_capital', views.capital),
    path('balance_general', views.general),

    ##transacciones
    path('transacciones', views.transacciones),
    
    path('agregar_cuenta', views.agregar_cuenta, name='agregar_cuenta'),
    path('agregar_transaccion', views.agregar_transaccion, name='agregar_transaccion'),
    path('crear_periodo', views.crear_periodo, name='crear_periodo'),
    path('filtrar_transacciones', views.filtrar_transacciones, name='filtrar_transacciones'),

    path('modificar_transaccion/<int:transaccion_id>/', views.modificar_transaccion, name='modificar_transaccion'),
    path('eliminar_transaccion/<int:transaccion_id>/', views.eliminar_transaccion, name='eliminar_transaccion'),
    path('actualizar_resumen_cuentas', views.actualizar_resumen_cuentas, name='actualizar_resumen_cuentas'),
    path('libro_mayor', views.libro_mayor, name='libro_mayor'),
    path('agregar_empleado', views.agregar_empleado, name='agregar_empleado'),
    path('modificar_empleado/<int:empleado_id>/', views.modificar_empleado, name='modificar_empleado'),
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('agregar_a_partida_doble', views.agregar_a_partida_doble, name='agregar_a_partida_doble'),
]