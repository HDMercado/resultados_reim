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


        #INICIO DIA MUNDIAL
        #Generales
        nombre=[]
        sesiones_PS_quantity_response=[]
        time_PS_quantity_response=[]
        tiempoXact_quantity_responseDM=[]##TIEMPO  POR ACTIVIDAD
        completa_incompleta_inactividad=[]
        get_ganar_perder_DM_Quest_response=[]

        #QUERYS LAB
        completa_incompleta_DM_quantity_response=[]
        fruta_chatarra_DM_quantity_response=[]
        muro_hoyo_DM_quantity_response=[]
        col_vs_time=[]
        #QUERYS RIO OCE
        tipo_basura_DM_quantity_response=[]
        animales_nivel_DM_quantity_response=[]
        #QUERYS LUCES
        touches_luces_DM_quantity_response=[]
        #QUERYS ABEJA
        get_miel_cae_choca_DM_quantity_response=[]
        #QUERYS ANIMALES
        get_animales_salvados_DM_quantity_response=[]
        get_animales_salvados_pornivel_DM_quantity_response=[]
        #QUERYS ARBOL
        correcta_incorrecta_arbol_DM_quantity_response=[]
        crecimiento_arbol_DM_quantity_response=[]


        #TAMAÑOS
        total_completa_incompleta=0
        time_DM_graf=0



        if reim_num=="4":
            #General
            nombre_query = get_name_student(request)
            queries.append({"name": 'nombre estudiante', "query": nombre_query})
            cursor.execute(nombre_query)
            nombre_quantity = cursor.fetchall()
            for row in nombre_quantity:
                nombre.append({ 'name': row[0]})

            sesiones_PS_query = get_time_act_co(request)
            queries.append({"name": 'Tiempo Actividad sesion query', "query": sesiones_PS_query})
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
            tiempoXact_query = get_tiempoactDM(request)
            cursor.execute(tiempoXact_query)
            queries.append({"name": 'TiempoXact query', "query": tiempoXact_query})
            tiempoXact_quantity = cursor.fetchall()
            print("tiempoXact quantity", tiempoXact_quantity)
            for row in tiempoXact_quantity:
                tiempoXact_quantity_responseDM.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #QUEST DM
            completa_incompleta_PS_query = get_ganar_perder_DM_Quest(request)
            queries.append({"name": 'Correcta Incorrecta Quest DM query', "query": completa_incompleta_PS_query})
            cursor.execute(completa_incompleta_PS_query)
            completa_incompleta_PS_quantity = cursor.fetchall()
            for row in completa_incompleta_PS_quantity:
                get_ganar_perder_DM_Quest_response.append({ 'id': row[0], 'name': row[1], 'correcta': row[2], 'incorrecta': row[3]})


        ##JUEGO LABERINTO
        #Colisiones en el tiempo
            colission_analitica_query = get_colisiones_analitica_DM(request)
            queries.append({"name": 'colisiones tiempo', "query": colission_analitica_query})
            cursor.execute(colission_analitica_query)
            colission_analitica_quantity = cursor.fetchall()
            for row in colission_analitica_quantity:
                col_vs_time.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #CompletavsIncompleta
            completa_incompleta_PS_query = get_completa_incompleta_PS(request)
            queries.append({"name": 'Completas incompletas DM query', "query": completa_incompleta_PS_query})
            cursor.execute(completa_incompleta_PS_query)
            completa_incompleta_PS_quantity = cursor.fetchall()
            for row in completa_incompleta_PS_quantity:
                completa_incompleta_inactividad.append({ 'id': row[0], 'name': row[1], 'completa': row[2], 'incompleta': row[3], 'inactiva': row[4] })
            
        #Fruta vs Chatarra
            elementos_PS_query = get_ganar_perder_lab(request)
            queries.append({"name": 'Fruta Chatarra DM query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                fruta_chatarra_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'fruta': row[2], 'chatarra': row[3],})

        #Muro vs Hoyo
            muro_hoyo = get_colision_muro_hoyo(request)
            queries.append({"name": 'Muro Hoyo DM query', "query": muro_hoyo})
            cursor.execute(muro_hoyo)
            muro_hoyo_quantity = cursor.fetchall()
            for row in muro_hoyo_quantity:
                muro_hoyo_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'muro': row[2], 'hoyo': row[3]})

        ##JUEGO RIO OCEANO
        #Tipo basura
            elementos_PS_query = get_tipo_basura(request)
            queries.append({"name": 'Tipo Basura DM query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                tipo_basura_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'bolsa': row[2], 'botella': row[3], 'mancha': row[4], 'red': row[5], 'zapato': row[6],})            

        #Animal Nivel
            elementos_PS_query = get_animales_nivel(request)
            queries.append({"name": 'Animales Nivel DM query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                animales_nivel_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'animalesoceano': row[2], 'animalesrio': row[3], 'basuraoceano': row[4], 'basurario': row[5],}) 

        ##JUEGO LUCES
        #Touches Luces
            elementos_PS_query = get_touches_luces(request)
            queries.append({"name": 'Touches Luces DM query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                touches_luces_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'touches': row[2], 'lucescorrectas': row[3],})  

        ##JUEGO ABEJA
        #GET MIEL
            elementos_PS_query = get_miel_cae_choca(request)
            queries.append({"name": 'Get Miel DM query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                get_miel_cae_choca_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'colisionpanal': row[2], 'colisionsuelo': row[3], 'colisionosoavispa': row[4],})

        ##JUEGO ANIMALES
        #ANIMALES SALVADOS
            elementos_PS_query = get_animales_salvados(request)
            queries.append({"name": 'Animales Salvados DM query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                get_animales_salvados_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'ballena': row[2], 'oso': row[3], 'pinguino': row[4], 'pepino': row[5], 'pajaro': row[6], 'foca': row[7], 'tigre': row[8], 'cocodrilo': row[9], 'mono': row[10], 'serpiente': row[11], 'perezoso': row[12], 'rana': row[13], 'lagartija': row[14], 'lemur': row[15], 'camaleon': row[16], 'tortuga': row[17], 'leon': row[18], 'fosa': row[19]})

        #ANIMALES SALVADOS POR NIVEL
            elementos_PS_query = get_animales_salvados_pornivel(request)
            queries.append({"name": 'Animales Salvados Por Nivel DM query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                get_animales_salvados_pornivel_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'animalesantartica': row[2], 'animalesselva': row[3], 'animalesmadagascar': row[4],})

        ##JUEGO ARBOL
        #Correcta Incorrecta
            elementos_PS_query = get_correcta_incorrecta_arbol(request)
            queries.append({"name": 'Correcta Incorrecta Arbol DM query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                correcta_incorrecta_arbol_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'perdida': row[2], 'atino': row[3],})

        #Crecimiento Arbol
            colission_analitica_query = get_crecimiento_arbol(request)
            queries.append({"name": 'Crecer Árbol en el tiempo', "query": colission_analitica_query})
            cursor.execute(colission_analitica_query)
            colission_analitica_quantity = cursor.fetchall()
            for row in colission_analitica_quantity:
                crecimiento_arbol_DM_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })











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
        sesiones_PS_quantity_response=[]
        #analitica PS
        elementos_analitica_PS_quantity_response=[]
        colission_analitica_quantity_response=[]
        touch_puzzle_quantity_response=[]
        nombre=[]

 
        if reim_num=="2":       

        #General
            nombre_query = get_name_student(request)
            queries.append({"name": 'nombre estudiante', "query": nombre_query})
            cursor.execute(nombre_query)
            nombre_quantity = cursor.fetchall()
            for row in nombre_quantity:
                nombre.append({ 'name': row[0]})

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
                move_element_quantity_response.append({ 'id': row[0], 'fila': row[1], 'columna':row[2]})
                print(row[1])
                print(row[2])
        #ELEMENTOS creacion
            elementos_PS_query = get_elementos_PS(request)
            queries.append({"name": 'planet creacion query', "query": elementos_PS_query})
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                elementos_PS_quantity_response.append({ 'id': row[0], 'name': row[1], 'planeta': row[2], 'planetaCS': row[3], 'planetaCA': row[4], 'estrella': row[5], 'supernova': row[6], 'nebulosa': row[7], 'galaxia': row[8] })
        #ELEMENTOS creacion analitica
            elementos_analitica_PS_query = get_elementos_alu_PS(request)
            queries.append({"name": 'creacion analitica query', "query": elementos_analitica_PS_query})
            cursor.execute(elementos_analitica_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                elementos_analitica_PS_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
       
        #LABERINTO
        #posicionamiento
            posicionamiento_PS_query = get_posicionamiento_PS(request)
            queries.append({"name": 'posicionamiento_PS query', "query": posicionamiento_PS_query})
            cursor.execute(posicionamiento_PS_query)
            posicionamiento_PS_quantity = cursor.fetchall()
            for row in posicionamiento_PS_quantity:
                posicionamiento_PS_quantity_response.append({ 'id': row[0], 'name': row[1], 'tierra': row[2], 'neptuno': row[3], 'jupiter': row[4], 'saturno': row[5], 'urano': row[6], 'venus': row[7], 'mercurio': row[8], 'marte': row[9] })

        #colisiones
            element_colission_query = get_element_colission_query(request)
            queries.append({"name": 'colisiones query', "query": element_colission_query})
            cursor.execute(element_colission_query)
            element_colission_quantity = cursor.fetchall()
            for row in element_colission_quantity:
                element_colission_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        #colisiones analitica
            colission_analitica_query = get_colisiones_analitica_PS(request)
            queries.append({"name": 'colisiones analitica query', "query": colission_analitica_query})
            cursor.execute(colission_analitica_query)
            colission_analitica_quantity = cursor.fetchall()
            for row in colission_analitica_quantity:
                colission_analitica_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
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
            for row in jumpxalumno_quantity:
                jumpxalumno_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
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
        #puzzle
            touch_puzzle_query = get_touch_analitica_query(request)
            queries.append({"name": 'touch puzzle query', "query": touch_puzzle_query})
            cursor.execute(touch_puzzle_query)
            touch_puzzle_quantity = cursor.fetchall()
            for row in touch_puzzle_quantity:
                touch_puzzle_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })           
        #otros
        time_PS_graf = len(time_PS_quantity_response) * 40+20
        correctas_PS_graf = len(correctas_PS_quantity_response) * 40+100
        elementos_PS_graf = len(elementos_PS_quantity_response) * 40+100
        element_colission_graf = len(element_colission_quantity_response) * 40+20
        posicionamiento_PS_graf = len(posicionamiento_PS_quantity_response) * 40+100
        jump_alternativas_graf = len(jump_alternativas_quantity_response) * 40+20
        acierto_cuida_graf = len(acierto_cuida_quantity_response) * 40+20
        completa_incompleta_PS_graf = len(completa_incompleta_PS_quantity_response) * 40+100
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

#INICIO REIM ID = 77, NOMBRE = BUSCANDO EL TESORO PERDIDO
        #-------
        nombre_estilo_cognitivo_alumno = ''
        tiempo_x_actividad_response = []
        identificar_estilo_cognitivo_response = []
        Estilo_cognitivo_por_niño = []
        buenas_malas_x_figura_compleja = []
        #-----------------------------------------
        actividad_1_volcan = []
        tiempoxactxsesion = []
        lista_estudiante = []
        lista_alumno_cognitivo = []
        lista_alumno_cognitivo_muy_dependiente = []
        lista_alumno_cognitivo_dependiente = []
        lista_alumno_cognitivo_intermedio = []
        lista_alumno_cognitivo_independiente = []
        lista_alumno_cognitivo_muy_independiente = []
        #-----------------------------------------
        nombre_activada_1 = ''
        activdad_1_completada = 0
        activdad_1_no_completada = 0
        nombre_activada_2 = ''
        activdad_2_completada = 0
        activdad_2_no_completada = 0
        nombre_activada_3 = ''
        activdad_3_completada = 0
        activdad_3_no_completada = 0
        nombre_activada_4 = ''
        activdad_4_completada = 0
        activdad_4_no_completada = 0
        nombre_activada_5 = ''
        activdad_5_completada = 0
        activdad_5_no_completada = 0
        nombre_activada_6 = ''
        activdad_6_completada = 0
        activdad_6_no_completada = 0
        #-----------------------------------
        color_base = ''
        lista_estudiante = []
        #print("\n\n\n lista: ", lista_estudiante[4])

        if reim_num=="77":
            #-------------------------por curso---------------------------  11
            tipo_grafico = 0
            contador_complejo_1 = 0
            contador_complejo_2 = 0
            contador_complejo_3 = 0
            contador_complejo_4 = 0
            contador_complejo_5 = 0
            contador_complejo_6 = 0
            contador_complejo_7 = 0
            contador_complejo_8 = 0
            contador_complejo_9 = 0
            contador_complejo_10 = 0
            completada_total = 0
            total_incompletas = 0
            nombre_actividad = ''
            contador_tiempo = 0
            Total_Completas_Actividad = 0
            rango_tiempo = datetime.now() 
            fecha_inicial = datetime.now()
            nombre_alumno = '' 
#POR CURSOR
            if request.GET.get('student') == '0':
                #print("\n\n grafico general")
                lista_estudiante = students_response
                for alumno in lista_estudiante:
                    try:
                        tipo_grafico = int(request.GET.get('option'))
                    except:
                        tipo_grafico = 1
                    #print("Grafico:", tipo_grafico)
                    

                    lista_actividad = [[7705, 50], [7706, 50], [7707,50], [7708, 65], [7709, 70], [7710, 80]]
                    for actividad_77 in lista_actividad:
                        
                        contador_complejo_1 = 0
                        contador_complejo_2 = 0
                        contador_complejo_3 = 0
                        contador_complejo_4 = 0
                        contador_complejo_5 = 0
                        contador_complejo_6 = 0
                        contador_complejo_7 = 0
                        contador_complejo_8 = 0
                        contador_complejo_9 = 0
                        contador_complejo_10 = 0
                        completada_total = 0
                        total_incompletas = 0
                        nombre_actividad = ''
                        contador_tiempo = 0
                        queryXactividad = ''

                        if(tipo_grafico == 1 ):
                            print('\n\nAlumno', alumno["id"], ' nombre: ', alumno["name"])
                            queryXactividad = get_figura_simple_estandar_por_curso(request, actividad_77, alumno["id"])
                            #print("ESTANDAR")
                        if(tipo_grafico == 2 ):
                            queryXactividad = get_figura_simple_promedio_por_curso(request, actividad_77, alumno["id"])
                            #print("PROMEDIO")
                        if(tipo_grafico == 3 ):
                            queryXactividad = get_figura_simple_ultimos_registros_por_curso(request, actividad_77, alumno["id"])
                            #print("FINAL")
                        cursor.execute(queryXactividad)
                        queries.append({"name": 'TiempoXact query', "query": queryXactividad})
                        resultado_query = cursor.fetchall()
                        for row in resultado_query:

                                if(len(row[5]) > 0):
                                    nombre_alumno = row[5]
                                    #print("nombre: " + nombre_alumno)
                                nombre_actividad = row[4]
                                if(contador_tiempo == 0):
                                    contador_tiempo+=1
                                    rango_tiempo = row[2]
                                    fecha_inicial = rango_tiempo + timedelta(seconds = actividad_77[1])
                                    try:
                                        if(int(request.GET.get('rango')) != 0):
                                            valor = actividad_77[1] + ((actividad_77[1] * int(request.GET.get('rango')))/100)
                                            #print("VALOR: ", valor)
                                            fecha_inicial = rango_tiempo + timedelta(seconds = valor)
                                    except:
                                            valor = actividad_77[1] + ((actividad_77[1] * int("50"))/100)
                                            #print("VALOR: ", valor)
                                            fecha_inicial = rango_tiempo + timedelta(seconds = valor)
                                #print("\n\n\n\nFECHA INICIAL: ",fecha_inicial, " Nombre: ", actividad_77[0], " Segundos: ", actividad_77[1])
                                #print("Contador 1: ", contador_complejo_1)
                                #print(row[1]," == 7728 and ", contador_complejo_1, " == 0 and correcta ", row[3], " == 1 and ", row[2], " <= " , fecha_inicial )
                                if(row[1] == 7728 and contador_complejo_1 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    #print("Entro actividad 7728 7705")
                                    contador_complejo_1+=1
                                    completada_total+=1
                                if(row[1] == 7729 and contador_complejo_2 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    #print("Entro actividad 7729 7705")
                                    completada_total+=1
                                    contador_complejo_2+=1
                                if(row[1] == 7730 and contador_complejo_3 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    completada_total+=1
                                    contador_complejo_3+=1
                                if(row[1] == 7731 and contador_complejo_4 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    completada_total+=1
                                    contador_complejo_4+=1
                                if(row[1] == 7732 and contador_complejo_5 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    completada_total+=1
                                    contador_complejo_5+=1
                                if(row[1] == 7733 and contador_complejo_6 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    completada_total+=1
                                    contador_complejo_6+=1
                                if(row[1] == 7734 and contador_complejo_7 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    completada_total+=1
                                    contador_complejo_7+=1
                                if(row[1] == 7735 and contador_complejo_8 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    completada_total+=1
                                    contador_complejo_8+=1
                                if(row[1] == 7736 and contador_complejo_9 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    completada_total+=1
                                    contador_complejo_9+=1
                                if(row[1] == 7737 and contador_complejo_10 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                    completada_total+=1
                                    contador_complejo_10+=1      
                        if(int(completada_total) < 10 and len(nombre_actividad) != 0):               
                            total_incompletas = (10 - completada_total)
                            actividad_1_volcan.append({'name': nombre_actividad, 'completada': completada_total, 'no_completada': total_incompletas})
                        
                        Total_Completas_Actividad +=completada_total

                    Nombre_Estilo_Cognitivo = ''
                    if(Total_Completas_Actividad > 0 and Total_Completas_Actividad < 11):
                        Nombre_Estilo_Cognitivo = 'Muy Dependiente del Campo'
                        color_base = '(119,170,255)'
                        lista_alumno_cognitivo_muy_dependiente.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'cantidad': Total_Completas_Actividad})
                    if(Total_Completas_Actividad > 10 and Total_Completas_Actividad < 21):
                        Nombre_Estilo_Cognitivo = 'Dependiente del Campo'
                        color_base = '(153,204,255)'
                        lista_alumno_cognitivo_dependiente.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'cantidad': Total_Completas_Actividad})
                    if(Total_Completas_Actividad > 20 and Total_Completas_Actividad < 31):
                        Nombre_Estilo_Cognitivo = 'Intermedio del Campo'
                        color_base = '(187,238,255)'
                        lista_alumno_cognitivo_intermedio.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'cantidad': Total_Completas_Actividad})
                    if(Total_Completas_Actividad > 30 and Total_Completas_Actividad < 41):
                        Nombre_Estilo_Cognitivo = 'Independiente del Campo'
                        color_base = 'rgb(85,136,255)'
                        lista_alumno_cognitivo_independiente.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'cantidad': Total_Completas_Actividad})
                    if(Total_Completas_Actividad > 40 and Total_Completas_Actividad < 51):
                        Nombre_Estilo_Cognitivo = 'Muy Dependiente del Campo'
                        color_base = '(51,102,255)'
                        lista_alumno_cognitivo_muy_independiente.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'cantidad': Total_Completas_Actividad})    
                    #print("Nombre: ", nombre_alumno)
                    
                    if(len(nombre_alumno) > 0):
                        lista_alumno_cognitivo.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'cantidad': Total_Completas_Actividad, 'color': color_base})

                    nombre_alumno = ''
                    Nombre_Estilo_Cognitivo = ''
                    Total_Completas_Actividad = 0
                    completada_total = 0
                    #print('\n\nAlumno', nombre_alumno,' Nomnre', Nombre_Estilo_Cognitivo, 'Cantidad: ', Total_Completas_Actividad )
                    #
            
            #----------------------por CURSO----------------------------- 22
            
        #---------------------------------por alumno---------------------------------------------------
            if request.GET.get('student') and request.GET.get('student') != '0':
                print("\n\n\nPASOS")
                lista_actividad = [[7705, 50], [7706, 50], [7707,50], [7708, 65], [7709, 70], [7710, 80]]
                for actividad_77 in lista_actividad:
                    tipo_grafico = int(request.GET.get('option'))
                    print("Grafico:", tipo_grafico)
                    contador_complejo_1 = 0
                    contador_complejo_2 = 0
                    contador_complejo_3 = 0
                    contador_complejo_4 = 0
                    contador_complejo_5 = 0
                    contador_complejo_6 = 0
                    contador_complejo_7 = 0
                    contador_complejo_8 = 0
                    contador_complejo_9 = 0
                    contador_complejo_10 = 0
                    completada_total = 0
                    total_incompletas = 0
                    nombre_actividad = ''
                    contador_tiempo = 0
                    queryXactividad = ''

                    if(tipo_grafico == 1 ):
                        queryXactividad = get_figura_simple_volcan(request, actividad_77)
                        print("ESTANDAR")
                    if(tipo_grafico == 2 ):
                        queryXactividad = get_figura_simple_promedio(request, actividad_77)
                        print("PROMEDIO")
                    if(tipo_grafico == 3 ):
                        queryXactividad = get_figura_simple_ultimos_registros(request, actividad_77)
                        print("FINAL")
                    cursor.execute(queryXactividad)
                    queries.append({"name": 'TiempoXact query', "query": queryXactividad})
                    resultado_query = cursor.fetchall()
                    for row in resultado_query:

                            if(len(row[5]) > 0):
                                nombre_alumno = row[5]
                            nombre_actividad = row[4]
                            if(contador_tiempo == 0):
                                contador_tiempo+=1
                                rango_tiempo = row[2]
                                fecha_inicial = rango_tiempo + timedelta(seconds = actividad_77[1])
                                if(int(request.GET.get('rango')) != 0):
                                    valor = actividad_77[1] + ((actividad_77[1] * int(request.GET.get('rango')))/100)
                                    #print("VALOR: ", valor)
                                    fecha_inicial = rango_tiempo + timedelta(seconds = valor)
                            print("\n\n\n\nFECHA INICIAL: ",fecha_inicial, " Nombre: ", actividad_77[0], " Segundos: ", actividad_77[1])
                            #print("Contador 1: ", contador_complejo_1)
                            #print(row[1]," == 7728 and ", contador_complejo_1, " == 0 and correcta ", row[3], " == 1 and ", row[2], " <= " , fecha_inicial )
                            if(row[1] == 7728 and contador_complejo_1 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                print("Entro actividad 7728 7705")
                                contador_complejo_1+=1
                                completada_total+=1
                            if(row[1] == 7729 and contador_complejo_2 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                print("Entro actividad 7729 7705")
                                completada_total+=1
                                contador_complejo_2+=1
                            if(row[1] == 7730 and contador_complejo_3 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                completada_total+=1
                                contador_complejo_3+=1
                            if(row[1] == 7731 and contador_complejo_4 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                completada_total+=1
                                contador_complejo_4+=1
                            if(row[1] == 7732 and contador_complejo_5 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                completada_total+=1
                                contador_complejo_5+=1
                            if(row[1] == 7733 and contador_complejo_6 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                completada_total+=1
                                contador_complejo_6+=1
                            if(row[1] == 7734 and contador_complejo_7 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                completada_total+=1
                                contador_complejo_7+=1
                            if(row[1] == 7735 and contador_complejo_8 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                completada_total+=1
                                contador_complejo_8+=1
                            if(row[1] == 7736 and contador_complejo_9 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                completada_total+=1
                                contador_complejo_9+=1
                            if(row[1] == 7737 and contador_complejo_10 == 0 and row[3] == 1 and row[2] <= fecha_inicial):
                                completada_total+=1
                                contador_complejo_10+=1      
                    if(int(completada_total) < 10 and len(nombre_actividad) != 0):               
                        total_incompletas = (10 - completada_total)
                        actividad_1_volcan.append({'name': nombre_actividad, 'completada': completada_total, 'no_completada': total_incompletas})
                    
                    Total_Completas_Actividad +=completada_total

                Nombre_Estilo_Cognitivo = ''
                if(Total_Completas_Actividad > 0 and Total_Completas_Actividad < 11):
                    Nombre_Estilo_Cognitivo = 'Muy Dependiente'
                    nombre_estilo_cognitivo_alumno = 'Muy Dependiente del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })
                if(Total_Completas_Actividad > 10 and Total_Completas_Actividad < 21):
                    Nombre_Estilo_Cognitivo = 'Dependiente'
                    nombre_estilo_cognitivo_alumno = 'Dependiente del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })
                if(Total_Completas_Actividad > 20 and Total_Completas_Actividad < 31):
                    Nombre_Estilo_Cognitivo = 'Intermedio'
                    nombre_estilo_cognitivo_alumno = 'Intermedio del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })
                if(Total_Completas_Actividad > 30 and Total_Completas_Actividad < 41):
                    Nombre_Estilo_Cognitivo = 'Independiente'
                    nombre_estilo_cognitivo_alumno = 'Independiente del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })
                if(Total_Completas_Actividad > 40 and Total_Completas_Actividad < 51):
                    Nombre_Estilo_Cognitivo = 'Muy Dependiente'
                    nombre_estilo_cognitivo_alumno = 'Muy Independiente del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })

                Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })

            

            #----------------------por alumno----------------------------- 22
            if request.GET.get('student') and request.GET.get('student') != '0':
                buenas_malas = get_Actividad_Buenas_Mala(request)
                cursor.execute(buenas_malas)
                queries.append({"name": 'TiempoXact query', "query": buenas_malas})
                tiempoXact_quantity = cursor.fetchall()
                for row in tiempoXact_quantity:
                    nombre_actividad = row[7]
                    nombre_actividad = nombre_actividad.replace("Btn-Aceptar-Figura-","Figura Compleja ")
                    buenas_malas_x_figura_compleja.append({  'name': nombre_actividad, 'completa': row[4], 'no_completa': row[5] })



            #--------------------------------------------------- 33
            if request.GET.get('student') and request.GET.get('student') != '0':
                tiem_acti_sesion = get_tiempoact_sesion(request)
                cursor.execute(tiem_acti_sesion)
                queries.append({"name": 'TiempoXact query', "query": tiem_acti_sesion})
                tiempoXact_quantity = cursor.fetchall()
                for row in tiempoXact_quantity:
                    tiempoxactxsesion.append({  'name': row[1], 'quantity': row[2] })
            
            
            #--------------------------------------------------- 33
            #Estilo_cognitivo_por_niño.append({'name': Nombre_Estilo_Cognitivo, 'quantity': Valor_Total_Figuras_complejas })


        #TAMAÑO GRAFICOS
        time_ps_query_77= len(tiempo_x_actividad_response) * 40+20
        identificar_estilo_cognitivo = len(identificar_estilo_cognitivo_response) * 40+20
        tamaño_curso = len(lista_alumno_cognitivo) * 40+20
        tamaña_grafico_por_alumno = len(actividad_1_volcan) * 40 + 20
        tamaña_grafico_por_actividad = len(buenas_malas_x_figura_compleja) * 40 + 20
        
        print("Tamaño: ", tamaño_curso)
        for item in lista_alumno_cognitivo:
                print("Nombre: ", item["alumno"], "item: ", item["cantidad"], "Estilo del campo: ", item["name"])



#FIN REIM ID = 77, NOMBRE = BUSCANDO EL TESORO PERDIDO
        
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
                #Día Mundial
                'time_DM_quantity':time_PS_quantity_response,
                'completa_incompleta_DM_quantity':completa_incompleta_DM_quantity_response,
                'fruta_chatarra_DM_quantity_response':fruta_chatarra_DM_quantity_response,
                'muro_hoyo_DM_quantity_response':muro_hoyo_DM_quantity_response,
                'tipo_basura_DM_quantity_response': tipo_basura_DM_quantity_response,
                'animales_nivel_DM_quantity_response':animales_nivel_DM_quantity_response,
                'touches_luces_DM_quantity_response': touches_luces_DM_quantity_response,
                'get_miel_cae_choca_DM_quantity_response':get_miel_cae_choca_DM_quantity_response,
                'get_animales_salvados_DM_quantity_response':get_animales_salvados_DM_quantity_response,
                'get_animales_salvados_pornivel_DM_quantity_response':get_animales_salvados_pornivel_DM_quantity_response,
                'correcta_incorrecta_arbol_DM_quantity_response':correcta_incorrecta_arbol_DM_quantity_response,
                'crecimiento_arbol_DM_quantity_response':crecimiento_arbol_DM_quantity_response,
                'completa_incompleta_inactividad':completa_incompleta_inactividad,
                'col_vs_time':col_vs_time,
                'tiempoXact_quantity_responseDM': tiempoXact_quantity_responseDM,
                'get_ganar_perder_DM_Quest_response': get_ganar_perder_DM_Quest_response,
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
                #analitica
                'elementos_analitica_PS_quantity':elementos_analitica_PS_quantity_response,
                'colission_analitica_quantity':colission_analitica_quantity_response,
                'touch_puzzle_quantity':touch_puzzle_quantity_response,
                'nombre':nombre,
                #INICIO REIM ID = 77, NOMBRE = BUSCANDO EL TESORO PERDIDO
                'tiempo_x_actividad': tiempo_x_actividad_response,
                'respuesta_x_estilo': identificar_estilo_cognitivo_response,
                'estilo_x_cognitivo': Estilo_cognitivo_por_niño,
                'actividad_1_volcan_response': actividad_1_volcan,
                'figura_compleja_x_actividad': buenas_malas_x_figura_compleja,
                'tiempo_acti_sesion':  tiempoxactxsesion,
                'grafico_curso_77': lista_alumno_cognitivo,
                'grafico_muy_dependiente': lista_alumno_cognitivo_muy_dependiente,
                'grafico_dependiente': lista_alumno_cognitivo_dependiente,
                'grafico_intermedio': lista_alumno_cognitivo_intermedio,
                'grafico_independiente': lista_alumno_cognitivo_independiente,
                'grafico_muy_independiente': lista_alumno_cognitivo_muy_independiente,
                'Reconocimiento_Alumno': nombre_estilo_cognitivo_alumno,
                #Tamaño Grafico
                'time_PS_graf_1': time_ps_query_77,
                'estilo_cognitivo': identificar_estilo_cognitivo,
                'tamaño_curso': tamaño_curso,
                'tamaña_grafico_por_alumno': tamaña_grafico_por_alumno,
                'tamaño_actividad_alumno': tamaña_grafico_por_actividad
                #FIN REIM ID = 77, NOMBRE = BUSCANDO EL TESORO PERDIDO
                
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