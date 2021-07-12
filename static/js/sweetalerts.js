var $ = jQuery.noConflict();

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


function crearUsuario(){
    activarBoton();
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: 'institucional:elegir_horario',
        type: $('#form_creacion').attr('method'),
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
                redirigirCrearUsuario(response, response.context);
            }, 2000)
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion2(error);
            activarBoton();
        }
    })
}



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
	error += '<div class = "alert alert-danger" <strong>' + errores.responseJSON.error + '</strong></div>';
	$('#errores').append(error);
}

function activarBoton(){
	if($('#boton_creacion').prop('disabled')){
		$('#boton_creacion').prop('disabled',true);
	}else{
		$('#boton_creacion').prop('disabled', false);
	}
}


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
