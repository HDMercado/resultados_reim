Antes de la modificación al código de la plataforma, se recomienda tener las querys de SQL listas para implementarlas. Luego de que estén
entregando los datos correctos, se procede a modificar el archivo "users/utils.py" agregando una nueva función por cada query a 
implementar (siguiendo la estructura de las funciones de los otros REIM que ya poseen gráficos).

Posteriormente, se modifica el users/views.py en la función "welcome", se declaran los response que se retornarán y luego una condición
"if reim_num=="x": " para que no se ejecute en caso de tener seleccionado el REIM, las variables que retornarán valores se declaran antes del if
debido a que en caso de que otro REIM esté seleccionado arrojará un error de variable indefinida. (Se muestra un ejemplo más adelante)

Para temas de optimización pueden realizar un if para cada actividad de sus REIM.

Se utilizaron diccionarios para el almacenamiento de los datos rescatados en las querys utilizando la siguente estructura:


variable_query_quantity_response = []

if reim_num="223": #filtro por REIM
    if activity_num=="10001" or activity_num=="10002": #filtro por actividad mencionado anteriorente
        variable_query = function_from_utils(request) #instanciamos la funcion de utils y la almacenamos en una variable
        queries.append({"name": 'Query prueba', "query": variable_query}) #lista queries almacena todas las querys utilizadas para imprimirlas (con la sintaxis de SQL, es netamente para ver error de comillas que es lo más común) en pantalla (el botón para verlas se ocultó debido a que la página pasó a producción)
        cursor.execute(variable_query) #Se ejecuta la query
        variable_query_quantity = cursor.fetchall() #Se obtiene la respuesta de la query en una lista de tublas
        for row in variable_query_quantity:
            variable_query_quantity_response.append({ 'id': row[0], 'dato1': row[1], 'dato2': row[2], 'dato3': row[3] }) #Se agregan al response los datos obtenidos, el número de datos varía dependiendo de la cantidad de columnas de la respuesta de cada query, debido a que el for recorre las filas y las variables cada col, asignarle un nombre correspondiente a cada "dato" para una mayor facilidad de uso en los pasos posteriores


Finalizando en el archivo views.py, se agregan los response al return de la función. Un ejemplo de esto es:

    'variable_query_quantity':variable_query_quantity_response,

Lista la obtención de los datos, queda graficarlos y mostrarlos. Para esto nos dirigimos al users/templates/users/welcome.html, agregar
los filtros correspondientes a numero de reim, numero de actividad (entre otros que se estimen convenientes) y agregar la estructura a utilizar.

Ejemplo de la estructura utilizada:

    {% if reim_num == '223' %}
        <div class="wrapper wrapper-content">
                {% if activity_num == '10001' and student_num == '0' %}  <!-- El otro filtro existente que se aplica para todos los reim es el de student_num, en este caso es un gráfico para todo el curso, por ende student_num=='0', en caso de hacer por alumno student_num!='0' -->
                    <div class="row">
                        <div class="col-lg-12">
                            <div class="row" {% if not activate_graphics %}style="display: none;"{% endif %}>
                                <div class="col-lg-6">
                                    <div class="ibox">
                                        <div class="ibox-title">
                                            <h5>Query de actividad prueba</h5><span class="glyphicon glyphicon-info-sign" title="Información textual a mostrar del gráfico, se mmuestra solo en caso de mover el curso encima del ícono"></span>
                                        </div>
                                        <div class="ibox-content">
                                            <div class="scroll_content">
                                                <canvas id="query_REIM223" height={{cant_usuarios}}>{% load staticfiles %}</canvas> <!-- Alto del gráfico por defecto es cant_usuarios, en caso querer implementar un alto personalizado se recomienda calcularlo en el views en base a la cantidad de filas de la respuesta de la query y retornarlo en el return render -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <!-- Gráfico 2--> 
                                <div class="col-lg-6">
                                    <div class="ibox ">
                                        <div class="ibox-title">
                                            <h5></h5><span class="glyphicon glyphicon-info-sign" title=""></span>
                                            <div class="ibox-tools"></div>
                                        </div>
                                        <div class="ibox-content">
                                            <div class="scroll_content">
                                                <canvas id="" height={{}>{% load staticfiles %}</canvas>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                {% endif %}
        </div>
    {% endif %}

Como paso final solo basta realizar los gráficos con los datos obtenidos del views. Antes del script del selector de filtros 
de la linea 4225, se encuentran los scripts para graficar los datos, utilizando la siguiente estructura:

    // Data del gráfico
    var ctx80data = {
        labels:
        [
            {% if variable_query_quantity %} 
                {% for variable_query in variable_query_quantity %}
                    '{{variable_query.data1}}', //Aquí se ve reflejado el diccionario creado, en este caso se utiliza data1 que vendría siendo el nombre del alumno
                {% endfor%}
            {% endif%}
        ],
        datasets:
        [
            {
            label: "Cantidad de x", //nombre de la etiqueta del gráfico
            backgroundColor: '#00b5eb',
            borderColor: "#00b5eb",
            pointBorderColor: "#fff",
            data:
            [
                {% if variable_query_quantity %}
                    {% for variable_query in variable_query_quantity %}
                        '{{variable_query.dato2}}',
                    {% endfor%}
                {% endif%}
            ]
            },
            
            {
            label: "Cantidad de y", //nombre de la etiqueta del gráfico
            backgroundColor: '#00b5eb',
            borderColor: "#00b5eb",
            pointBorderColor: "#fff",
            data:
            [
                {% if variable_query_quantity %}
                    {% for variable_query in variable_query_quantity %}
                        '{{variable_query.dato3}}',
                    {% endfor%}
                {% endif%}
            ]
            },
            // n labels como datos a presentar

        ]
        };

    if ($('#query_REIM223').length){ //En caso de que exista el id query_REIM223 se instancia el gráfico, en caso de no hacer esto y que se acceda a otro REIM, el código JS no seguirá ejecutando hacia abajo debido a que no encuentra dicha id
        var ctx80 = document.getElementById("query_REIM223");
        new Chart(ctx80, {type: 'horizontalBar', data: ctx80data, options:barOptions}); //para realizar gráficos como los presentes en la plataforma, se utiliza barOptions, para otros estilos de gráficos se debe crear dichos ajustes
    }

Con dichos pasos realizados ya se verán reflejados los gráficos con datos, en caso de que no sea así, primero revisar 
la consola donde se ejecuta el servidor para ver si presenta algún error, segundo revusar la query (debugeando en el views.py), 
luego revisar que coincidan los id del html con los del JS,  y finalmente revisar la consola del navegador para corroborar si es 
que existen errores en el JS.
