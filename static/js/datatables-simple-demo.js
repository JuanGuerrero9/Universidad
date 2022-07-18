
$(document).ready(function() {
    $('#datatablesSimple').DataTable( {
        "paging":   true,
        "ordering": true,
        "info":     true,
        "pagingType": "full_numbers",
        "language": {
            "emptyTable":     "No hay datos para mostrar",
            "info":           "Mostrar _START_ a _END_ de _TOTAL_ datos",
            "infoEmpty":      "Mostrar 0 to 0 of 0 entries",
            "infoFiltered":   "(Filtarado desde _MAX_ total filas)",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Mostrar _MENU_  filas",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros",
            "paginate": {
                "first":      "Primero",
                "last":       "Ultimo",
                "next":       "Siguiente",
                "previous":   "Anterior"
            },
        }
    });
});
$(document).ready(function() {
    $('#datatablesSimple2').DataTable( {
        "paging":   true,
        "ordering": true,
        "info":     true,
        "pagingType": "full_numbers",
        "language": {
            "emptyTable":     "No hay datos para mostrar",
            "info":           "Mostrar _START_ a _END_ de _TOTAL_ datos",
            "infoEmpty":      "Mostrar 0 to 0 of 0 entries",
            "infoFiltered":   "(Filtarado desde _MAX_ total filas)",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Mostrar _MENU_  filas",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros",
            "paginate": {
                "first":      "Primero",
                "last":       "Ultimo",
                "next":       "Siguiente",
                "previous":   "Anterior"
            },
        }
    });
});

$('.mask').number( true, 0 );