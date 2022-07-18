
var $ = jQuery.noConflict();

$(document).ready(function(){
    var URLactual = jQuery(location).attr("href");
    if (URLactual.indexOf("/institucional/recibo/") != -1) {
        recibo_pago();
    }
    else if (URLactual.indexOf("/institucional/usuario_creado/") != -1) {
        usuario_creado();
    }
    else if (URLactual.indexOf("/institucional/matricular_asignaturas/") != -1) {
        matricular_asignatura();
        
    }
    else if(URLactual.indexOf("/institucional/editar_notas/") != -1) {
        edicion_notas();
    }
    else if(URLactual.indexOf("/institucional/recibo_pagado/")) {
        cancelacion_recibo_semestre();
    }

    }
)




// Funcion que funciona desde la vista de matricular asignatura

function agregar_horarios(pk) {
    let access_token = localStorage.getItem('Token'); 
    localStorage.setItem("id_asignatura", pk);
    $.ajax({
        url: `/rest/institucional/tramites_funcionario/${pk}/obtener_horarios_asignatura/`,
        method: 'GET', 
        headers: { "Authorization": 'Bearer ' + access_token},
        success: function(data) {  
            
            let horarios = data.horarios
            console.log(horarios)
            var select_horarios = document.getElementById('select_horario');
            for (var i = 0; i <= horarios.length; i++){
                let id_horario = horarios[i]['id_horario'];
                let opt = document.createElement('option');
                if (typeof(id_horario) !== 'undefined') {
                    opt.value = id_horario;
                }
                opt.text = `${horarios[i]['docente']} ${horarios[i]['hora_inicio']} ${horarios[i]['hora_final'] }`
                select_horarios.appendChild(opt);
            }

        },
    });
}

function agregar_notas(pk) {
    let access_token = localStorage.getItem('Token'); 
    $.ajax({
        url: `/rest/institucional/tramites_funcionario/${pk}/agregar_nota_corte/`,
        method: 'GET', 
        headers: { "Authorization": 'Bearer ' + access_token},
        success: function(data) {  
            $('#div_notas').html("");
            for (let i = 1;i <= 3; i++) {
                if (data[`nota${i}_agregada`] == false) {
                    fila = '<label>' + `Nota de corte ${i}` + '</label>';
                    fila += `<input name="nota_corte_${i}" class="form-control" type="number" placeholder="Nota del corte ${i}">`;
                    fila += `</input>`
                    $('#div_notas').append(fila);
                }
            }
        },
    });
}

function abrir_modal_con_parametros(url, pk) {
    localStorage.setItem("id", pk);
	$('#edicion').load(url, function () {
        $(this).modal('show');
	});
    setTimeout(() => {
        agregar_horarios(pk);
    }, 1000)
}

function abrir_modal_agregar_notas(url, pk) {
	$('#edicion').load(url, function () {
        $(this).modal('show');
	});
    setTimeout(() => {
        agregar_notas(pk);
    }, 1000)
}