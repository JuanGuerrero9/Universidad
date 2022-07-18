var $ = jQuery.noConflict();


$(document).ready(function(){    
    $('#boton_creacion2').click(function(){                       
        /*Obtener datos almacenados*/
        
    });   
});



$(function(){
    $('#edicion').on('shown.bs.modal', function () {
        $(document).ready(function() {
            $('.selectpicker').select2();
        });
    });
});


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



function editar(){
    activarBoton();
    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            setTimeout(() => {
                cerrar_modal_edicion();
            }, 2000)
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBoton();
        }
    });
}

function editar3(){
    activarBoton();
    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            setTimeout(() => {
                redirigirCrear(response.url);
                cerrar_modal_edicion();
            }, 2000)
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBoton();
        }
    });
}

function editarUsuario(){
    activarBoton();
    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            setTimeout(() => {
                reciboPagadoTarjeta();
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

function mostrarErroresEdicion(errores) {
	$('#erroresEdicion').html("");
	let error = "";
	for (let item in errores.responseJSON.error) {
		error += '<div class = "alert alert-danger" <strong>' + errores.responseJSON.error[item] + '</strong></div>';
	}
	$('#erroresEdicion').append(error);
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
          ),
          setTimeout(() => {
            reciboPagadoTarjeta();
            }, 2000)
        }
      })
}

function eleccion_estudiante(pk) {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-success',
          cancelButton: 'btn btn-primary'
        },
        buttonsStyling: false
    })
      
    swalWithBootstrapButtons.fire({
        title: 'Que proceso deseas realizar?',
        text: "Aqui te damos las dos opciones para generacion de recibos de pago",
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Estudiante antiguo',
        cancelButtonText: 'Estudiante nuevo',
        reverseButtons: true
        }).then((result) => {
        if (result.isConfirmed) {
            abrir_modal_edicion(`/institucional/estudiante_antiguo/${pk}/`)
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            abrir_modal_edicion(`/institucional/estudiante_nuevo/${pk}/`)
        }
    })
}

function eleccion_tipo_usuario() {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-success',
          cancelButton: 'btn btn-primary'
        },
        buttonsStyling: false
    })
      
    swalWithBootstrapButtons.fire({
        title: 'Que proceso deseas realizar?',
        text: "Elige cual de los dos tipos de usuario deseas crear",
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Docente',
        cancelButtonText: 'Estudiante',
        reverseButtons: true
        }).then((result) => {
        if (result.isConfirmed) {
            abrir_modal_edicion('/institucional/crear_usuario_docente/')
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            abrir_modal_edicion('/institucional/crear_usuario_estudiante/')
        }
    })
}


function eliminar(url){
    activarBoton();
    $.ajax({
        headers: {
            'X-CSRFToken': csrfToken
          },
        url: url,
        type: "POST",
        success: function (response) {
            notificacionSuccess(response.mensaje);
            setTimeout(() => {
                cerrar_modal_edicion();
                redirigirEditar();
            }, 10)
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBoton();
        }
    });
}


function confirmacion(variable){
    Swal.fire({
        title: `Desea matricular la ${variable}?`,
        text: 'Se le matriculará el horario elegido para la asignatura',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si deseo validar'
      }).then((result) => {
        if (result.isConfirmed) {
            editar();
        }
      })
}


// Funciones de redireccion


function redireccion_url(url) {
    window.location.href = url;
}




























function reciboPagadoTarjeta() {
    window.location.href = `/`;
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

function redirigirCrear(url) {
    window.location.href = url;
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