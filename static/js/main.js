var $ = jQuery.noConflict();

// funciones para activar modales

function registrar() {
    activarBoton();
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje)
            setTimeout(() => {
                generarRecibo(response.context.recibo, response);
            }, 2000)
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion(error);
            activarBoton();
        }
    });
}

function pagarRecibo(){
    activarBoton();
    $.ajax({
        data: $('#form_pagar').serialize(),
        url: $('#form_pagar').attr('action'),
        type: $('#form_pagar').attr('method'),
        success: function (response) {
            confirmacionPagoTarjeta(response.mensaje);
            setTimeout(() => {
                reciboPagadoTarjeta(response);
            }, 2000)
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion2(error);
            activarBoton();
        }
    });
}



function crearUsuario(){
    activarBoton();
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            setTimeout(() => {
                redirigirCrearUsuario(response, response.context);
            }, 2000)
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion2(error);
            activarBoton();
        }
    });
}

function matricularMateria() {
    activarBoton();
    $.ajax({
        data: $('#form_agregar').serialize(),
        url: $('#form_agregar').attr('action'),
        type: $('#form_agregar').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            setTimeout(() => {
                horarioAgregado(response);
            }, 2000)
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion2(error);
            activarBoton();
        }
    })
}

// Funciones para generar errores 


function mostrarErroresCreacion(errores){
	$('#errores').html("");
	let error = "";
	for(let item in errores.responseJSON.error){
		error += '<div class = "alert alert-danger" <strong>' + errores.responseJSON.error[item] + '</strong></div>';
	}
	$('#errores').append(error);
}

function mostrarErroresCreacion2(errores){
	$('#errores').html("");
	let error = "";
	error += '<div class = "alert alert-danger" <strong>' + errores.responseJSON.mensaje + '</strong></div>';
	$('#errores').append(error);
}

// SweetAlerts

function notificacionError(mensaje){
	Swal.fire({
		title: 'Error!',
		text: mensaje,
		icon: 'error'
	})
}

function notificacionSuccess(mensaje) {

	Swal.fire({
		title: 'Buen Trabajo!',
		text: mensaje,
		icon: 'success'
	})
}


function confirmacionPagoTarjeta(mensaje){
    Swal.fire({
        title: 'Esta seguro?',
        text: mensaje,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si deseo pagarlo'
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire(
            'Pagado!',
            'El recibo ha sido pagado satisfactoriamente.',
            'success'
          )
        }
      })
}



// Funciones de redireccion

function reciboPagadoTarjeta(response) {
    if (response.status == 201) {
        window.location.href = `/`;
    }
}


function horarioAgregado(response) {
    if (response.context.status == 201) {
        window.location.href = `/institucional/matricular_asignaturas/`;
    }
}

function generarRecibo(recibo, response) {
    if (response.context.status == 201) {
        window.location.href = `/institucional/recibo/${recibo}/`;
    }
}

function redirigirCrearUsuario(response, context) {
    if (response.context.status == 201) {
        window.location.href = `/institucional/usuario_creado/${context.usuario}/${context.passusuario}`;
    }
}



// Funciones con botones


function activarBoton(){
	if($('#boton_creacion').prop('disabled')){
		$('#boton_creacion').prop('disabled',true);
	}else{
		$('#boton_creacion').prop('disabled', false);
	}
}

function cerrar_modal_edicion() {
	$('#edicion').modal('hide');
}

function abrir_modal_edicion(url) {
	$('#edicion').load(url, function () {
        $(this).modal('show');
	});
}