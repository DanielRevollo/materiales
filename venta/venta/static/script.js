$(document).ready(inicio)
$(document).ready(carrito)
function carrito(){
    $(".enlace" ).click(function( event ) {
        event.preventDefault();
        var direccion=$(this).attr("href");
        $.ajax({
            type:'GET',
            url:direccion,
            data: {},
            success: crearFormulario,
            error:errores
        });
    });
    //FUNCIONES PARA NUESTRO CARRITO
    //AQUI USAMOS AJAX  que tiene una funcion llamada load, LOAD ES UNA FUNCION DE TIPO AJAX PERO MAS SIMPLE
    //LO QUE HACE ES CARGAR UNA URL QUE LE ENVIAMOS COMO PARAMENTRO, HACEMOS ESTO EN CASO DE QUE SI EL USUARIO VA A OTRA PAGINA
    //SE CARGE AUTOMATICAMENTE NUESTRO CARRITO
    $('#carrito').load("/productos/mostrar/carrito/");
}
function crearFormulario(data){
    $("#formulario").html(data);
}
function inicio()
{
    //Lo que acemos aqui es seleccionar el select del dia en el formulario registro  en la opcion o indice 0
    //y cambiar el texto que era -- por Dia, es el mismo procedimiento para el mes y año
    //Hacemos esto porq django omite esto y hace que nuestro formulario no sea completo
    var dia=$("#id_fecha_nacimiento_day option:[value=0]").val('0');
    dia.text("Dia");
    var mes=$("#id_fecha_nacimiento_month option:[value=0]").val('0');
    mes.text("Mes");
    var anio=$("#id_fecha_nacimiento_year option:[value=0]").val('0');
    anio.text("Año");
    //Aqui seleccionamos el campo de texto del buscador y removemos el atributo autocompletar para que no complete el campo
    //ya que nosotros crearemos nuestro propio buscador
    var tbuscar=$("#id_texto").attr('autocomplete','off');
    //Luego usamos la funcion keypress que nos indicara si el usuario esta presionando alguna tecla
    //Si es asi se llamara a una funcion buscar
    tbuscar.keypress(buscar);
}
function buscar(){
    //es una simple funcion ajax que es de tipo GET y apunta a una url buscar, le enviamos como datos
    //el formulario con el id fbuscar
    //y cuando se complete la funcion ajax llamara a una funcion resultado
    $.ajax({
        type:'GET',
        url:'/buscar/',
        data:$("#fbuscar").serialize(),
        success:resultado,
        error:errores
    })
}
function resultado(data){
    //Seleccionamos el div con la clase resultado y aplicamos un efecto llamso fadeIn, este efecto lo que hace
    //es deslizar el div hacia avajo y le enviamos un parametro slow para que la transiccion no sea rapida
    $(".resultados").fadeIn("slow");
    // finalmente recibimos el dato que nos evia la url buscar y la añadimos al div resultado
    $(".resultados").html(data);
}
function errores(){
    alert ("Error");
}
