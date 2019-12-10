from .utils import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import User


def welcome(request):

    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        
        cursor = get_from_db()
        queries = []

        #School selector
        course_filter = ''
        activate_course_filter = False
        if request.GET.get('course') and request.GET.get('course') != "0":
            activate_course_filter = True
            course_filter = ' AND pertenece.curso_id='+ request.GET.get('course')
  
        cursor.execute('SELECT colegio.id, colegio.nombre FROM pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id INNER JOIN colegio ON pertenece.colegio_id = colegio.id WHERE usuario.username="' + request.user.username + '" GROUP BY colegio.id')
        schools = cursor.fetchall()
        schools_response = []
        for row in schools:
            schools_response.append({ 'id': row[0], 'name': row[1] })

        #Reim selector
        course_filter = ''
        #if request.GET.get('course') and request.GET.get('activity') != "0":
        #    course_filter = request.GET.get('course')
        activate_course_filter = False
        if request.GET.get('course') and request.GET.get('course') != "0":
            activate_course_filter = True
            course_filter = 'where curso_id ='+ request.GET.get('course')
         
        #cursor.execute('SELECT DISTINCT reim.id, reim.nombre from actividad inner join reim on id_reim = reim.id inner join asigna_reim on reim_id = reim_id inner join pertenece on asigna_reim.colegio_id = pertenece.colegio_id  inner join colegio on asigna_reim.colegio_id = colegio.id inner join curso on asigna_reim.curso_id = curso.id  inner join usuario on pertenece.usuario_id = usuario.id where usuario.username ="' + request.user.username + '"' + course_filter +' GROUP BY reim.id')
        cursor.execute('SELECT DISTINCT reim.id, reim.nombre from asigna_reim inner join reim on reim_id = reim.id '+ course_filter +' GROUP BY reim.id')
        reims = cursor.fetchall()
        reims_response = []
        for row in reims:
            reims_response.append({ 'id': row[0], 'name': row[1] })

        #Course selector
        school_filter = ''
        activate_school_filter = False
        if request.GET.get('school') and request.GET.get('school') != "0":
            activate_school_filter = True
            school_filter = ' AND pertenece.colegio_id='+ request.GET.get('school')
            
        cursor.execute('SELECT curso.id, concat(nivel.nombre, " ",curso.nombre) as Nivelcurso FROM pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id INNER JOIN curso ON pertenece.curso_id = curso.id INNER JOIN nivel ON pertenece.nivel_id = nivel.id WHERE usuario.username ="' + request.user.username + '"' + school_filter +' GROUP BY curso.id')
        courses = cursor.fetchall()
        courses_response = []
        for row in courses:
            courses_response.append({ 'id': row[0], 'name': row[1] })

        #Activity selector
        reim_filter = ''
        activate_reim_filter = False
        if request.GET.get('reim') and request.GET.get('reim') != "0":
            activate_reim_filter = True
            reim_filter = ' AND actividad.id_reim='+ request.GET.get('reim')
         
        cursor.execute('SELECT DISTINCT actividad.id, actividad.nombre from asigna_reim inner join actividad on reim_id = reim_id inner join pertenece on asigna_reim.colegio_id = pertenece.colegio_id  inner join colegio on asigna_reim.colegio_id = colegio.id inner join curso on asigna_reim.curso_id = curso.id  inner join usuario on pertenece.usuario_id = usuario.id where usuario.username ="' + request.user.username + '"' + reim_filter +' GROUP BY actividad.id')
        activities = cursor.fetchall()
        activities_response = []
        for row in activities:
            activities_response.append({ 'id': row[0], 'name': row[1] })

        #Game time
        time_query = get_time_query(request)
        print(time_query)
        queries.append({"name": 'Time query', "query": time_query })
        cursor.execute(time_query)
        game_time = cursor.fetchall()
        game_time_response = []
        for row in game_time:
            game_time_response.append({ 'id': row[0], 'name': row[1], 'time': row[2] })

        #Touch
        touch_query = get_touch_query(request)
        queries.append({"name": 'Touch query', "query": touch_query})
        cursor.execute(touch_query)
        touch_quantity = cursor.fetchall()
        touch_quantity_response = []
        for row in touch_quantity:
            touch_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        
        #Cantidad de Usuarios
        cant_usuarios = get_alumnos(request)
        print("largo de graficos")
        print(cant_usuarios)
        #actividad seleccionada
        activity_num = request.GET.get('activity')
        activate_activity_filter = True
        if request.GET.get('activity') and request.GET.get('activity') != "0":
            activate_activity_filter = False
        #REIM SELECCIONADO
        reim_num = request.GET.get('reim')
        
        student_num = request.GET.get('student')
        students_response = []
        if request.GET.get('school') and request.GET.get('school') != '0':
            if request.GET.get('course') and request.GET.get('course') != '0':
                cursor.execute('SELECT DISTINCT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '")' + 'AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username ="' + request.user.username + '"))' + 'AND a.id_reim="' + request.GET.get('reim') + '"' + 'AND b.curso_id ="' + request.GET.get('course') + '"' + 'AND b.colegio_id ="' + request.GET.get('school') + '";')
                students = cursor.fetchall()
                for row in students:
                    students_response.append({ 'id': row[0], 'name': row[1] })

        #INICIO MUNDO ANIMAL 
        piezas_quantity_response =[]
        malas_quantity_response = []
        animales_quantity_response = []
        actividades_quantity_response=[]
        interaccion_quantity_response=[]
        tiempoact_quantity_response=[]
        
        if reim_num=="1":
            piezas_query = get_piezas(request)
            cursor.execute(piezas_query)
            queries.append({"name": 'Piezas query', "query": piezas_query})
            piezas_quantity = cursor.fetchall()
            print ("piezas quantity", piezas_quantity)
            for row in piezas_quantity:
                piezas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            malas_query = get_malas(request)
            cursor.execute(malas_query)
            queries.append({"name": 'Malas query', "query": malas_query})
            malas_quantity = cursor.fetchall()
            print("malas quantity", malas_quantity)
            for row in malas_quantity:
                malas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            animales_query = get_animals(request)
            cursor.execute(animales_query)
            queries.append({"name": 'Animales query', "query": animales_query})
            animales_quantity = cursor.fetchall()
            print("animales quantity", animales_quantity)
            for row in animales_quantity:
                animales_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })


            interaccion_query = get_interaccion(request)
            cursor.execute(interaccion_query)
            queries.append({"name": 'Interaccion query', "query": interaccion_query})
            interaccion_quantity = cursor.fetchall()
            print("interacccion quantity", interaccion_quantity)
            for row in interaccion_quantity:
                interaccion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            tiempoact_query = get_tiempoact(request)
            cursor.execute(tiempoact_query)
            queries.append({"name": 'Tiempoact query', "query": tiempoact_query})
            tiempoact_quantity = cursor.fetchall()
            print("tiempoact quantity", tiempoact_quantity)
            for row in tiempoact_quantity:
                tiempoact_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            actividades_query = get_cant_touch(request)
            cursor.execute(actividades_query)
            queries.append({"name": 'Actividades query', "query": actividades_query})
            actividades_quantity = cursor.fetchall()
            print("actividades quantity", actividades_quantity)
            for row in actividades_quantity:
                actividades_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #FIN MUNDO ANIMAL 
        #filtro estudiente
        activate_student_filter = False
        if request.GET.get('student') and request.GET.get('student') != "0":
            activate_student_filter = True


        #INICIO PLUS SPACE
        #PLUS SPACE-------------------------------------
        #Creacion
        move_element_quantity_response = []
        volver_creacion_quantity_response = []
        aceptar_creacion_quantity_response = []
        ingresar_creacion_quantity_response = []
        planet_creacion_quantity_response = []
        planetS_creacion_quantity_response = []
        planetR_creacion_quantity_response = []
        star_creacion_quantity_response = []
        superNova_creacion_quantity_response = []
        nebulosa_creacion_quantity_response = []
        galaxy_creacion_quantity_response = []
        #Laberinto
        element_colission_quantity_response = []
        aceptar_laberinto_quantity_response = []
        volver_laberinto_quantity_response = []
        ingresar_laberinto_quantity_response = []
        #alternativas
        jump_alternativas_quantity_response = []
        correctas_alternativas_quantity_response = []
        incorrectas_alternativas_quantity_response = []
        aceptar_alternativas_quantity_response = []
        volver_alternativas_quantity_response = []
        ingresar_alternativas_quantity_response = []
        #busca
        correctas_busca_quantity_response = []
        incorrectas_busca_quantity_response = []
        aceptar_busca_quantity_response = []
        volver_busca_quantity_response = []
        ingresar_busca_quantity_response = []
        #cuida
        acierto_cuida_quantity_response = []
        aceptar_cuida_quantity_response = []
        volver_cuida_quantity_response = []
        ingresar_cuida_quantity_response = []
        #puzzle
        aceptar_puzzle_quantity_response = []
        volver_puzzle_quantity_response = []
        ingresar_puzzle_quantity_response = []
        
        if reim_num=="2":
        #CREACION
        #Elemento desplazado
            move_element_query = get_move_element_query(request)
            queries.append({"name": 'Desplazado query', "query": move_element_query})
            cursor.execute(move_element_query)
            move_element_quantity = cursor.fetchall()
            for row in move_element_quantity:
                move_element_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #Volver creacion
            volver_creacion_query = get_volver_creacion_query(request)
            queries.append({"name": 'volver creacion query', "query": volver_creacion_query})
            cursor.execute(volver_creacion_query)
            volver_creacion_quantity = cursor.fetchall()
            for row in volver_creacion_quantity:
                volver_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #aceptar creacion
            aceptar_creacion_query = get_aceptar_creacion_query(request)
            queries.append({"name": 'aceptar creacion query', "query": aceptar_creacion_query})
            cursor.execute(aceptar_creacion_query)
            aceptar_creacion_quantity = cursor.fetchall()
            for row in aceptar_creacion_quantity:
                aceptar_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #Ingresar creacion
            ingresar_creacion_query = get_ingresar_creacion_query(request)
            queries.append({"name": 'ingresar creacion query', "query": ingresar_creacion_query})
            cursor.execute(ingresar_creacion_query)
            ingresar_creacion_quantity = cursor.fetchall()
            for row in ingresar_creacion_quantity:
                ingresar_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #planeta creacion
            planet_creacion_query = get_planet_query(request)
            queries.append({"name": 'planet creacion query', "query": planet_creacion_query})
            cursor.execute(planet_creacion_query)
            planet_creacion_quantity = cursor.fetchall()
            for row in planet_creacion_quantity:
                planet_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #planeta con satelite creacion
            planetS_creacion_query = get_planet_satelite_query(request)
            queries.append({"name": 'planetS creacion query', "query": planetS_creacion_query})
            cursor.execute(planetS_creacion_query)
            planetS_creacion_quantity = cursor.fetchall()
            for row in planetS_creacion_quantity:
                planetS_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #Planeta con anillo creacion
            planetR_creacion_query = get_planet_ring_query(request)
            queries.append({"name": 'planetR creacion query', "query": planetR_creacion_query})
            cursor.execute(planetR_creacion_query)
            planetR_creacion_quantity = cursor.fetchall()
            for row in planetR_creacion_quantity:
                planetR_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #Estrella creacion
            star_creacion_query = get_star_query(request)
            queries.append({"name": 'Star creacion query', "query":star_creacion_query})
            cursor.execute(star_creacion_query)
            star_creacion_quantity = cursor.fetchall()
            for row in star_creacion_quantity:
               star_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #supernova creacion
            superNova_creacion_query = get_supernova_query(request)
            queries.append({"name": 'superNova creacion query', "query": superNova_creacion_query})
            cursor.execute(superNova_creacion_query)
            superNova_creacion_quantity = cursor.fetchall()
            for row in superNova_creacion_quantity:
                superNova_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #nebulosa creacion
            nebulosa_creacion_query = get_nebulosa_query(request)
            queries.append({"name": 'nebulosa creacion query', "query": nebulosa_creacion_query})
            cursor.execute(nebulosa_creacion_query)
            nebulosa_creacion_quantity = cursor.fetchall()
            for row in nebulosa_creacion_quantity:
                nebulosa_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #galaxia creacion
            galaxy_creacion_query = get_galaxy_query(request)
            queries.append({"name": 'galaxy creacion query', "query": galaxy_creacion_query})
            cursor.execute(galaxy_creacion_query)
            galaxy_creacion_quantity = cursor.fetchall()
            for row in galaxy_creacion_quantity:
                galaxy_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #LABERINTO
        #colisiones
            element_colission_query = get_element_colission_query(request)
            queries.append({"name": 'colisiones query', "query": element_colission_query})
            cursor.execute(element_colission_query)
            element_colission_quantity = cursor.fetchall()
            for row in element_colission_quantity:
                element_colission_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #aceptar
            aceptar_laberinto_query = get_aceptar_laberinto_query(request)
            queries.append({"name": 'aceptar laberinto query', "query": aceptar_laberinto_query})
            cursor.execute(aceptar_laberinto_query)
            aceptar_laberinto_quantity = cursor.fetchall()
            for row in aceptar_laberinto_quantity:
                aceptar_laberinto_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #volver
            volver_laberinto_query = get_volver_laberinto_query(request)
            queries.append({"name": 'volver laberinto query', "query": volver_laberinto_query})
            cursor.execute(volver_laberinto_query)
            volver_laberinto_quantity = cursor.fetchall()
            for row in volver_laberinto_quantity:
                volver_laberinto_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #ingresar
            ingresar_laberinto_query = get_ingresar_laberinto_query(request)
            queries.append({"name": 'ingresar laberinto query', "query": ingresar_laberinto_query})
            cursor.execute(ingresar_laberinto_query)
            ingresar_laberinto_quantity = cursor.fetchall()
            for row in ingresar_laberinto_quantity:
                ingresar_laberinto_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })       
        #ALTERNATIVAS
        #saltos
            jump_alternativas_query = get_jump_alternativas_query(request)
            queries.append({"name": 'Saltos query', "query": jump_alternativas_query})
            cursor.execute(jump_alternativas_query)
            jump_alternativas_quantity = cursor.fetchall()
            for row in jump_alternativas_quantity:
                jump_alternativas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #correctas
            correctas_alternativas_query = get_correctas_alternativas_query(request)
            queries.append({"name": 'Correctas Alternativas query', "query": correctas_alternativas_query})
            cursor.execute(correctas_alternativas_query)
            correctas_alternativas_quantity = cursor.fetchall()
            for row in correctas_alternativas_quantity:
                correctas_alternativas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #incorrectas
            incorrectas_alternativas_query = get_incorrectas_alternativas_query(request)
            queries.append({"name": 'Incorrectas Alternativas query', "query": incorrectas_alternativas_query})
            cursor.execute(incorrectas_alternativas_query)
            incorrectas_alternativas_quantity = cursor.fetchall()
            for row in incorrectas_alternativas_quantity:
                incorrectas_alternativas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #aceptar
            aceptar_alternativas_query = get_aceptar_alternativas_query(request)
            queries.append({"name": 'Aceptar Alternativas query', "query": aceptar_alternativas_query})
            cursor.execute(aceptar_alternativas_query)
            aceptar_alternativas_quantity = cursor.fetchall()
            for row in aceptar_alternativas_quantity:
                aceptar_alternativas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #volver
            volver_alternativas_query = get_volver_alternativas_query(request)
            queries.append({"name": 'Volver Alternativas query', "query": volver_alternativas_query})
            cursor.execute(volver_alternativas_query)
            volver_alternativas_quantity = cursor.fetchall()
            for row in volver_alternativas_quantity:
                volver_alternativas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #ingresar
            ingresar_alternativas_query = get_ingresar_alternativas_query(request)
            queries.append({"name": 'Ingresar Alternativas query', "query": ingresar_alternativas_query})
            cursor.execute(ingresar_alternativas_query)
            ingresar_alternativas_quantity = cursor.fetchall()
            for row in ingresar_alternativas_quantity:
                ingresar_alternativas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
#busca
        #correctas
            correctas_busca_query = get_correctas_busca_query(request)
            queries.append({"name": 'Correctas Busca query', "query": correctas_busca_query})
            cursor.execute(correctas_busca_query)
            correctas_busca_quantity = cursor.fetchall()
            for row in correctas_busca_quantity:
                correctas_busca_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #incorrectas
            incorrectas_busca_query = get_incorrectas_busca_query(request)
            queries.append({"name": 'Incorrrectas Busca query', "query": incorrectas_busca_query})
            cursor.execute(incorrectas_busca_query)
            incorrectas_busca_quantity = cursor.fetchall()
            for row in incorrectas_busca_quantity:
                incorrectas_busca_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #aceptar
            aceptar_busca_query = get_aceptar_busca_query(request)
            queries.append({"name": 'Aceptar Busca query', "query": aceptar_busca_query})
            cursor.execute(aceptar_busca_query)
            aceptar_busca_quantity = cursor.fetchall()
            for row in aceptar_busca_quantity:
                aceptar_busca_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #volver
            volver_busca_query = get_volver_busca_query(request)
            queries.append({"name": 'Volver Busca query', "query": volver_busca_query})
            cursor.execute(volver_busca_query)
            volver_busca_quantity = cursor.fetchall()
            for row in volver_busca_quantity:
                volver_busca_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #ingresar
            ingresar_busca_query = get_ingresar_busca_query(request)
            queries.append({"name": 'Ingresar Busca query', "query": ingresar_busca_query})
            cursor.execute(ingresar_busca_query)
            ingresar_busca_quantity = cursor.fetchall()
            for row in ingresar_busca_quantity:
                ingresar_busca_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #cuida
        #acierto
            acierto_cuida_query = get_acierto_cuida_query(request)
            queries.append({"name": 'Acierto Cuida query', "query": acierto_cuida_query})
            cursor.execute(acierto_cuida_query)
            acierto_cuida_quantity = cursor.fetchall()
            for row in acierto_cuida_quantity:
                acierto_cuida_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #aceptar
            aceptar_cuida_query = get_aceptar_cuida_query(request)
            queries.append({"name": 'Aceptar Cuida query', "query": aceptar_cuida_query})
            cursor.execute(aceptar_cuida_query)
            aceptar_cuida_quantity = cursor.fetchall()
            for row in aceptar_cuida_quantity:
                aceptar_cuida_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #volver
            volver_cuida_query = get_volver_cuida_query(request)
            queries.append({"name": 'Volver Cuida query', "query": volver_cuida_query})
            cursor.execute(volver_cuida_query)
            volver_cuida_quantity = cursor.fetchall()
            for row in volver_cuida_quantity:
                volver_cuida_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #ingresar
            ingresar_cuida_query = get_ingresar_cuida_query(request)
            queries.append({"name": 'Ingresar Cuida query', "query": ingresar_cuida_query})
            cursor.execute(ingresar_cuida_query)
            ingresar_cuida_quantity = cursor.fetchall()
            for row in ingresar_cuida_quantity:
                ingresar_cuida_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                get_acierto_cuida_query(request)
        #puzzle
        #aceptar
            aceptar_puzzle_query = get_aceptar_puzzle_query(request)
            queries.append({"name": 'Aceptar Puzzle query', "query": aceptar_puzzle_query})
            cursor.execute(aceptar_puzzle_query)
            aceptar_puzzle_quantity = cursor.fetchall()
            for row in aceptar_puzzle_quantity:
                aceptar_puzzle_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #volver
            volver_puzzle_query = get_volver_puzzle_query(request)
            queries.append({"name": 'Volver Puzzle query', "query": volver_puzzle_query})
            cursor.execute(volver_puzzle_query)
            volver_puzzle_quantity = cursor.fetchall()
            for row in volver_puzzle_quantity:
                volver_puzzle_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #ingresar
            ingresar_puzzle_query = get_ingresar_puzzle_query(request)
            queries.append({"name": 'Ingresar Puzzle query', "query": ingresar_puzzle_query})
            cursor.execute(ingresar_puzzle_query)
            ingresar_puzzle_quantity = cursor.fetchall()
            for row in ingresar_puzzle_quantity:
                ingresar_puzzle_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        
        #FIN PLUS SPACE

        #INICIO CLEAN OCEAN
        colision_quantity_response = []
        corrects_quantity_response = []
        incorrects_quantity_response = []
        jumps_quantity_response = []
        analytics_co_quantity_response = []
        exit_lab_quantity_response = []
        touch_animals_co_quantity_response = []
        touch_trash_co_quantity_response = []

        if reim_num=="3":
            colision_query = get_colision_co(request)
            cursor.execute(colision_query)
            queries.append({"name": 'Colision query', "query": colision_query})
            colision_quantity = cursor.fetchall()
            print ("colision quantity" , colision_quantity)
            for row in colision_quantity:
                colision_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        
            corrects_query = get_corrects_co(request)
            cursor.execute(corrects_query)
            queries.append({"name": 'Corrects query', "query": corrects_query})
            corrects_quantity = cursor.fetchall()
            for row in corrects_quantity:
                corrects_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            incorrects_query = get_incorrects_co(request)
            cursor.execute(incorrects_query)
            queries.append({"name": 'Incorrects query', "query": incorrects_query})
            incorrects_quantity = cursor.fetchall()
            for row in incorrects_quantity:
                incorrects_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            jumps_query = get_jumps_co(request)
            cursor.execute(jumps_query)
            queries.append({"name": 'Jumps query', "query": jumps_query})
            jumps_quantity = cursor.fetchall()
            for row in jumps_quantity:
                jumps_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
            
            analytics_co_query = get_analytics_co(request)
            cursor.execute(analytics_co_query)
            queries.append({"name": 'Analytics co query', "query": analytics_co_query})
            analytics_co_quantity = cursor.fetchall()
            print ("analytics_co_quantity", analytics_co_quantity)
            for row in analytics_co_quantity:
                analytics_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'correctsact1': row[2], 'incorrectsact1': row[3], 'correctsact2': row[4], 'incorrectsact2': row[5]  })

            exit_lab_query = get_exit_lab(request)
            cursor.execute(exit_lab_query)
            queries.append({"name": 'Exit lab query', "query": exit_lab_query})
            exit_lab_quantity = cursor.fetchall()
            for row in exit_lab_quantity:
                exit_lab_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            touch_animals_co_query = get_touch_animals_co(request)
            cursor.execute(touch_animals_co_query)
            queries.append({"name": 'Touch animals co query', "query": touch_animals_co_query})
            touch_animals_co_quantity = cursor.fetchall()
            print ("Touch animals co quantity" , touch_animals_co_quantity)
            for row in touch_animals_co_quantity:
                touch_animals_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            touch_trash_co_query = get_touch_trash_co(request)
            cursor.execute(touch_trash_co_query)
            queries.append({"name": 'Touch trash co query', "query": touch_trash_co_query})
            touch_trash_co_quantity = cursor.fetchall()
            print ("Touch trash co quantity" , touch_trash_co_quantity)
            for row in touch_trash_co_quantity:
                touch_trash_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
            

        #FIN CLEAN OCEAN
        
        #Cantidad de Sesiones
        session_query = get_session_query(request)
        cursor.execute(session_query)
        queries.append({"name": 'Session query', "query": session_query})
        sesion_quantity = cursor.fetchall()
        sesion_quantity_response = []
        for row in sesion_quantity:
            sesion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        activate_graphics = activate_course_filter and activate_school_filter and activate_reim_filter
        activate_graphics_general = activate_activity_filter and activate_course_filter and activate_school_filter and activate_reim_filter
        activate_graphics_student = activate_course_filter and activate_school_filter and activate_reim_filter and activate_student_filter
       
        return render(
            request,
            "users/welcome.html",
            {
                # Show graphics at the init
                'activate_graphics': activate_graphics,
                'activate_graphics_general':activate_graphics_general,
                'activate_graphics_student':activate_graphics_student,
                # Other context var
                'queries': queries,
                'schools': schools_response,
                'reims': reims_response,
                'game_time': game_time_response,
                'courses': courses_response,
                'activities': activities_response,
                'students': students_response,
                'touch_quantity': touch_quantity_response,
                'sesion_quantity': sesion_quantity_response,
                'cant_usuarios':cant_usuarios,
                'activity_num':activity_num,
                'student_num':student_num,
                'reim_num':reim_num,
                'colision_quantity':colision_quantity_response,
                'corrects_quantity':corrects_quantity_response,
                'incorrects_quantity':incorrects_quantity_response,
                'jumps_quantity':jumps_quantity_response,
                'analytics_co_quantity':analytics_co_quantity_response,
                'exit_lab_quantity': exit_lab_quantity_response,
                'touch_animals_co_quantity':touch_animals_co_quantity_response,
                'touch_trash_co_quantity':touch_trash_co_quantity_response,
                'piezas_quantity':piezas_quantity_response,
                'malas_quantity':malas_quantity_response,
                'animales_quantity':animales_quantity_response,
                'actividades_quantity':actividades_quantity_response,
                'interaccion_quantity':interaccion_quantity_response,
                'tiempoact_quantity':tiempoact_quantity_response,
                                
                #PLUSSPACE
                #CREACION
                'move_element_quantity':move_element_quantity_response,
                'ingresar_creacion_quantity':ingresar_creacion_quantity_response,
                'aceptar_creacion_quantity':aceptar_creacion_quantity_response,
                'volver_creacion_quantity':volver_creacion_quantity_response,
                'planet_creacion_quantity':planet_creacion_quantity_response,
                'planetS_creacion_quantity':planetS_creacion_quantity_response,
                'planetR_creacion_quantity':planetR_creacion_quantity_response,
                'star_creacion_quantity':star_creacion_quantity_response,
                'superNova_creacion_quantity':superNova_creacion_quantity_response,
                'nebulosa_creacion_quantity':nebulosa_creacion_quantity_response,
                'galaxy_creacion_quantity':galaxy_creacion_quantity_response,
                #LABERINTO
                'element_colission_quantity':element_colission_quantity_response,
                'aceptar_laberinto_quantity':aceptar_laberinto_quantity_response,
                'volver_laberinto_quantity':volver_laberinto_quantity_response,
                'ingresar_laberinto_quantity':ingresar_laberinto_quantity_response,
                #ALTERNATIVAS
                'jump_alternativas_quantity':jump_alternativas_quantity_response,
                'correctas_alternativas_quantity':correctas_alternativas_quantity_response,
                'incorrectas_alternativas_quantity':incorrectas_alternativas_quantity_response,
                'aceptar_alternativas_quantity':aceptar_alternativas_quantity_response,
                'volver_alternativas_quantity':volver_alternativas_quantity_response,
                'ingresar_alternativas_quantity':ingresar_alternativas_quantity_response,
                #BUSCA
                'correctas_busca_quantity':correctas_busca_quantity_response,
                'incorrectas_busca_quantity':incorrectas_busca_quantity_response,
                'aceptar_busca_quantity':aceptar_busca_quantity_response,
                'volver_busca_quantity':volver_busca_quantity_response,
                'ingresar_busca_quantity':ingresar_busca_quantity_response,
                #CUIDA
                'acierto_cuida_quantity':acierto_cuida_quantity_response,
                'aceptar_cuida_quantity':aceptar_cuida_quantity_response,
                'volver_cuida_quantity':volver_cuida_quantity_response,
                'ingresar_cuida_quantity':ingresar_cuida_quantity_response, 
                #PUZZLE
                'aceptar_puzzle_quantity':aceptar_puzzle_quantity_response,
                'volver_puzzle_quantity':volver_puzzle_quantity_response,
                'ingresar_puzzle_quantity':ingresar_puzzle_quantity_response,
            })
    # En otro caso redireccionamos al login
    return redirect('/login')

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/register.html", {'form': form})

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
             #Conectamos con la db de ulearnet][_h]
        cursor = get_from_db()
        query = 'SELECT username, email, password, nombres FROM usuario WHERE (tipo_usuario_id = 1 OR tipo_usuario_id = 2) AND (username="' + request.POST.get('username') +'" AND password="' + request.POST.get('password') + '")'
        cursor.execute(query)
        data = cursor.fetchone()
        
        if data:
            user, created = User.objects.get_or_create(username=data[0], email=data[1], first_name=data[3])
            if created:
                user.set_password(data[2])
                user.save()
        else:
            print("nada")
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')
        else:
            print(form)

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')