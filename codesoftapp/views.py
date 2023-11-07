from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Cuenta, Transaccion, ResumenCuentas, Periodo, ManoDeObra
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models import Sum, FloatField, Case, When, F, Value, IntegerField, DecimalField
from decimal import Decimal


# Vista para la página de inicio
@login_required
def inicio(request):
    return render(request, 'index.html')

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('/')

# Vista para mostrar el catálogo de cuentas
@login_required
def catalogo(request):
    cuentas = Cuenta.objects.all().order_by('codigo')
    return render(request, 'catalogo/catalogo.html', {'cuentas': cuentas})

# Vistas relacionadas con el control de costos
@login_required
def control(request):
    return render(request, 'controlcostos/controlcostos.html')

@login_required
def indirectos(request):
    return render(request, 'controlcostos/indirectos.html')

@login_required
def manoobra(request):
    registros = ManoDeObra.objects.all()
    # Recalcula las sumas totales después de eliminar el empleado
    suma_pago_diario = ManoDeObra.objects.aggregate(Sum('pago_diario'))['pago_diario__sum']
    suma_septimo_dia = ManoDeObra.objects.aggregate(Sum('septimo_dia'))['septimo_dia__sum']
    suma_vacaciones = ManoDeObra.objects.aggregate(Sum('vacaciones'))['vacaciones__sum']
    suma_salario_cancelado = ManoDeObra.objects.aggregate(Sum('salario_cancelado'))['salario_cancelado__sum']
    suma_aguinaldo = ManoDeObra.objects.aggregate(Sum('aguinaldo'))['aguinaldo__sum']
    suma_iss = ManoDeObra.objects.aggregate(Sum('iss'))['iss__sum']
    suma_afp = ManoDeObra.objects.aggregate(Sum('afp'))['afp__sum']
    suma_insaforp = ManoDeObra.objects.aggregate(Sum('insaforp'))['insaforp__sum']
    suma_costo_real = ManoDeObra.objects.aggregate(Sum('costo_real'))['costo_real__sum']
    total = suma_costo_real
    periodos = Periodo.objects.all()
    return render(request, 'controlcostos/manoobra.html', {'registros': registros,
        'suma_pago_diario': suma_pago_diario,
        'suma_septimo_dia': suma_septimo_dia,
        'suma_vacaciones': suma_vacaciones,
        'suma_salario_cancelado': suma_salario_cancelado,
        'suma_aguinaldo': suma_aguinaldo,
        'suma_iss': suma_iss,
        'suma_afp': suma_afp,
        'suma_insaforp': suma_insaforp,
        'suma_costo_real': suma_costo_real,
        'periodos':periodos})

# Vistas relacionadas con los estados financieros
@login_required
def estados(request):
    return render(request, 'estadosfinancieros/estadosfinancieros.html')

@login_required
def comprobacion(request, periodo_id=None):
    if request.method == 'POST':
        periodo_id = request.POST.get('periodo')
        
    periodos = Periodo.objects.all()
    periodo_seleccionado = None
    if periodo_id:
        periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)
        if not periodo_seleccionado:
            periodo_seleccionado = None
    
    consulta = Cuenta.objects.filter(resumen_cuentas__isnull=False, resumen_cuentas__periodo=periodo_seleccionado)
    consulta = consulta.values('codigo', 'nombre', 'resumen_cuentas__debe_total', 'resumen_cuentas__haber_total', 'resumen_cuentas__saldo')
    resultados = []
    suma_debe_total = Decimal(0)  # Inicializa la suma del debe
    suma_haber_total = Decimal(0)  # Inicializa la suma del haber
    
    for cuenta in consulta:
        if '1000' <= cuenta['codigo'] <= '1203':
            cuenta['resumen_cuentas__debe_total'] = cuenta['resumen_cuentas__saldo']
            cuenta['resumen_cuentas__haber_total'] = 0
            if(cuenta['resumen_cuentas__debe_total'] < 0):
                cuenta['resumen_cuentas__haber_total'] = -1* (cuenta['resumen_cuentas__debe_total'])
                cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__haber_total'] < 0):
                cuenta['resumen_cuentas__debe_total'] = -1* (cuenta['resumen_cuentas__haber_total'])
                cuenta['resumen_cuentas__haber_total'] = 0

        elif '2101' <= cuenta['codigo'] <= '3102':
            cuenta['resumen_cuentas__haber_total'] = cuenta['resumen_cuentas__saldo']
            cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__debe_total'] < 0):
                cuenta['resumen_cuentas__haber_total'] = -1* (cuenta['resumen_cuentas__debe_total'])
                cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__haber_total'] < 0):
                cuenta['resumen_cuentas__debe_total'] = -1* (cuenta['resumen_cuentas__haber_total'])
                cuenta['resumen_cuentas__haber_total'] = 0

        elif '4101' <= cuenta['codigo'] <= '4112':
            cuenta['resumen_cuentas__debe_total'] = cuenta['resumen_cuentas__saldo']
            cuenta['resumen_cuentas__haber_total'] = 0
            if(cuenta['resumen_cuentas__debe_total'] < 0):
                cuenta['resumen_cuentas__haber_total'] = -1* (cuenta['resumen_cuentas__debe_total'])
                cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__haber_total'] < 0):
                cuenta['resumen_cuentas__debe_total'] = -1* (cuenta['resumen_cuentas__haber_total'])
                cuenta['resumen_cuentas__haber_total'] = 0

        elif '510101' <= cuenta['codigo'] <= '510202':
            cuenta['resumen_cuentas__haber_total'] = cuenta['resumen_cuentas__saldo']
            cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__debe_total'] < 0):
                cuenta['resumen_cuentas__haber_total'] = -1* (cuenta['resumen_cuentas__debe_total'])
                cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__haber_total'] < 0):
                cuenta['resumen_cuentas__debe_total'] = -1* (cuenta['resumen_cuentas__haber_total'])
                cuenta['resumen_cuentas__haber_total'] = 0
        
        resultados.append(cuenta)
        
        suma_debe_total += cuenta['resumen_cuentas__debe_total']
        suma_haber_total += cuenta['resumen_cuentas__haber_total']
    if(suma_debe_total < 0):
        suma_haber_total = -1*(suma_debe_total)
        suma_debe_total=0

    if(suma_haber_total < 0):
        suma_debe_total = -1*(suma_haber_total)
        suma_haber_total=0
    return render(request, 'estadosfinancieros/comprobacion.html', {
            'resultados': resultados,
            'suma_debe_total': suma_debe_total,
            'suma_haber_total': suma_haber_total,
            'periodos': periodos,
            'periodo_seleccionado': periodo_seleccionado,
        })

@login_required
def ajustes(request):
    return render(request, 'estadosfinancieros/ajustes.html')

@login_required
def ajustado(request):
    return render(request, 'estadosfinancieros/ajustado.html')

@login_required
def general(request):
    periodos = Periodo.objects.all()
    return render(request, 'estadosfinancieros/general.html', {'periodos': periodos})

from decimal import Decimal
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from django.db.models.functions import Coalesce

@login_required
def resultados(request, periodo_id=None):
    if request.method == 'POST':
        periodo_id = request.POST.get('periodo')
        
    periodos = Periodo.objects.all()
    periodo_seleccionado = None
    
    if periodo_id:
        periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

    consultas = Cuenta.objects.filter(
        resumen_cuentas__isnull=False,
        resumen_cuentas__periodo=periodo_seleccionado,
        codigo__in=['4101', '4102', '4103', '4104', '4105', '4106', '4107', '4108', '4109', '4110', '4111', '4112', '510101', '510102']
    ).annotate(
        debe_total=Coalesce(F('resumen_cuentas__debe_total'), 0),
        haber_total=Coalesce(F('resumen_cuentas__haber_total'), 0)
    )

    ##4101
    suma_debe_total1 = consultas.filter(codigo='4101').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total1 = consultas.filter(codigo='4101').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total1 < 0:
        suma_haber_total1 = -1 * suma_debe_total1
        suma_debe_total1 = Decimal(0)

    if suma_haber_total1 < 0:
        suma_debe_total1 = -1 * suma_haber_total1
        suma_haber_total1 = Decimal(0)

    ### 4102
    suma_debe_total2 = consultas.filter(codigo='4102').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total2 = consultas.filter(codigo='4101').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total2 < 0:
        suma_haber_total2 = -1 * suma_debe_total2
        suma_debe_total2 = Decimal(0)

    if suma_haber_total2 < 0:
        suma_debe_total2 = -1 * suma_haber_total2
        suma_haber_total2 = Decimal(0)

    ## 4103
    suma_debe_total3 = consultas.filter(codigo='4103').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total3 = consultas.filter(codigo='4103').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total3 < 0:
        suma_haber_total3 = -1 * suma_debe_total3
        suma_debe_total3 = Decimal(0)

    if suma_haber_total3 < 0:
        suma_debe_total3 = -1 * suma_haber_total3
        suma_haber_total3 = Decimal(0)

    ## 4104
    suma_debe_total4 = consultas.filter(codigo='4104').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total4 = consultas.filter(codigo='4104').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total4 < 0:
        suma_haber_total4 = -1 * suma_debe_total4
        suma_debe_total4 = Decimal(0)

    if suma_haber_total4 < 0:
        suma_debe_total4 = -1 * suma_haber_total4
        suma_haber_total4 = Decimal(0)

    ## 4105
    suma_debe_total5 = consultas.filter(codigo='4105').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total5 = consultas.filter(codigo='4105').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total5 < 0:
        suma_haber_total5 = -1 * suma_debe_total5
        suma_debe_total5 = Decimal(0)

    if suma_haber_total5 < 0:
        suma_debe_total5 = -1 * suma_haber_total5
        suma_haber_total5 = Decimal(0)

    ## 4106
    suma_debe_total6 = consultas.filter(codigo='4106').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total6 = consultas.filter(codigo='4106').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total6 < 0:
        suma_haber_total6 = -1 * suma_debe_total6
        suma_debe_total6 = Decimal(0)

    if suma_haber_total6 < 0:
        suma_debe_total6 = -1 * suma_haber_total6
        suma_haber_total6 = Decimal(0)

    ## 4107
    suma_debe_total7 = consultas.filter(codigo='4107').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total7 = consultas.filter(codigo='4107').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total7 < 0:
        suma_haber_total7 = -1 * suma_debe_total7
        suma_debe_total7 = Decimal(0)

    if suma_haber_total7 < 0:
        suma_debe_total7 = -1 * suma_haber_total7
        suma_haber_total7 = Decimal(0)

    ## 4108
    suma_debe_total8 = consultas.filter(codigo='4108').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total8 = consultas.filter(codigo='4108').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total8 < 0:
        suma_haber_total8 = -1 * suma_debe_total8
        suma_debe_total8 = Decimal(0)

    if suma_haber_total8 < 0:
        suma_debe_total8 = -1 * suma_haber_total8
        suma_haber_total8 = Decimal(0)
    
    ## 4109
    suma_debe_total9 = consultas.filter(codigo='4109').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total9 = consultas.filter(codigo='4109').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total9 < 0:
        suma_haber_total9 = -1 * suma_debe_total9
        suma_debe_total9 = Decimal(0)

    if suma_haber_total9 < 0:
        suma_debe_total9 = -1 * suma_haber_total9
        suma_haber_total9 = Decimal(0)

    ## 4110
    suma_debe_total10 = consultas.filter(codigo='4110').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total10 = consultas.filter(codigo='4110').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total10 < 0:
        suma_haber_total10 = -1 * suma_debe_total10
        suma_debe_total10 = Decimal(0)

    if suma_haber_total10 < 0:
        suma_debe_total10 = -1 * suma_haber_total10
        suma_haber_total10 = Decimal(0)
    
    ## 4111
    suma_debe_total11 = consultas.filter(codigo='4111').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total11 = consultas.filter(codigo='4111').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total11 < 0:
        suma_haber_total11 = -1 * suma_debe_total11
        suma_debe_total11 = Decimal(0)

    if suma_haber_total11 < 0:
        suma_debe_total11 = -1 * suma_haber_total11
        suma_haber_total11 = Decimal(0)

    ## 4112
    suma_debe_total12 = consultas.filter(codigo='4112').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total12 = consultas.filter(codigo='4112').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total12 < 0:
        suma_haber_total12 = -1 * suma_debe_total12
        suma_debe_total12 = Decimal(0)

    if suma_haber_total12 < 0:
        suma_debe_total12 = -1 * suma_haber_total12
        suma_haber_total12 = Decimal(0)

    ## 510101
    suma_debe_total13 = consultas.filter(codigo='510101').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total13 = consultas.filter(codigo='510101').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total13 < 0:
        suma_haber_total13 = -1 * suma_debe_total13
        suma_debe_total13 = Decimal(0)

    if suma_haber_total13 < 0:
        suma_debe_total13 = -1 * suma_haber_total13
        suma_haber_total13 = Decimal(0)
    
    ## 510102
    suma_debe_total14 = consultas.filter(codigo='510102').aggregate(
        Sum('debe_total', output_field=DecimalField())
    )['debe_total__sum'] or Decimal(0)

    suma_haber_total14 = consultas.filter(codigo='510102').aggregate(
        Sum('haber_total', output_field=DecimalField())
    )['haber_total__sum'] or Decimal(0)

    if suma_debe_total14 < 0:
        suma_haber_total14 = -1 * suma_debe_total14
        suma_debe_total14 = Decimal(0)

    if suma_haber_total14 < 0:
        suma_debe_total14 = -1 * suma_haber_total14
        suma_haber_total14 = Decimal(0)
#### lo demas ############
    suma_debe = (suma_debe_total1 + suma_debe_total2 + suma_debe_total3 + 
                 suma_debe_total4 + suma_debe_total5 + suma_debe_total6 + 
                 suma_debe_total7 + suma_debe_total8 + suma_debe_total9 + 
                 suma_debe_total10 + suma_debe_total11 + suma_debe_total12 + 
                 suma_debe_total13 + suma_debe_total14)
    suma_haber = (suma_haber_total1 + suma_haber_total2 + suma_haber_total3 + 
                  suma_haber_total4 + suma_haber_total5 + suma_haber_total6 +
                  suma_haber_total7 + suma_haber_total8 + suma_haber_total9 +
                  suma_haber_total10 + suma_haber_total11 + suma_haber_total12 +
                  suma_haber_total13 + suma_haber_total14)

    utilidades_haber = suma_haber - suma_debe
    utilidades_debe = 0
    if utilidades_haber < 0:
        utilidades_debe = utilidades_haber * -1
        utilidades_haber = 0

    return render(request, 'estadosfinancieros/resultados.html', {
        'suma_debe_total1': suma_debe_total1,
        'suma_haber_total1': suma_haber_total1,
        'suma_debe_total2': suma_debe_total2,
        'suma_haber_total2': suma_haber_total2,
        'suma_debe_total3': suma_debe_total3,
        'suma_haber_total3': suma_haber_total3,
        'suma_debe_total4': suma_debe_total4,
        'suma_haber_total4': suma_haber_total4,
        'suma_debe_total5': suma_debe_total5,
        'suma_haber_total5': suma_haber_total5,
        'suma_debe_total6': suma_debe_total6,
        'suma_haber_total6': suma_haber_total6,
        'suma_debe_total7': suma_debe_total7,
        'suma_haber_total7': suma_haber_total7,
        'suma_debe_total8': suma_debe_total8,
        'suma_haber_total8': suma_haber_total8,
        'suma_debe_total9': suma_debe_total9,
        'suma_haber_total9': suma_haber_total9,
        'suma_debe_total10': suma_debe_total10,
        'suma_haber_total10': suma_haber_total10,
        'suma_debe_total11': suma_debe_total11,
        'suma_haber_total11': suma_haber_total11,
        'suma_debe_total12': suma_debe_total12,
        'suma_haber_total12': suma_haber_total12,
        'suma_debe_total13': suma_debe_total13,
        'suma_haber_total13': suma_haber_total13,
        'suma_debe_total14': suma_debe_total14,
        'suma_haber_total14': suma_haber_total14,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'utilidades_haber': utilidades_haber,
        'utilidades_debe':utilidades_debe,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
    })


@login_required
def capital(request):
    periodos = Periodo.objects.all()
    return render(request, 'estadosfinancieros/capital.html', {'periodos': periodos})

# Vistas relacionadas con las transacciones
@login_required
def transacciones(request, periodo_id=None):
    periodos = Periodo.objects.all()
    periodo_seleccionado = None

    if periodo_id:
        periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

    if not periodo_seleccionado:
        periodo_seleccionado = None

    transacciones = Transaccion.objects.filter(periodo=periodo_seleccionado).order_by('codigo')
    cuentas = Cuenta.objects.all().order_by('codigo')
    suma_debe = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
    
    return render(request, 'transacciones/transacciones.html', {
        'cuentas': cuentas,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
    })

@login_required
def agregar_cuenta(request):
    cuentas = Cuenta.objects.all().order_by('codigo')
    error_message = None

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')

        cuenta_existente = Cuenta.objects.filter(Q(codigo=codigo) | Q(nombre=nombre)).first()

        if cuenta_existente:
            error_message = "Una cuenta con el mismo código o nombre ya existe en la base de datos."
        else:
            nueva_cuenta = Cuenta(codigo=codigo, nombre=nombre)
            nueva_cuenta.save()
    
    return render(request, 'catalogo/catalogo.html', {'cuentas': cuentas, 'error_message': error_message})

@login_required
def agregar_transaccion(request, periodo_id=None):
    periodos = Periodo.objects.all()
    periodo_seleccionado = None
    cuentas = Cuenta.objects.all().order_by('codigo')

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        fecha = request.POST.get('fecha')
        descripcion = request.POST.get('descripcion')
        movimiento_debe = request.POST.get('movimiento_debe', 0)
        movimiento_haber = request.POST.get('movimiento_haber', 0)
        periodo_id = request.POST.get('periodo')

        if periodo_id:
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)
        if not periodo_seleccionado:
            periodo_seleccionado = None
        transacciones = Transaccion.objects.filter(periodo_id=periodo_id)
        cuenta = Cuenta.objects.get(codigo=codigo)
        nueva_transaccion = Transaccion(
            codigo=cuenta,
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            periodo_id = periodo_id
        )
        nueva_transaccion.save()

    suma_debe = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)

    return render(request, 'transacciones/transacciones.html', {
        'transacciones': transacciones,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
        'cuentas':cuentas
    })

def modificar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, pk=transaccion_id)
    
    if request.method == 'POST':
        if 'codigo' in request.POST:
            codigo_cuenta = request.POST['codigo']
            cuenta = Cuenta.objects.get(codigo=codigo_cuenta)  # Encuentra la cuenta con el código proporcionado
            transaccion.codigo = cuenta  # Asigna la cuenta a la transacción
        if 'fecha' in request.POST:
            transaccion.fecha = request.POST['fecha']
        if 'descripcion' in request.POST:
            transaccion.descripcion = request.POST['descripcion']
        if 'movimiento_debe' in request.POST:
            transaccion.movimiento_debe = request.POST['movimiento_debe']
        else:
            transaccion.movimiento_debe = 0
        if 'movimiento_haber' in request.POST:
            transaccion.movimiento_haber = request.POST['movimiento_haber']
        else:
            transaccion.movimiento_haber = 0
        transaccion.save()
    
    periodos = Periodo.objects.all()
    periodo_seleccionado = None

    if request.method == 'POST':
        periodo_id = request.POST.get('periodo-select', 'Ninguno')  # Obtén el ID del período desde el formulario
        if periodo_id != 'Ninguno':
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

    transacciones = Transaccion.objects.filter(periodo=periodo_seleccionado).order_by('fecha')
    suma_debe = transacciones.aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = transacciones.aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
    cuentas = Cuenta.objects.all().order_by('codigo')

    return render(request, 'transacciones/transacciones.html', {
        'transaccion': transaccion,
        'transacciones': transacciones,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'cuentas': cuentas,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
    })



@login_required
def eliminar_transaccion(request, transaccion_id):
    transaccion = Transaccion.objects.get(id=transaccion_id)
    transaccion.delete()

    transacciones = Transaccion.objects.filter(periodo=transaccion.periodo).order_by('fecha')
    suma_debe = Transaccion.objects.filter(periodo=transaccion.periodo).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = Transaccion.objects.filter(periodo=transaccion.periodo).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
    cuentas = Cuenta.objects.all().order_by('codigo')

    return redirect('/transacciones', {
        'transaccion': transaccion,
        'transacciones': transacciones,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'cuentas': cuentas,
    })


@login_required
def libro_mayor(request, periodo_id=None):
    if request.method == 'POST':
        periodo_id = request.POST.get('periodo')
        periodos = Periodo.objects.all()
        periodo_seleccionado = None

        if periodo_id:
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

        if not periodo_seleccionado:
            periodo_seleccionado = None

        consulta = Cuenta.objects.filter(resumen_cuentas__isnull=False, resumen_cuentas__periodo=periodo_seleccionado)
        consulta = consulta.values('codigo', 'nombre', 'resumen_cuentas__debe_total', 'resumen_cuentas__haber_total', 'resumen_cuentas__saldo')
        resultados = consulta.all()
    else:
        periodos = Periodo.objects.all()
        periodo_seleccionado = None

        if periodo_id:
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

        if not periodo_seleccionado:
            periodo_seleccionado = None

        consulta = Cuenta.objects.filter(resumen_cuentas__isnull=False, resumen_cuentas__periodo=periodo_seleccionado)
        consulta = consulta.values('codigo', 'nombre', 'resumen_cuentas__debe_total', 'resumen_cuentas__haber_total', 'resumen_cuentas__saldo')
        resultados = consulta.all()
        resultados = resultados.order_by('codigo')

    return render(request, 'transacciones/libromayor.html', {
        'resultados': resultados,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
    })

@login_required
def crear_periodo(request, periodo_id=None):
    if request.method == 'POST':
        nombre_periodo = request.POST.get('nombre_periodo')

        # Encuentra el último período creado
        ultimo_periodo = Periodo.objects.order_by('-codigo').first()
        nuevo_codigo = 1  # Valor predeterminado si no hay ningún período existente

        if ultimo_periodo:
            # Si hay períodos existentes, incrementa el código en 1
            nuevo_codigo = int(ultimo_periodo.codigo) + 1

        # Convierte nuevo_codigo a una cadena
        nuevo_codigo = str(nuevo_codigo)

        # Crea el nuevo período con el código generado
        nuevo_periodo = Periodo(codigo=nuevo_codigo, nombre=nombre_periodo)
        nuevo_periodo.save()

    periodos = Periodo.objects.all()
    periodo_seleccionado = None

    if periodo_id:
        periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

    if not periodo_seleccionado:
        periodo_seleccionado = None

    transacciones = Transaccion.objects.filter(periodo=periodo_seleccionado).order_by('codigo')
    cuentas = Cuenta.objects.all().order_by('codigo')
    suma_debe = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
    
    return render(request, 'transacciones/transacciones.html', {
        'transacciones': transacciones,
        'cuentas': cuentas,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
    })



def filtrar_transacciones(request, periodo_id=None):
    periodos = Periodo.objects.all()
    cuentas = Cuenta.objects.all().order_by('codigo')
    if request.method == 'POST':
        periodo_id = request.POST.get('periodo-select')  # Obtén el ID del período desde el formulario
        suma_debe = Transaccion.objects.filter(periodo=periodo_id).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
        suma_haber = Transaccion.objects.filter(periodo=periodo_id).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
        if periodo_id == 'Ninguno':
            # Si se selecciona "Todos los períodos," muestra todas las transacciones
            return render(request, 'transacciones/transacciones.html', {'periodos'})
        else:
            # De lo contrario, filtra las transacciones por el período seleccionado
            transacciones = Transaccion.objects.filter(periodo_id=periodo_id)

        # Aquí puedes realizar cualquier otro procesamiento necesario antes de mostrar las transacciones

        # A continuación, debes pasar las transacciones filtradas a la plantilla
        return render(request, 'transacciones/transacciones.html', 
                      {'transacciones':transacciones, 
                       'suma_debe':suma_debe, 
                       'suma_haber': suma_haber,
                       'suma_haber': suma_haber,
                       'periodos': periodos,
                       'cuentas': cuentas,
                       })


from decimal import Decimal

@login_required
def actualizar_resumen_cuentas(request, periodo_id=None):
    # Lógica para manejar solicitudes POST
    if request.method == 'POST':
        periodo_id = request.POST.get('periodo')
        periodo_seleccionado = None
        if periodo_id:
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

        # Obtén todas las cuentas, incluso las que no tienen transacciones
        cuentas = Cuenta.objects.all()

        # Si hay un periodo seleccionado, realiza los cálculos
        if periodo_seleccionado:
            cuentas = cuentas.annotate(
                suma_debe=Sum(
                    Case(
                        When(transaccion__periodo=periodo_seleccionado, then=F('transaccion__movimiento_debe')),
                        default=Value(0, output_field=DecimalField()),  # Establece output_field como DecimalField
                    )
                ),
                suma_haber=Sum(
                    Case(
                        When(transaccion__periodo=periodo_seleccionado, then=F('transaccion__movimiento_haber')),
                        default=Value(0, output_field=DecimalField()),  # Establece output_field como DecimalField
                    )
                )
            )

            ResumenCuentas.objects.filter(periodo=periodo_seleccionado).delete()

            for cuenta in cuentas:
                suma_debe = float(cuenta.suma_debe)
                suma_haber = float(cuenta.suma_haber)
                saldo = 0

                if '1000' <= cuenta.codigo <= '1203':
                    saldo = suma_debe - suma_haber
                elif '2101' <= cuenta.codigo <= '3102':
                    saldo = suma_haber - suma_debe
                elif '4101' <= cuenta.codigo <= '4112':
                    saldo = suma_debe - suma_haber
                elif '510101' <= cuenta.codigo <= '510202':
                    saldo = suma_haber - suma_debe

                ResumenCuentas.objects.update_or_create(
                    periodo=periodo_seleccionado,
                    cuenta=cuenta,
                    defaults={
                        'debe_total': suma_debe,
                        'haber_total': suma_haber,
                        'saldo': saldo,
                    }
                )
    else:
        # Si no hay periodo seleccionado, establece los valores por defecto
        cuentas = cuentas.annotate(
            suma_debe=Value(0, output_field=DecimalField()),  # Establece output_field como DecimalField
            suma_haber=Value(0, output_field=DecimalField())  # Establece output_field como DecimalField
        )
    # Lógica para manejar solicitudes GET
    periodos = Periodo.objects.all()
    periodo_seleccionado = None

    if periodo_id:
        periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

    consulta = Cuenta.objects.filter(
        resumen_cuentas__isnull=False,
        resumen_cuentas__periodo=periodo_seleccionado
    ).values(
        'codigo', 'nombre', 'resumen_cuentas__debe_total',
        'resumen_cuentas__haber_total', 'resumen_cuentas__saldo'
    )

    resultados = consulta.all()

    suma_debe_total = ResumenCuentas.objects.filter(
        periodo=periodo_seleccionado
    ).aggregate(Sum('debe_total'))['debe_total__sum'] or 0

    suma_haber_total = ResumenCuentas.objects.filter(
        periodo=periodo_seleccionado
    ).aggregate(Sum('haber_total'))['haber_total__sum'] or 0

    suma_debe = Transaccion.objects.filter(
        periodo=periodo_seleccionado
    ).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or 0

    suma_haber = Transaccion.objects.filter(
        periodo=periodo_seleccionado
    ).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or 0

    cuentas = cuentas.order_by('codigo')
    transacciones = Transaccion.objects.filter(
        periodo=periodo_seleccionado
    ).order_by('fecha')

    return render(request, 'transacciones/transacciones.html', {
        'resultados': resultados,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
        'transacciones': transacciones,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'cuentas': cuentas,
        'suma_debe_total': suma_debe_total,
        'suma_haber_total': suma_haber_total,
    })


def agregar_empleado(request):
    if request.method == "POST":
        nombre=request.POST.get('nombre')
        puesto=request.POST.get('puesto')
        salario=float(request.POST.get('salario'))
        
        pago_diario=salario
        septimo=salario*7
        vacaciones=((15*salario)+0.3*(15*salario))/52
        salario_cancelado=septimo + vacaciones
        aguinaldo=(15*salario)/52
        ISS=salario_cancelado*0.075
        AFP=salario_cancelado*0.0875
        INSAFORP=salario*0.01
        costo_real=septimo+vacaciones+aguinaldo+ISS+AFP+INSAFORP

        # Cálculos y creación del nuevo empleado
        nuevo_empleado = ManoDeObra(nombre_empleado=nombre, puesto_trabajo=puesto, pago_diario=pago_diario, septimo_dia=septimo,
                                    vacaciones=vacaciones, salario_cancelado=salario_cancelado, aguinaldo=aguinaldo,
                                    iss=ISS, afp=AFP, insaforp=INSAFORP, costo_real=costo_real)
        nuevo_empleado.save()

    # Recalcula las sumas totales después de agregar el empleado
    suma_pago_diario = ManoDeObra.objects.aggregate(Sum('pago_diario'))['pago_diario__sum']
    suma_septimo_dia = ManoDeObra.objects.aggregate(Sum('septimo_dia'))['septimo_dia__sum']
    suma_vacaciones = ManoDeObra.objects.aggregate(Sum('vacaciones'))['vacaciones__sum']
    suma_salario_cancelado = ManoDeObra.objects.aggregate(Sum('salario_cancelado'))['salario_cancelado__sum']
    suma_aguinaldo = ManoDeObra.objects.aggregate(Sum('aguinaldo'))['aguinaldo__sum']
    suma_iss = ManoDeObra.objects.aggregate(Sum('iss'))['iss__sum']
    suma_afp = ManoDeObra.objects.aggregate(Sum('afp'))['afp__sum']
    suma_insaforp = ManoDeObra.objects.aggregate(Sum('insaforp'))['insaforp__sum']
    suma_costo_real = ManoDeObra.objects.aggregate(Sum('costo_real'))['costo_real__sum']
    total = suma_costo_real

    registros = ManoDeObra.objects.all()
    periodos = Periodo.objects.all()


    return render(request, 'controlcostos/manoobra.html', {
        'registros': registros,
        'suma_pago_diario': suma_pago_diario,
        'suma_septimo_dia': suma_septimo_dia,
        'suma_vacaciones': suma_vacaciones,
        'suma_salario_cancelado': suma_salario_cancelado,
        'suma_aguinaldo': suma_aguinaldo,
        'suma_iss': suma_iss,
        'suma_afp': suma_afp,
        'suma_insaforp': suma_insaforp,
        'suma_costo_real': suma_costo_real,
        'periodos':periodos
    })

def modificar_empleado(request, empleado_id):
    empleado = get_object_or_404(ManoDeObra, pk=empleado_id)

    if request.method == "POST":
        # Obtén los datos actualizados de la solicitud POST
        nombre = request.POST.get('nombre')
        puesto = request.POST.get('puesto')
        salario = float(request.POST.get('salario'))
        # Realiza los cálculos necesarios
        pago_diario = salario
        septimo = salario * 7
        vacaciones = ((15 * salario) + 0.3 * (15 * salario)) / 52
        salario_cancelado = septimo + vacaciones
        aguinaldo = (15 * salario) / 52
        ISS = salario_cancelado * 0.075
        AFP = salario_cancelado * 0.0875
        INSAFORP = salario * 0.01
        costo_real = septimo + vacaciones + aguinaldo + ISS + AFP + INSAFORP

        # Actualiza los campos del empleado con los nuevos valores
        empleado.nombre_empleado = nombre
        empleado.puesto_trabajo = puesto
        empleado.pago_diario = pago_diario
        empleado.septimo_dia = septimo
        empleado.vacaciones = vacaciones
        empleado.salario_cancelado = salario_cancelado
        empleado.aguinaldo = aguinaldo
        empleado.iss = ISS
        empleado.afp = AFP
        empleado.insaforp = INSAFORP
        empleado.costo_real = costo_real

        # Recalcula las sumas totales después de modificar el empleado
        suma_pago_diario = ManoDeObra.objects.aggregate(Sum('pago_diario'))['pago_diario__sum']
        suma_septimo_dia = ManoDeObra.objects.aggregate(Sum('septimo_dia'))['septimo_dia__sum']
        suma_vacaciones = ManoDeObra.objects.aggregate(Sum('vacaciones'))['vacaciones__sum']
        suma_salario_cancelado = ManoDeObra.objects.aggregate(Sum('salario_cancelado'))['salario_cancelado__sum']
        suma_aguinaldo = ManoDeObra.objects.aggregate(Sum('aguinaldo'))['aguinaldo__sum']
        suma_iss = ManoDeObra.objects.aggregate(Sum('iss'))['iss__sum']
        suma_afp = ManoDeObra.objects.aggregate(Sum('afp'))['afp__sum']
        suma_insaforp = ManoDeObra.objects.aggregate(Sum('insaforp'))['insaforp__sum']
        suma_costo_real = ManoDeObra.objects.aggregate(Sum('costo_real'))['costo_real__sum']
        total = suma_costo_real

        empleado.save()

    registros = ManoDeObra.objects.all()
    periodos = Periodo.objects.all()

    return redirect('/mano_de_obra_directa', {
        'registros': registros,
        'suma_pago_diario': suma_pago_diario,
        'suma_septimo_dia': suma_septimo_dia,
        'suma_vacaciones': suma_vacaciones,
        'suma_salario_cancelado': suma_salario_cancelado,
        'suma_aguinaldo': suma_aguinaldo,
        'suma_iss': suma_iss,
        'suma_afp': suma_afp,
        'suma_insaforp': suma_insaforp,
        'suma_costo_real': suma_costo_real,
        'periodos':periodos
    })

def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(ManoDeObra, pk=empleado_id)
    empleado.delete()

    # Recalcula las sumas totales después de eliminar el empleado
    suma_pago_diario = ManoDeObra.objects.aggregate(Sum('pago_diario'))['pago_diario__sum']
    suma_septimo_dia = ManoDeObra.objects.aggregate(Sum('septimo_dia'))['septimo_dia__sum']
    suma_vacaciones = ManoDeObra.objects.aggregate(Sum('vacaciones'))['vacaciones__sum']
    suma_salario_cancelado = ManoDeObra.objects.aggregate(Sum('salario_cancelado'))['salario_cancelado__sum']
    suma_aguinaldo = ManoDeObra.objects.aggregate(Sum('aguinaldo'))['aguinaldo__sum']
    suma_iss = ManoDeObra.objects.aggregate(Sum('iss'))['iss__sum']
    suma_afp = ManoDeObra.objects.aggregate(Sum('afp'))['afp__sum']
    suma_insaforp = ManoDeObra.objects.aggregate(Sum('insaforp'))['insaforp__sum']
    suma_costo_real = ManoDeObra.objects.aggregate(Sum('costo_real'))['costo_real__sum']
    total = suma_costo_real

    registros = ManoDeObra.objects.all()
    periodos = Periodo.objects.all()

    return redirect('/mano_de_obra_directa', {
        'registros': registros,
        'suma_pago_diario': suma_pago_diario,
        'suma_septimo_dia': suma_septimo_dia,
        'suma_vacaciones': suma_vacaciones,
        'suma_salario_cancelado': suma_salario_cancelado,
        'suma_aguinaldo': suma_aguinaldo,
        'suma_iss': suma_iss,
        'suma_afp': suma_afp,
        'suma_insaforp': suma_insaforp,
        'suma_costo_real': suma_costo_real,
        'periodos':periodos
    })

def agregar_a_partida_doble(request):
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        periodo = request.POST.get('periodo')
    
        suma_pago_diario = ManoDeObra.objects.aggregate(Sum('pago_diario'))['pago_diario__sum']
        suma_septimo_dia = ManoDeObra.objects.aggregate(Sum('septimo_dia'))['septimo_dia__sum']
        cuenta = Cuenta.objects.get(codigo='4103')
        descripcion = 'Mano de obra directa'
        movimiento_debe = suma_septimo_dia
        movimiento_haber = 0
        periodo_id = periodo
        nueva_transaccion = Transaccion(
            codigo=cuenta,
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            periodo_id = periodo_id
        )
        nueva_transaccion.save()

        suma_vacaciones = ManoDeObra.objects.aggregate(Sum('vacaciones'))['vacaciones__sum']
        cuenta = Cuenta.objects.get(codigo='4104')
        descripcion = 'Mano de obra directa'
        movimiento_debe = suma_vacaciones
        movimiento_haber = 0
        periodo_id = periodo
        nueva_transaccion = Transaccion(
            codigo=cuenta,
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            periodo_id = periodo_id
        )
        nueva_transaccion.save()

        suma_salario_cancelado = ManoDeObra.objects.aggregate(Sum('salario_cancelado'))['salario_cancelado__sum']

        suma_aguinaldo = ManoDeObra.objects.aggregate(Sum('aguinaldo'))['aguinaldo__sum']
        cuenta = Cuenta.objects.get(codigo='4105')
        descripcion = 'Mano de obra directa'
        movimiento_debe = suma_aguinaldo
        movimiento_haber = 0
        periodo_id = periodo
        nueva_transaccion = Transaccion(
            codigo=cuenta,
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            periodo_id = periodo_id
        )
        nueva_transaccion.save()

        suma_iss = ManoDeObra.objects.aggregate(Sum('iss'))['iss__sum']
        cuenta = Cuenta.objects.get(codigo='4106')
        descripcion = 'Mano de obra directa'
        movimiento_debe = suma_iss
        movimiento_haber = 0
        periodo_id = periodo
        nueva_transaccion = Transaccion(
            codigo=cuenta,
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            periodo_id = periodo_id
        )
        nueva_transaccion.save()

        suma_afp = ManoDeObra.objects.aggregate(Sum('afp'))['afp__sum']
        cuenta = Cuenta.objects.get(codigo='4107')
        descripcion = 'Mano de obra directa'
        movimiento_debe = suma_afp
        movimiento_haber = 0
        periodo_id = periodo
        nueva_transaccion = Transaccion(
            codigo=cuenta,
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            periodo_id = periodo_id
        )
        nueva_transaccion.save()

        suma_insaforp = ManoDeObra.objects.aggregate(Sum('insaforp'))['insaforp__sum']
        cuenta = Cuenta.objects.get(codigo='4108')
        descripcion = 'Mano de obra directa'
        movimiento_debe = suma_insaforp
        movimiento_haber = 0
        periodo_id = periodo
        nueva_transaccion = Transaccion(
            codigo=cuenta,
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            periodo_id = periodo_id
        )
        nueva_transaccion.save()

        suma_costo_real = ManoDeObra.objects.aggregate(Sum('costo_real'))['costo_real__sum']
        cuenta = Cuenta.objects.get(codigo='110101')
        descripcion = 'Mano de obra directa'
        movimiento_debe = 0
        movimiento_haber = suma_costo_real
        periodo_id = periodo
        nueva_transaccion = Transaccion(
            codigo=cuenta,
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            periodo_id = periodo_id
        )
        nueva_transaccion.save()

        total = suma_costo_real
    return redirect('/mano_de_obra_directa')


def ver_balance_general_de_periodo(request):
    codigo_periodo = 1
    if request.method == "POST":
        codigo_periodo = request.POST.get("periodo")
    # obtiene todas las cuentas de activo
    cuentas_activo = Cuenta.objects.filter(codigo__startswith="1")
    # obtiene todas las cuentas de pasivo
    cuentas_pasivo = Cuenta.objects.filter(codigo__startswith="2")
    # obtiene todas las cuentas de capital
    cuentas_capital = Cuenta.objects.filter(codigo__startswith="3")

    array_cuentas_activo = []
    array_cuentas_pasivo = []
    array_cuentas_capital = []
    # obtiene el periodo seleccionado
    periodo = Periodo.objects.get(codigo=codigo_periodo)

    # por cada cuenta de activo, obtiene el saldo de la cuenta en el periodo seleccionado
    for cuenta in cuentas_activo:
            transacciones = Transaccion.objects.filter(codigo=cuenta, periodo=periodo)
            if(transacciones):
                suma_debe = transacciones.aggregate(Sum("movimiento_debe"))["movimiento_debe__sum"] or Decimal(0)
                suma_haberes = transacciones.aggregate(Sum("movimiento_haber"))["movimiento_haber__sum"] or Decimal(0)
                saldo = suma_debe - suma_haberes
                nueva_cuenta = {
                    "codigo": cuenta.codigo,
                    "nombre": cuenta.nombre,
                    "saldo": saldo,
                    "debe_total": suma_debe,
                    "haber_total": suma_haberes,
                }

                array_cuentas_activo.append(nueva_cuenta)

    # por cada cuenta de pasivo, obtiene el saldo de la cuenta en el periodo seleccionado
    for cuenta in cuentas_pasivo:
        transacciones = Transaccion.objects.filter(codigo=cuenta, periodo=periodo)
        if(transacciones):
            suma_debe = transacciones.aggregate(Sum("movimiento_debe"))["movimiento_debe__sum"] or Decimal(0)
            suma_haberes = transacciones.aggregate(Sum("movimiento_haber"))["movimiento_haber__sum"] or Decimal(0)
            saldo = suma_haberes - suma_debe
            nueva_cuenta = {
                "codigo": cuenta.codigo,
                "nombre": cuenta.nombre,
                "saldo": saldo,
                "debe_total": suma_debe,
                "haber_total": suma_haberes,
            }
            array_cuentas_pasivo.append(nueva_cuenta)

    # por cada cuenta de capital, obtiene el saldo de la cuenta en el periodo seleccionado
    for cuenta in cuentas_capital:
        transacciones = Transaccion.objects.filter(codigo=cuenta, periodo=periodo)
        if(transacciones):
            suma_debe = transacciones.aggregate(Sum("movimiento_debe"))["movimiento_debe__sum"] or Decimal(0)
            suma_haberes = transacciones.aggregate(Sum("movimiento_haber"))["movimiento_haber__sum"] or Decimal(0)
            saldo = suma_haberes - suma_debe
            nueva_cuenta = {
                "codigo": cuenta.codigo,
                "nombre": cuenta.nombre,
                "saldo": saldo,
                "debe_total": suma_debe,
                "haber_total": suma_haberes,
            }
            array_cuentas_capital.append(nueva_cuenta)

    # obtiene el saldo total de activo
    totales_saldos_activos = {
        "total_haberes": 0,
        "total_debe": 0,
        "total_saldo": 0,
    }
    for cuenta in array_cuentas_activo:
        # total haberes 
        totales_saldos_activos['total_haberes'] += cuenta['haber_total']
        # total debe
        totales_saldos_activos['total_debe'] += cuenta['debe_total']
        # total saldo
        totales_saldos_activos['total_saldo'] += cuenta['saldo']
        

    # obtiene el saldo total de pasivo
    totales_saldos_pasivos = {
        "total_haberes": 0,
        "total_debe": 0,
        "total_saldo": 0,
    }


    for cuenta in array_cuentas_pasivo:
        totales_saldos_pasivos['total_haberes'] += cuenta['haber_total']
        totales_saldos_pasivos['total_debe'] += cuenta['debe_total']
        totales_saldos_pasivos['total_saldo'] += cuenta['saldo']

    # obtiene el saldo total de capital
    totales_saldos_capital = {
        "total_haberes": 0,
        "total_debe": 0,
        "total_saldo": 0,
    }

    for cuenta in array_cuentas_capital:
        totales_saldos_capital['total_haberes'] += cuenta['haber_total']
        totales_saldos_capital['total_debe'] += cuenta['debe_total']
        totales_saldos_capital['total_saldo'] += cuenta['saldo']

    total_saldo_pasivo = totales_saldos_pasivos['total_debe'] - totales_saldos_pasivos['total_haberes']
    total_saldo_capital = totales_saldos_capital['total_debe'] - totales_saldos_capital['total_haberes']
    total_saldo_pasivo_capital = total_saldo_pasivo + total_saldo_capital

    # Retorna la vista con los datos
    return render(
        request,
        "estadosfinancieros/general.html",
        {
            "cuentas_activo": array_cuentas_activo,
            "cuentas_pasivo": array_cuentas_pasivo,
            "cuentas_capital": array_cuentas_capital,
            "total_saldo_pasivo_capital": total_saldo_pasivo_capital,
            "periodos": Periodo.objects.all(),
            "totales_saldos_activos": totales_saldos_activos,
            "totales_saldos_pasivos": totales_saldos_pasivos,
            "totales_saldos_capital": totales_saldos_capital,
        },
    )

def ver_estado_de_capital_de_periodo(request):

    # periodo seleccionado
    codigo_periodo = 1
    if request.method == "POST":
        codigo_periodo = request.POST.get("periodo")
    
    # capital inicial
    capital_inicial = 0
    cuenta_caja = Cuenta.objects.get(codigo="110101")
    cuenta_bancos = Cuenta.objects.get(codigo="110102")

    capital_inicial += Transaccion.objects.filter(codigo=cuenta_caja, periodo=codigo_periodo).aggregate(Sum("movimiento_debe"))["movimiento_debe__sum"] or Decimal(0)
    capital_inicial += Transaccion.objects.filter(codigo=cuenta_bancos, periodo=codigo_periodo).aggregate(Sum("movimiento_debe"))["movimiento_debe__sum"] or Decimal(0)

    # utilidad del ejercicio
    utilidad_ejercicio = 0
    ingresos = 0
    gastos = 0
    otros_ingresos = 0
    otros_gastos = 0
    # ingresos
    cuenta_ingresos = Cuenta.objects.filter(codigo__startswith="1")
    for cuenta in cuenta_ingresos:
        ingresos += Transaccion.objects.filter(codigo=cuenta, periodo=codigo_periodo).aggregate(Sum("movimiento_debe"))["movimiento_debe__sum"] or Decimal(0)

    ingresos -= capital_inicial
    # gastos
    cuenta_gastos = Cuenta.objects.filter(codigo__startswith="4")
    for cuenta in cuenta_gastos:
        gastos += Transaccion.objects.filter(codigo=cuenta, periodo=codigo_periodo).aggregate(Sum("movimiento_debe"))["movimiento_debe__sum"] or Decimal(0)
    # otros ingresos
    cuenta_otros_ingresos = Cuenta.objects.filter(codigo__startswith="2")
    for cuenta in cuenta_otros_ingresos:
        otros_ingresos += Transaccion.objects.filter(codigo=cuenta, periodo=codigo_periodo).aggregate(Sum("movimiento_debe"))["movimiento_debe__sum"] or Decimal(0)
    # otros gastos
    cuenta_otros_gastos = Cuenta.objects.filter(codigo__startswith="5")
    for cuenta in cuenta_otros_gastos:
        otros_gastos += Transaccion.objects.filter(codigo=cuenta, periodo=codigo_periodo).aggregate(Sum("movimiento_debe"))["movimiento_debe__sum"] or Decimal(0)

    print(ingresos)
    print(gastos)
    print(otros_ingresos)
    # capital final
    utilidad_ejercicio = ingresos - gastos + otros_ingresos - otros_gastos
    capital_final = capital_inicial + utilidad_ejercicio

    

    return render(
        request,
        "estadosfinancieros/capital.html",
        {
            "capital_inicial": capital_inicial,
            "utilidad_ejercicio": utilidad_ejercicio,
            "capital_final": capital_final,
            "periodos": Periodo.objects.all(),
            "ingresos": ingresos,
            "gastos": gastos,
            "otros_ingresos": otros_ingresos,
            "otros_gastos": otros_gastos,
        },
    )