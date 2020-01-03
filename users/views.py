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
        #print(time_query)
        queries.append({"name": 'Time query', "query": time_query })
        cursor.execute(time_query)
        game_time = cursor.fetchall()
        game_time_response = []
        for row in game_time:
            game_time_response.append({ 'id': row[0], 'name': row[1], 'time': row[2] })
        game_time_graph = len(game_time)*40+20

        #Touch
        touch_query = get_touch_query(request)
        queries.append({"name": 'Touch query', "query": touch_query})
        cursor.execute(touch_query)
        touch_quantity = cursor.fetchall()
        touch_quantity_response = []
        for row in touch_quantity:
            touch_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        touch_quantity_graph = len(touch_quantity)*40+20

        #Cantidad de Usuarios
        cant_usuarios = get_alumnos(request)
        #print("largo de graficos")
        #print(cant_usuarios)
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
        analytics1_co_quantity_response=[]
        tiempo_total_quantity_response=[]
        audios_quantity_response=[]
        total_correctas = 0
        count1=1
        promedio_correctas=0
        animales_quantity_graph=0
        total_incorrectas = 0
        count2=1
        promedio_incorrectas=0


        if reim_num=="1":

            analytics1_co_query = get_analytics1_co(request)
            cursor.execute(analytics1_co_query)
            queries.append({"name": 'Analytics1 co query', "query": analytics1_co_query})
            analytics1_co_quantity = cursor.fetchall()
            #print ("analytics1_co_quantity", analytics1_co_quantity)
            for row in analytics1_co_quantity:
                analytics1_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'act1': row[2], 'act2': row[3], 'act3': row[4], 'act4': row[5]  })
           
            piezas_query = get_piezas(request)
            cursor.execute(piezas_query)
            queries.append({"name": 'Piezas query', "query": piezas_query})
            piezas_quantity = cursor.fetchall()
            #print ("piezas quantity", piezas_quantity)
            for row in piezas_quantity:
                piezas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                total_correctas += row[2]
                count1 = count1+1
            promedio_correctas = total_correctas / count1         

            malas_query = get_malas(request)
            cursor.execute(malas_query)
            queries.append({"name": 'Malas query', "query": malas_query})
            malas_quantity = cursor.fetchall()
            #print("malas quantity", malas_quantity)
            for row in malas_quantity:
                malas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                total_incorrectas += row[2]
                count2 = count2+1
            promedio_incorrectas = total_incorrectas / count2

            animales_query = get_animals(request)
            cursor.execute(animales_query)
            queries.append({"name": 'Animales query', "query": animales_query})
            animales_quantity = cursor.fetchall()
            #print("animales quantity", animales_quantity)
            for row in animales_quantity:
                animales_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
            animales_quantity_graph = len(animales_quantity)*40+20    
            
            
            interaccion_query = get_interaccion(request)
            cursor.execute(interaccion_query)
            queries.append({"name": 'Interaccion query', "query": interaccion_query})
            interaccion_quantity = cursor.fetchall()
            #print("interacccion quantity", interaccion_quantity)
            for row in interaccion_quantity:
                interaccion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            tiempoact_query = get_tiempoact(request)
            cursor.execute(tiempoact_query)
            queries.append({"name": 'Tiempoact query', "query": tiempoact_query})
            tiempoact_quantity = cursor.fetchall()
            #print("tiempoact quantity", tiempoact_quantity)
            for row in tiempoact_quantity:
                tiempoact_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            actividades_query = get_cant_touch(request)
            cursor.execute(actividades_query)
            queries.append({"name": 'Actividades query', "query": actividades_query})
            actividades_quantity = cursor.fetchall()
            #print("actividades quantity", actividades_quantity)
            for row in actividades_quantity:
                actividades_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            tiempo_total_query = get_tiempo_total_act(request)
            cursor.execute(tiempo_total_query)
            queries.append({"name": 'Tiempo total por act query', "query": tiempo_total_query})
            tiempo_total_quantity = cursor.fetchall()
            #print("tiempo total por act quantity", tiempo_total_quantity)
            for row in tiempo_total_quantity:
                tiempo_total_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            audios_query = get_audios(request)
            cursor.execute(audios_query)
            queries.append({"name": 'Audios query', "query": audios_query})
            audios_quantity = cursor.fetchall()
            for row in audios_quantity:
                audios_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #FIN MUNDO ANIMAL 

        #filtro estudiente
        activate_student_filter = False
        if request.GET.get('student') and request.GET.get('student') != "0":
            activate_student_filter = True
        #INICIO PLUS SPACE
        #PLUS SPACE-------------------------------------
        #General
        time_PS_quantity_response = []
        correctas_PS_quantity_response = []
        move_element_quantity_response = []
        elementos_PS_quantity_response = []
        element_colission_quantity_response = []
        posicionamiento_PS_quantity_response = []
        jump_alternativas_quantity_response = []
        acierto_cuida_quantity_response = []
        completa_incompleta_PS_quantity_response = []
        tiempoXact_quantity_response = []
        jumpxalumno_quantity_response = []
        elementosXalum_PS_quantity_response = []
        element_colission_alum_quantity_response=[]
        posicionamiento_alu_PS_quantity_response=[]
        acierto_cuida_alu_quantity_response=[]
        time_PS_graf = 0
        correctas_PS_graf = 0
        move_element_graf = 0
        elementos_PS_graf = 0
        element_colission_graf = 0
        posicionamiento_PS_graf = 0
        jump_alternativas_graf = 0
        acierto_cuida_graf = 0
        completa_incompleta_PS_graf = 0
        i=0
        construccion_PS_quantity_response=[]
        saltos_PS_quantity_response=[]
        colisiones_PS_quantity_response=[]
        sesiones_PS_quantity_response=[]
        puzzle_PS_quantity_response=[]
        ingreso_puzzle_PS_quantity_response=[]
        construccion=0
        colisiones=0
        saltos = 0
        puzzle=0
        sesiones = 0
        
        if reim_num=="2":       

        #General
            sesiones_PS_query = get_time_act_co(request)
            queries.append({"name": 'Tiempo Actividad query', "query": sesiones_PS_query})
            cursor.execute(sesiones_PS_query)
            sesiones_PS_quantity = cursor.fetchall()
            for row in sesiones_PS_quantity:
                sesiones_PS_quantity_response.append({ 'id': row[0]})
       
            time_PS_query = get_time_act_co(request)
            queries.append({"name": 'Tiempo Actividad query', "query": time_PS_query})
            cursor.execute(time_PS_query)
            time_PS_quantity = cursor.fetchall()
            for row in time_PS_quantity:
                time_PS_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #tiempo por actividad general
            tiempoXact_query = get_tiempoact(request)
            cursor.execute(tiempoXact_query)
            queries.append({"name": 'TiempoXact query', "query": tiempoXact_query})
            tiempoXact_quantity = cursor.fetchall()
            print("tiempoXact quantity", tiempoXact_quantity)
            for row in tiempoXact_quantity:
                tiempoXact_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #CREACION
        #Elemento desplazado
            move_element_query = get_move_element_query(request)
            queries.append({"name": 'Desplazado query', "query": move_element_query})
            cursor.execute(move_element_query)
            move_element_quantity = cursor.fetchall()
            for row in move_element_quantity:
                move_element_quantity_response.append({ 'id': row[0], 'fila': row[1], 'columna':row[2] })
        #ELEMENTOS creacion
            elementos_PS_query = get_elementos_PS(request)
            queries.append({"name": 'planet creacion query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                elementos_PS_quantity_response.append({ 'id': row[0], 'name': row[1], 'planeta': row[2], 'planetaCS': row[3], 'planetaCA': row[4], 'estrella': row[5], 'supernova': row[6], 'nebulosa': row[7], 'galaxia': row[8] })
        #ELEMENTOS creacion
            elementosXalum_PS_query = get_elementos_alum_PS(request)
            queries.append({"name": 'planet creacion x alumno query', "query": elementosXalum_PS_query})
            cursor.execute(elementosXalum_PS_query)
            elementosXalum_PS_quantity = cursor.fetchall()
            i=0
            for row in elementosXalum_PS_quantity:
                i=i+1
                elementosXalum_PS_quantity_response.append({ 'id': i, 'name': row[0], 'elemento': row[0]})
        #construcción PS analitica
            construccion_PS_query = get_construccion_PS(request)
            queries.append({"name": 'construcción query', "query": construccion_PS_query})
            cursor.execute(construccion_PS_query)
            construccion_PS_quantity = cursor.fetchall()
            for row in construccion_PS_quantity:
                construccion_PS_quantity_response.append({ 'id': row[0], 'name': row[1]})
        #saltos PS analitica
            saltos_PS_query = get_saltos_analitica_PS(request)
            queries.append({"name": 'saltos analitica query', "query": saltos_PS_query})
            cursor.execute(saltos_PS_query)
            saltos_PS_quantity = cursor.fetchall()
            for row in saltos_PS_quantity:
                saltos_PS_quantity_response.append({ 'id': row[0], 'name': row[1]})
        #colisiones PS analitica
            colisiones_PS_query = get_colisiones_analitica_PS(request)
            queries.append({"name": 'colisiones analitica query', "query": colisiones_PS_query})
            cursor.execute(colisiones_PS_query)
            colisiones_PS_quantity = cursor.fetchall()
            for row in colisiones_PS_quantity:
                colisiones_PS_quantity_response.append({ 'id': row[0], 'name': row[1]})
        #puzzle PS analitica
            puzzle_PS_query = get_puzzle_PS(request)
            queries.append({"name": 'construcción query', "query": puzzle_PS_query})
            cursor.execute(puzzle_PS_query)
            puzzle_PS_quantity = cursor.fetchall()
            for row in puzzle_PS_quantity:
                puzzle_PS_quantity_response.append({ 'id': row[0], 'name': row[1]})
        #ingreso puzzle PS analitica
            ingreso_puzzle_PS_query = get_ingreso_puzzle_PS(request)
            queries.append({"name": 'construcción query', "query": ingreso_puzzle_PS_query})
            cursor.execute(ingreso_puzzle_PS_query)
            ingreso_puzzle_PS_quantity = cursor.fetchall()
            for row in ingreso_puzzle_PS_quantity:
                ingreso_puzzle_PS_quantity_response.append({ 'id': row[0], 'name': row[1]})
        #LABERINTO
        #posicionamiento
            posicionamiento_PS_query = get_posicionamiento_PS(request)
            queries.append({"name": 'posicionamiento_PS query', "query": posicionamiento_PS_query})
            cursor.execute(posicionamiento_PS_query)
            posicionamiento_PS_quantity = cursor.fetchall()
            for row in posicionamiento_PS_quantity:
                posicionamiento_PS_quantity_response.append({ 'id': row[0], 'name': row[1], 'tierra': row[2], 'neptuno': row[3], 'jupiter': row[4], 'saturno': row[5], 'urano': row[6], 'venus': row[7], 'mercurio': row[8], 'marte': row[9] })
        #posicionamiento
            posicionamiento_alu_PS_query = get_posicionamiento_alu_PS(request)
            queries.append({"name": 'posicionamiento_alu_PS query', "query": posicionamiento_alu_PS_query})
            cursor.execute(posicionamiento_alu_PS_query)
            posicionamiento_alu_PS_quantity = cursor.fetchall()
            for row in posicionamiento_alu_PS_quantity:
                i=i+1
                posicionamiento_alu_PS_quantity_response.append({ 'id': i, 'name': row[0], 'elemento': row[0]})

        #colisiones
            element_colission_query = get_element_colission_query(request)
            queries.append({"name": 'colisiones query', "query": element_colission_query})
            cursor.execute(element_colission_query)
            element_colission_quantity = cursor.fetchall()
            for row in element_colission_quantity:
                element_colission_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #colisiones x alumno
            element_colission_alum_query = get_element_colission_alu_query(request)
            queries.append({"name": 'colisionesxalumno query', "query": element_colission_alum_query})
            cursor.execute(element_colission_alum_query)
            element_colission_alum_quantity = cursor.fetchall()
            i=0
            for row in element_colission_alum_quantity:
                i=i+1
                element_colission_alum_quantity_response.append({ 'id':i ,'name': row[0], 'quantity': row[1] })
        
        #ALTERNATIVAS
        #saltos
            jump_alternativas_query = get_jump_alternativas_query(request)
            queries.append({"name": 'Saltos query', "query": jump_alternativas_query})
            cursor.execute(jump_alternativas_query)
            jump_alternativas_quantity = cursor.fetchall()
            for row in jump_alternativas_quantity:
                jump_alternativas_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #saltosxalumno
            jumpxalumno_query = get_jump_alternativas_alu_query(request)
            queries.append({"name": 'Saltosxalumno query', "query": jumpxalumno_query})
            cursor.execute(jumpxalumno_query)
            jumpxalumno_quantity = cursor.fetchall()
            i=0
            for row in jumpxalumno_quantity:
                i=i+1
                jumpxalumno_quantity_response.append({ 'id':i ,'name': row[0], 'quantity': row[1] })
        
        #busca
        #CORRECTAS INCORRECTAS
            correctas_PS_query = get_corrects_incorrects_co(request)
            queries.append({"name": 'Correctas PS query', "query": correctas_PS_query})
            cursor.execute(correctas_PS_query)
            correctas_PS_quantity = cursor.fetchall()
            for row in correctas_PS_quantity:
                correctas_PS_quantity_response.append({ 'id': row[0], 'name': row[1], 'correct': row[2], 'incorrect': row[3] })
       #COMPLETAS INCOMPLETAS
            completa_incompleta_PS_query = get_completa_incompleta_PS(request)
            queries.append({"name": 'Completas incompletas query', "query": completa_incompleta_PS_query})
            cursor.execute(completa_incompleta_PS_query)
            completa_incompleta_PS_quantity = cursor.fetchall()
            for row in completa_incompleta_PS_quantity:
                completa_incompleta_PS_quantity_response.append({ 'id': row[0], 'name': row[1], 'completa': row[2], 'incompleta': row[3], 'inactiva': row[4] })
       #cuida
        #acierto
            acierto_cuida_query = get_acierto_cuida_query(request)
            queries.append({"name": 'Acierto Cuida query', "query": acierto_cuida_query})
            cursor.execute(acierto_cuida_query)
            acierto_cuida_quantity = cursor.fetchall()
            for row in acierto_cuida_quantity:
                acierto_cuida_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #acierto x alumno
            acierto_cuida_alu_query = get_acierto_cuida_alu_query(request)
            queries.append({"name": 'Acierto Cuida query', "query": acierto_cuida_alu_query})
            cursor.execute(acierto_cuida_alu_query)
            acierto_cuida_alu_quantity = cursor.fetchall()
            i=0
            for row in acierto_cuida_alu_quantity:
                i=i+1
                acierto_cuida_alu_quantity_response.append({ 'id':i ,'name': row[0], 'quantity': row[1] })
        
            
        #otros
        time_PS_graf = len(time_PS_quantity_response) * 40+20
        correctas_PS_graf = len(correctas_PS_quantity_response) * 40+100
        elementos_PS_graf = len(elementos_PS_quantity_response) * 40+100
        element_colission_graf = len(element_colission_quantity_response) * 40+20
        posicionamiento_PS_graf = len(posicionamiento_PS_quantity_response) * 40+100
        jump_alternativas_graf = len(jump_alternativas_quantity_response) * 40+20
        acierto_cuida_graf = len(acierto_cuida_quantity_response) * 40+20
        completa_incompleta_PS_graf = len(completa_incompleta_PS_quantity_response) * 40+100
        
        #Analitica
    
        sesiones= len(sesiones_PS_quantity_response)
        if(len(construccion_PS_quantity_response)!=0 or len(sesiones_PS_quantity_response)!=0 ):
            construccion=(len(construccion_PS_quantity_response)/len(sesiones_PS_quantity_response))
        if(len(construccion_PS_quantity_response)==0 or len(sesiones_PS_quantity_response)==0 ):
            construccion=0
        if(len(saltos_PS_quantity_response)!=0 or len(sesiones_PS_quantity_response)!=0):
            saltos=(len(saltos_PS_quantity_response)/len(sesiones_PS_quantity_response))
        if(len(saltos_PS_quantity_response)==0 or len(sesiones_PS_quantity_response)==0):
            saltos=0
        if(len(colisiones_PS_quantity_response)!=0 or len(sesiones_PS_quantity_response)!=0):
            colisiones=(len(colisiones_PS_quantity_response)/len(sesiones_PS_quantity_response))
        if(len(colisiones_PS_quantity_response)==0 or len(sesiones_PS_quantity_response)==0):
            colisiones=0
        if(len(puzzle_PS_quantity_response)!=0 or ingreso_puzzle_PS_quantity_response!=0 or len(sesiones_PS_quantity_response)!=0):
            puzzle=(len(puzzle_PS_quantity_response)/len(ingreso_puzzle_PS_quantity_response))/len(sesiones_PS_quantity_response)
        if(len(puzzle_PS_quantity_response)==0 or len(sesiones_PS_quantity_response)==0):
            puzzle=0
        print("contruccion")
        print(construccion)
        print("saltos")
        print(saltos)
        print("sesiones")
        print(sesiones)
        #FIN PLUS SPACE

        #INICIO CLEAN OCEAN

        #List Querys
        colision_quantity_response = []
        corrects_quantity_response = []
        incorrects_quantity_response = []
        jumps_quantity_response = []
        analytics_co_quantity_response = []
        exit_lab_quantity_response = []
        touch_animals_co_quantity_response = []
        touch_trash_co_quantity_response = []
        actividades_co_quantity_response = []
        colision_trash_quantity_response = []
        touch_all_animals_quantity_response = []
        exits_lab_co_quantity_response = []
        touch_all_trash_quantity_response = []
        buttons_co_quantity_response = []
        trash_clean_co_quantity_response = []
        corrects_student_co_quantity_response = []
        time_act_co_quantity_response = []
        corrects_incorrects_quantity_response = []
        #Promedios
        countCO = 0
        promedio_saltos = 0
        total_jumps = 0
        total_corrects_co = 0
        total_incorrects_co = 0
        total_colisions = 0
        promedio_correctas_co = 0
        promedio_incorrectas_co = 0
        promedio_colisions = 0

        #Size Graphs
        colision_quantity_graph = 0
        corrects_quantity_graph = 0
        corrects_incorrects_quantity_graph = 0
        jumps_quantity_graph = 0
        analytics_co_quantity_graph = 0
        actividades_co_quantity_graph = 0
        exit_lab_quantity_graph = 0
        touch_trash_co_quantity_graph = 0
        corrects_student_co_quantity_graph = 0
        colision_trash_quantity_graph = 0
        exits_lab_co_quantity_graph = 0
        touch_all_trash_quantity_graph = 0
        buttons_co_quantity_graph = 0
        trash_clean_co_quantity_graph = 0
        time_act_co_quantity_graph = 0
        # def redondear(int n):

        if reim_num=="3":
            if activity_num=="3004" or activity_num=="3002" or activity_num=="3006":
                #actividad 3004, 3002, 3006
                colision_query = get_colision_co(request)
                cursor.execute(colision_query)
                queries.append({"name": 'Colision query', "query": colision_query})
                colision_quantity = cursor.fetchall()
                #print ("colision quantity" , colision_quantity)
                for row in colision_quantity:
                    colision_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                    total_colisions += row[2]
                    countCO = countCO+1
                if (countCO!=0):
                    promedio_colisions = total_colisions / countCO
                else:
                    promedio_colisions = total_colisions / 1
                colision_quantity_graph = len(colision_quantity)*40+20


            if activity_num=="3005":
                #3005
                corrects_query = get_corrects_co(request)
                cursor.execute(corrects_query)
                queries.append({"name": 'Corrects query', "query": corrects_query})
                corrects_quantity = cursor.fetchall()
                for row in corrects_quantity:
                    corrects_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                corrects_quantity_graph = len(corrects_quantity)*40+20

                jumps_query = get_jumps_co(request)
                cursor.execute(jumps_query)
                queries.append({"name": 'Jumps query', "query": jumps_query})
                jumps_quantity = cursor.fetchall()
                for row in jumps_quantity:
                    jumps_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                    total_jumps += row[2]
                    countCO = countCO+1
                if (countCO!=0):
                    promedio_saltos = total_jumps / countCO
                else:
                    promedio_saltos = total_jumps / 1
                jumps_quantity_graph = len(jumps_quantity)*40+20

            if activity_num=="3002" or activity_num=="3003" or activity_num=="3004" or activity_num=="3006" or activity_num=="3007":
                #3002 3003 3004 3006 3007
                corrects_incorrects_query = get_corrects_incorrects_co(request)
                cursor.execute(corrects_incorrects_query)
                queries.append({"name": 'Correctas e incorrectas query', "query": corrects_incorrects_query})
                corrects_incorrects_quantity = cursor.fetchall()
                for row in corrects_incorrects_quantity:
                    corrects_incorrects_quantity_response.append({ 'id': row[0], 'name': row[1], 'corrects': row[2], 'incorrects': row[3] })
                    total_corrects_co += row[2]
                    total_incorrects_co += row[3]
                    countCO = countCO+1
                if (countCO!=0):
                    promedio_correctas_co = total_corrects_co / countCO
                    promedio_incorrectas_co = total_incorrects_co / countCO
                else:
                    promedio_correctas_co = total_corrects_co / 1
                    promedio_incorrectas_co = total_incorrects_co / 1
                corrects_incorrects_quantity_graph = len(corrects_incorrects_quantity)*40+20

            
            if activity_num=="0":
                # act = 0
                analytics_co_query = get_analytics_co(request)
                cursor.execute(analytics_co_query)
                queries.append({"name": 'Analytics co query', "query": analytics_co_query})
                analytics_co_quantity = cursor.fetchall()
                #print ("analytics_co_quantity", analytics_co_quantity)
                for row in analytics_co_quantity:
                    analytics_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'correctsact1': row[2], 'correctsact2': row[3] })
                analytics_co_quantity_graph = len(analytics_co_quantity)*40+20

                actividades_co_query = get_cant_touch_act_co(request)
                cursor.execute(actividades_co_query)
                queries.append({"name": 'Actividades CO query', "query": actividades_co_query})
                actividades_co_quantity = cursor.fetchall()
                #print("actividades CO quantity", actividades_co_quantity)
                for row in actividades_co_quantity:
                    actividades_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                actividades_co_quantity_graph = len(actividades_co_quantity)*40+20

            if student_num!="0":
                #student =!0
                exit_lab_query = get_exit_lab(request)
                cursor.execute(exit_lab_query)
                queries.append({"name": 'Exit lab query', "query": exit_lab_query})
                exit_lab_quantity = cursor.fetchall()
                for row in exit_lab_quantity:
                    exit_lab_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                exit_lab_quantity_graph = len(exit_lab_quantity)*40+20

                touch_trash_co_query = get_touch_trash_co(request)
                cursor.execute(touch_trash_co_query)
                queries.append({"name": 'Touch trash co query', "query": touch_trash_co_query})
                touch_trash_co_quantity = cursor.fetchall()
                #print ("Touch trash co quantity" , touch_trash_co_quantity)
                for row in touch_trash_co_quantity:
                    touch_trash_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                touch_trash_co_quantity_graph = len(touch_trash_co_quantity)*40+20

                # student=! 0
                #correctas e incorrectas para c/ alumno x actividad
                corrects_student_co_query = get_corrects_student_co(request)
                cursor.execute(corrects_student_co_query)
                queries.append({"name": 'Corrects students CO query', "query": corrects_student_co_query})
                corrects_student_co_quantity = cursor.fetchall()
                #print ("Corrects students CO quantity" , corrects_student_co_quantity)
                for row in corrects_student_co_quantity:
                    corrects_student_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'correct': row[2], 'incorrect': row[3] })
                corrects_student_co_quantity_graph = len(corrects_student_co_quantity)*40+20

            # touch_animals_co_query = get_touch_animals_co(request)
            # cursor.execute(touch_animals_co_query)
            # queries.append({"name": 'Touch animals co query', "query": touch_animals_co_query})
            # touch_animals_co_quantity = cursor.fetchall()
            # #print ("Touch animals co quantity" , touch_animals_co_quantity)
            # for row in touch_animals_co_quantity:
            #     touch_animals_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            if activity_num=="3002":
                colision_trash_query = get_colision_trash(request)
                cursor.execute(colision_trash_query)
                queries.append({"name": 'Colision trash query', "query": colision_trash_query})
                colision_trash_quantity = cursor.fetchall()
                #print("Colision trash quantity", colision_trash_quantity)
                for row in colision_trash_quantity:
                    colision_trash_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                colision_trash_quantity_graph = len(colision_trash_quantity)*40+20


            # touch_all_animals_query = get_touch_all_animals(request)
            # cursor.execute(touch_all_animals_query)
            # queries.append({"name": 'Touch all animals query', "query": touch_all_animals_query})
            # touch_all_animals_quantity = cursor.fetchall()
            # #print ("Touch all animals quantity" , touch_all_animals_quantity)
            # for row in touch_all_animals_quantity:
            #     touch_all_animals_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            # !!!!!!!!!!!!!!
            if activity_num == "3004":
                exits_lab_co_query = get_exits_lab_co(request)
                cursor.execute(exits_lab_co_query)
                queries.append({"name": 'Exits lab co query', "query": exits_lab_co_query})
                exits_lab_co_quantity = cursor.fetchall()
                #print ("Exits lab co quantity" , exits_lab_co_quantity)
                for row in exits_lab_co_quantity:
                    exits_lab_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                exits_lab_co_quantity_graph = len(exits_lab_co_quantity)*40+20

            if activity_num=="3000":
                # act 3000
                touch_all_trash_query = get_touch_all_trash(request)
                cursor.execute(touch_all_trash_query)
                queries.append({"name": 'Touch all trash query', "query": touch_all_trash_query})
                touch_all_trash_quantity = cursor.fetchall()
                #print ("Touch all trash quantity" , touch_all_trash_quantity)
                for row in touch_all_trash_quantity:
                    touch_all_trash_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                touch_all_trash_quantity_graph = len(touch_all_trash_quantity)*40+20
            
            if activity_num!="0":
                #3000 3001 3002 3003 3004 3005 3006 3007
                buttons_co_query = get_buttons_co(request)
                cursor.execute(buttons_co_query)
                queries.append({"name": 'Buttons CO query', "query": buttons_co_query})
                buttons_co_quantity = cursor.fetchall()
                #print ("Buttons CO quantity" , buttons_co_quantity)
                for row in buttons_co_quantity:
                    buttons_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                buttons_co_quantity_graph = len(buttons_co_quantity)*40+20

            if activity_num=="3007":
                trash_clean_co_query = get_trash_clean_co(request)
                cursor.execute(trash_clean_co_query)
                queries.append({"name": 'Trash clean CO query', "query": trash_clean_co_query})
                trash_clean_co_quantity = cursor.fetchall()
                #print ("Trash clean CO quantity" , trash_clean_co_quantity)
                for row in trash_clean_co_quantity:
                    trash_clean_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                trash_clean_co_quantity_graph = len(trash_clean_co_quantity)*40+20

            if activity_num!="3000" and activity_num!="3001" and activity_num!="0":
                time_act_co_query = get_time_act_co(request)
                cursor.execute(time_act_co_query)
                queries.append({"name": 'Time act CO query', "query": time_act_co_query})
                time_act_co_quantity = cursor.fetchall()
                #print ("Time act CO quantity" , time_act_co_quantity)
                for row in time_act_co_quantity:
                    time_act_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                time_act_co_quantity_graph = len(time_act_co_quantity)*40+20

        #FIN CLEAN OCEAN
        
        #Cantidad de Sesiones
        session_query = get_session_query(request)
        cursor.execute(session_query)
        queries.append({"name": 'Session query', "query": session_query})
        sesion_quantity = cursor.fetchall()
        sesion_quantity_response = []
        for row in sesion_quantity:
            sesion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        sesion_quantity_graph = len(sesion_quantity)*40+20

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
                #size graphs
                'sesion_quantity_graph':sesion_quantity_graph,
                'touch_quantity_graph':touch_quantity_graph,
                'game_time_graph':game_time_graph,
                #CLEAN OCEAN
                'colision_quantity':colision_quantity_response,
                'corrects_quantity':corrects_quantity_response,
                'incorrects_quantity':incorrects_quantity_response,
                'corrects_incorrects_quantity':corrects_incorrects_quantity_response,
                'jumps_quantity':jumps_quantity_response,
                'analytics_co_quantity':analytics_co_quantity_response,
                'exit_lab_quantity': exit_lab_quantity_response,
                'touch_animals_co_quantity':touch_animals_co_quantity_response,
                'touch_trash_co_quantity':touch_trash_co_quantity_response,
                'actividades_co_quantity':actividades_co_quantity_response,
                'colision_trash_quantity' :colision_trash_quantity_response,
                'touch_all_animals_quantity':touch_all_animals_quantity_response,
                'exits_lab_co_quantity':exits_lab_co_quantity_response,
                'touch_all_trash_quantity':touch_all_trash_quantity_response,
                'buttons_co_quantity':buttons_co_quantity_response,
                'trash_clean_co_quantity':trash_clean_co_quantity_response,
                'corrects_student_co_quantity':corrects_student_co_quantity_response,
                'time_act_co_quantity':time_act_co_quantity_response,
                #height graphs
                'colision_quantity_graph':colision_quantity_graph,
                'corrects_quantity_graph':corrects_quantity_graph,
                'corrects_incorrects_quantity_graph':corrects_incorrects_quantity_graph,
                'jumps_quantity_graph':jumps_quantity_graph,
                'analytics_co_quantity_graph':analytics_co_quantity_graph,
                'actividades_co_quantity_graph':actividades_co_quantity_graph,
                'exit_lab_quantity_graph':exit_lab_quantity_graph,
                'touch_trash_co_quantity_graph':touch_trash_co_quantity_graph,
                'corrects_student_co_quantity_graph':corrects_student_co_quantity_graph,
                'colision_trash_quantity_graph':colision_trash_quantity_graph,
                'exits_lab_co_quantity_graph':exits_lab_co_quantity_graph,
                'touch_all_trash_quantity_graph':touch_all_trash_quantity_graph,
                'buttons_co_quantity_graph':buttons_co_quantity_graph,
                'trash_clean_co_quantity_graph':trash_clean_co_quantity_graph,
                'time_act_co_quantity_graph':time_act_co_quantity_graph,
                #promedios
                'promedio_correctas_co':int(promedio_correctas_co-0.5)+1,
                'promedio_incorrectas_co':int(promedio_incorrectas_co-0.5)+1,
                'promedio_saltos':int(promedio_saltos-0.5)+1,
                'promedio_colisions':int(promedio_colisions-0.5)+1,
                #MUNDO ANIMAL
                'piezas_quantity':piezas_quantity_response,
                'malas_quantity':malas_quantity_response,
                'animales_quantity':animales_quantity_response,
                'actividades_quantity':actividades_quantity_response,
                'interaccion_quantity':interaccion_quantity_response,
                'tiempoact_quantity':tiempoact_quantity_response,
                'promedio_correctas':int(promedio_correctas),
                'promedio_incorrectas':int(promedio_incorrectas),
                'analytics1_co_quantity':analytics1_co_quantity_response,
                'tiempo_total_quantity':tiempo_total_quantity_response,
                'audios_quantity':audios_quantity_response,
                'animales_quantity_graph':animales_quantity_graph,
               
                #PLUSSPACE
                'move_element_quantity':move_element_quantity_response,
                'elementos_PS_quantity':elementos_PS_quantity_response,
                'posicionamiento_PS_quantity':posicionamiento_PS_quantity_response,
                'element_colission_quantity':element_colission_quantity_response,
                'jump_alternativas_quantity':jump_alternativas_quantity_response,
                'acierto_cuida_quantity':acierto_cuida_quantity_response,
                'completa_incompleta_PS_quantity':completa_incompleta_PS_quantity_response,
                'correctas_PS_quantity':correctas_PS_quantity_response,
                'time_PS_quantity':time_PS_quantity_response,
                #por alumno
                'jumpxalumno_quantity':jumpxalumno_quantity_response,
                'elementosXalum_PS_quantity':elementosXalum_PS_quantity_response,
                'element_colission_alum_quantity':element_colission_alum_quantity_response,
                'posicionamiento_alu_PS_quantity':posicionamiento_alu_PS_quantity_response,
                'acierto_cuida_alu_quantity':acierto_cuida_alu_quantity_response,
                #tamaño de graficos
                'time_PS_graf':time_PS_graf,
                'correctas_PS_graf':correctas_PS_graf,
                'move_element_graf':move_element_graf,
                'elementos_PS_graf':elementos_PS_graf,
                'element_colission_graf':element_colission_graf,
                'posicionamiento_PS_graf':posicionamiento_PS_graf,
                'jump_alternativas_graf':jump_alternativas_graf,
                'acierto_cuida_graf':acierto_cuida_graf,
                'completa_incompleta_PS_graf':completa_incompleta_PS_graf,
                'tiempoXact_quantity':tiempoXact_quantity_response,
                #ANALITICA PS
                'construccion':round(construccion),
                'saltos':round(saltos),
                'colisiones':round(colisiones),
                'sesiones':sesiones,
                'puzzle':round(puzzle),
                
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