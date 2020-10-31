from .utils import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import User
# ----- 77
from datetime import timedelta
# ----- 77


def order_list_alm(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(json['porcent'])
    except KeyError:
        return 0


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
            course_filter = ' AND pertenece.curso_id=' + request.GET.get(
                'course')

        cursor.execute(
            'SELECT colegio.id, colegio.nombre FROM pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id INNER JOIN colegio ON pertenece.colegio_id = colegio.id WHERE usuario.username="'
            + request.user.username + '" GROUP BY colegio.id')
        schools = cursor.fetchall()
        schools_response = []
        for row in schools:
            schools_response.append({'id': row[0], 'name': row[1]})

        #Reim selector
        course_filter = ''
        #if request.GET.get('course') and request.GET.get('activity') != "0":
        #    course_filter = request.GET.get('course')
        activate_course_filter = False
        if request.GET.get('course') and request.GET.get('course') != "0":
            activate_course_filter = True
            course_filter = 'where curso_id =' + request.GET.get('course')

        #cursor.execute('SELECT DISTINCT reim.id, reim.nombre from actividad inner join reim on id_reim = reim.id inner join asigna_reim on reim_id = reim_id inner join pertenece on asigna_reim.colegio_id = pertenece.colegio_id  inner join colegio on asigna_reim.colegio_id = colegio.id inner join curso on asigna_reim.curso_id = curso.id  inner join usuario on pertenece.usuario_id = usuario.id where usuario.username ="' + request.user.username + '"' + course_filter +' GROUP BY reim.id')
        cursor.execute(
            'SELECT DISTINCT reim.id, reim.nombre from asigna_reim inner join reim on reim_id = reim.id '
            + course_filter + ' GROUP BY reim.id')
        reims = cursor.fetchall()
        reims_response = []
        for row in reims:
            reims_response.append({'id': row[0], 'name': row[1]})

        #Course selector
        school_filter = ''
        activate_school_filter = False
        if request.GET.get('school') and request.GET.get('school') != "0":
            activate_school_filter = True
            school_filter = ' AND pertenece.colegio_id=' + request.GET.get(
                'school')

        cursor.execute(
            'SELECT curso.id, concat(nivel.nombre, " ",curso.nombre) as Nivelcurso FROM pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id INNER JOIN curso ON pertenece.curso_id = curso.id INNER JOIN nivel ON pertenece.nivel_id = nivel.id WHERE usuario.username ="'
            + request.user.username + '"' + school_filter +
            ' GROUP BY curso.id')
        courses = cursor.fetchall()
        courses_response = []
        for row in courses:
            courses_response.append({'id': row[0], 'name': row[1]})

        #Activity selector
        reim_filter = ''
        activate_reim_filter = False
        if request.GET.get('reim') and request.GET.get('reim') != "0":
            activate_reim_filter = True
            reim_filter = ' AND actividad.id_reim=' + request.GET.get('reim')

        cursor.execute(
            'SELECT DISTINCT actividad.id, actividad.nombre from asigna_reim inner join actividad on reim_id = reim_id inner join pertenece on asigna_reim.colegio_id = pertenece.colegio_id  inner join colegio on asigna_reim.colegio_id = colegio.id inner join curso on asigna_reim.curso_id = curso.id  inner join usuario on pertenece.usuario_id = usuario.id where usuario.username ="'
            + request.user.username + '"' + reim_filter +
            ' GROUP BY actividad.id')
        activities = cursor.fetchall()
        activities_response = []
        for row in activities:
            activities_response.append({'id': row[0], 'name': row[1]})

        #Game time
        time_query = get_time_query(request)
        #print(time_query)
        queries.append({"name": 'Time query', "query": time_query})
        cursor.execute(time_query)
        game_time = cursor.fetchall()
        game_time_response = []
        for row in game_time:
            game_time_response.append({
                'id': row[0],
                'name': row[1],
                'time': row[2]
            })
        game_time_graph = len(game_time) * 40 + 20

        #Touch
        touch_query = get_touch_query(request)
        queries.append({"name": 'Touch query', "query": touch_query})
        cursor.execute(touch_query)
        touch_quantity = cursor.fetchall()
        touch_quantity_response = []
        for row in touch_quantity:
            touch_quantity_response.append({
                'id': row[0],
                'name': row[1],
                'quantity': row[2]
            })
        touch_quantity_graph = len(touch_quantity) * 40 + 20

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
                cursor.execute(
                    'SELECT DISTINCT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="'
                    + request.user.username + '")' +
                    'AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username ="'
                    + request.user.username + '"))' + 'AND a.id_reim="' +
                    request.GET.get('reim') + '"' + 'AND b.curso_id ="' +
                    request.GET.get('course') + '"' + 'AND b.colegio_id ="' +
                    request.GET.get('school') + '";')
                students = cursor.fetchall()
                for row in students:
                    students_response.append({'id': row[0], 'name': row[1]})

#####BEGIN BUILD YOUR CITY#####
#DEFINITIONS:
##DICTIONARYS:
        ByC_numberOfSessions_Dictionary = []
        ByC_playTime_Dictionary = []
        ByC_touchCount_Dictionary = []
        ByC_activitiesPlayedCounter_Dictionary = []
        ByC_built_elementsCounter_Dictionary = []
        ByC_built_elementsCounter_perCategory_Dictionary = []
        ByC_maxNumberOfAssistants_Dictionary = []
        ByC_Cinema_CompleteVsIncomplete_Dictionary = []
        ByC_Cinema_SuccessVsFailure_Dictionary = []
        ByC_Cinema_SuccessVsFailure_ParticularSeats_Dictionary = []
        ByC_Cinema_NumberOfEntrances_Dictionary = []
        ByC_Cinema_SuccessPercentageInTime_Dictionary = []
        ByC_Cinema_Count_Attempts = 0
        ByC_Cinema_Count_Success = 0
        ByC_Cinema_Count_Failure = 0
        ByC_Cinema_Average_Success = 0
        ByC_Cinema_Average_Failure = 0
        ByC_Cinema_Count_ParticularAttempts = 0
        ByC_Cinema_Count_ParticularSuccess = 0
        ByC_Cinema_Count_ParticularFailure = 0
        ByC_Cinema_Average_ParticularSuccess = 0
        ByC_Cinema_Average_ParticularFailure = 0
        ByC_Cinema_TotalAttempts = 0
        ByC_School_CompleteVsIncomplete_Dictionary = []
        ByC_School_SuccessVsFailure_Dictionary = []
        ByC_School_SuccessVsFailure_ParticularSeats_Dictionary = []
        ByC_School_NumberOfEntrances_Dictionary = []
        ByC_School_SuccessPercentageInTime_Dictionary = []
        ByC_School_Count_Attempts = 0
        ByC_School_Count_Success = 0
        ByC_School_Count_Failure = 0
        ByC_School_Average_Success = 0
        ByC_School_Average_Failure = 0
        ByC_School_Count_ParticularAttempts = 0
        ByC_School_Count_ParticularSuccess = 0
        ByC_School_Count_ParticularFailure = 0
        ByC_School_Average_ParticularSuccess = 0
        ByC_School_Average_ParticularFailure = 0
        ByC_School_TotalAttempts = 0
        ByC_Taxi_CompleteVsIncomplete_Dictionary = []
        ByC_Taxi_SuccessVsFailure_Dictionary = []
        ByC_Taxi_SuccessVsFailure_ParticularSeats_Dictionary = []
        ByC_Taxi_NumberOfEntrances_Dictionary = []
        ByC_Taxi_SuccessPercentageInTime_Dictionary = []
        ByC_Taxi_Count_Attempts = 0
        ByC_Taxi_Count_Success = 0
        ByC_Taxi_Count_Failure = 0
        ByC_Taxi_Average_Success = 0
        ByC_Taxi_Average_Failure = 0
        ByC_Taxi_Count_ParticularAttempts = 0
        ByC_Taxi_Count_ParticularSuccess = 0
        ByC_Taxi_Count_ParticularFailure = 0
        ByC_Taxi_Average_ParticularSuccess = 0
        ByC_Taxi_Average_ParticularFailure = 0
        ByC_Taxi_TotalAttempts = 0

        ##GRAPHS SIZE:
        ByC_numberOfSessions_GraphSize = 0
        ByC_playTime_GraphSize = 0
        ByC_touchCount_GraphSize = 0
        ByC_activitiesPlayedCounter_GraphSize = 0
        ByC_built_elementsCounter_GraphSize = 0
        ByC_built_elementsCounter_perCategory_GraphSize = 0
        ByC_maxNumberOfAssistants_GraphSize = 0
        ByC_Cinema_CompleteVsIncomplete_GraphSize = 0
        ByC_Cinema_SuccessVsFailure_GraphSize = 0
        ByC_Cinema_SuccessVsFailure_ParticularSeats_GraphSize = 0
        ByC_Cinema_NumberOfEntrances_GraphSize = 0
        ByC_School_CompleteVsIncomplete_GraphSize = 0
        ByC_School_SuccessVsFailure_GraphSize = 0
        ByC_School_SuccessVsFailure_ParticularSeats_GraphSize = 0
        ByC_School_NumberOfEntrances_GraphSize = 0
        ByC_Taxi_CompleteVsIncomplete_GraphSize = 0
        ByC_Taxi_SuccessVsFailure_GraphSize = 0
        ByC_Taxi_SuccessVsFailure_ParticularSeats_GraphSize = 0
        ByC_Taxi_NumberOfEntrances_GraphSize = 0

        if reim_num == "27":

            ##GET NUMBER OF SESSIONS##
            getNumberOfSessions_query = get_number_of_sessions(request)
            cursor.execute(getNumberOfSessions_query)
            queries.append({
                "name": 'Get Number Of Sessions',
                "query": getNumberOfSessions_query
            })
            numberOfSessions_QueryResponse = cursor.fetchall()
            #print ("analytics1_co_quantity", analytics1_co_quantity)
            for row in numberOfSessions_QueryResponse:
                ByC_numberOfSessions_Dictionary.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
            ByC_numberOfSessions_GraphSize = len(
                numberOfSessions_QueryResponse) * 40 + 20

            ##PLAYTIME REIM##
            getPlayTime = get_playtime(request)
            cursor.execute(getPlayTime)
            queries.append({
                "name": 'Get PlayTime of REIM',
                "query": getPlayTime
            })
            playTime_QueryResponse = cursor.fetchall()
            print("playTime_QueryResponse", playTime_QueryResponse)
            for row in playTime_QueryResponse:
                ByC_playTime_Dictionary.append({
                    'id': row[0],
                    'name': row[1],
                    'playTime': row[2]
                })
            ByC_playTime_GraphSize = len(playTime_QueryResponse) * 40 + 20

            ##TOUCH COUNT REIM##
            touch_query = get_touch_count(request)
            queries.append({"name": 'Get Touch Count', "query": touch_query})
            cursor.execute(touch_query)
            touchCount_QueryResponse = cursor.fetchall()
            for row in touchCount_QueryResponse:
                ByC_touchCount_Dictionary.append({
                    'id': row[0],
                    'name': row[1],
                    'touchCount': row[2]
                })
            ByC_touchCount_GraphSize = len(touchCount_QueryResponse) * 40 + 20

            ##ACTIVITIES PLAYED COUNTER##
            touch_query = get_activities_played_counter(request)
            queries.append({
                "name": 'Activities Played Counter',
                "query": touch_query
            })
            cursor.execute(touch_query)
            activitiesPlayedCounter_QueryResponse = cursor.fetchall()
            for row in activitiesPlayedCounter_QueryResponse:
                name = ''
                if row[0] == 27101:
                    name = 'Actividad 2: Cine'
                elif row[0] == 27102:
                    name = 'Actividad 3: Escuela'
                elif row[0] == 27103:
                    name = 'Actividad 4: Taxi'
                ByC_activitiesPlayedCounter_Dictionary.append({
                    'id': row[0],
                    'name': name,
                    'counter': row[1]
                })
            ByC_activitiesPlayedCounter_GraphSize = len(
                activitiesPlayedCounter_QueryResponse) * 40 + 20

            ##BUILT ELEMENTS COUNTER PER CATEGORY##
            built_elements_counter_percategory_query = get_built_elements_counter_per_category(
                request)
            queries.append({
                "name": 'BUILT ELEMENTS COUNTER PER CATEGORY',
                "query": built_elements_counter_percategory_query
            })
            cursor.execute(built_elements_counter_percategory_query)
            built_elementsCounter_percategory_QueryResponse = cursor.fetchall()
            for row in built_elementsCounter_percategory_QueryResponse:
                ByC_built_elementsCounter_perCategory_Dictionary.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'buildingsCount':
                    row[2],
                    'ornamentsCount':
                    row[3],
                    'carsCount':
                    row[4]
                })
            ByC_built_elementsCounter_perCategory_GraphSize = len(
                built_elementsCounter_percategory_QueryResponse) * 40 + 100

            ##BUILT ELEMENTS COUNTER ##
            built_elements_counter_query = get_built_elements_counter(request)
            queries.append({
                "name": 'BUILT ELEMENTS COUNTER',
                "query": built_elements_counter_query
            })
            cursor.execute(built_elements_counter_query)
            built_elementsCounter_QueryResponse = cursor.fetchall()
            for row in built_elementsCounter_QueryResponse:
                name = ''
                if row[0] == 27104:
                    name = 'Casa Azul'
                elif row[0] == 27105:
                    name = 'Casa Roja'
                elif row[0] == 27106:
                    name = 'Casa Verde'
                elif row[0] == 27107:
                    name = 'Edificio Azul'
                elif row[0] == 27108:
                    name = 'Fuente de Agua'
                elif row[0] == 27109:
                    name = 'Semaforo'
                elif row[0] == 27110:
                    name = 'Arbol'
                elif row[0] == 27111:
                    name = 'Obelisco'
                elif row[0] == 27112:
                    name = 'Taxi'
                elif row[0] == 27113:
                    name = 'Policia'
                elif row[0] == 27114:
                    name = 'Ambulancia'
                elif row[0] == 27115:
                    name = 'Camion de Bomberos'
                ByC_built_elementsCounter_Dictionary.append({
                    'id': row[0],
                    'name': name,
                    'counter': row[1]
                })
            ByC_built_elementsCounter_GraphSize = len(
                built_elementsCounter_QueryResponse) * 40 + 20

            ##CINEMA:

            ##2.1.- NUMBER OF ENTRANCES:
            Cinema_NumberOfEntrances_query = getNumberOfEntrances(request)
            queries.append({
                "name": 'NUMBER OF ENTRANCES',
                "query": Cinema_NumberOfEntrances_query
            })
            cursor.execute(Cinema_NumberOfEntrances_query)
            Cinema_NumberOfEntrances_QueryResponse = cursor.fetchall()
            for row in Cinema_NumberOfEntrances_QueryResponse:
                ByC_Cinema_NumberOfEntrances_Dictionary.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'numberOfEntrances':
                    row[2]
                })
            ByC_Cinema_NumberOfEntrances_GraphSize = len(
                Cinema_NumberOfEntrances_QueryResponse) * 40 + 20

            ##2.2.- CINEMA: ACTIVITY COMPLETE V/S INCOMPLETE:
            Cinema_CompleteVsIncomplete_query = getCinema_CompleteVsIncomplete(
                request)
            queries.append({
                "name": 'CINEMA: ACTIVITY COMPLETE V/S INCOMPLETE',
                "query": Cinema_CompleteVsIncomplete_query
            })
            cursor.execute(Cinema_CompleteVsIncomplete_query)
            Cinema_CompleteVsIncomplete_QueryResponse = cursor.fetchall()
            for row in Cinema_CompleteVsIncomplete_QueryResponse:
                ByC_Cinema_CompleteVsIncomplete_Dictionary.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'Complete':
                    row[2],
                    'Incomplete':
                    row[3]
                })
            ByC_Cinema_CompleteVsIncomplete_GraphSize = len(
                Cinema_CompleteVsIncomplete_QueryResponse) * 50 + 20

            ##2.3.- CINEMA: NUMBER OF SUCCESS V/S FAILURE:
            Cinema_SuccessVsFailure_query = getCinema_SuccessVsFailure(request)
            queries.append({
                "name": 'CINEMA: NUMBER OF SUCCESS V/S FAILURE',
                "query": Cinema_SuccessVsFailure_query
            })
            cursor.execute(Cinema_SuccessVsFailure_query)
            Cinema_SuccessVsFailure_QueryResponse = cursor.fetchall()
            for row in Cinema_SuccessVsFailure_QueryResponse:
                ByC_Cinema_SuccessVsFailure_Dictionary.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'Success':
                    row[2],
                    'Failure':
                    row[3],
                    'SuccessPercentage': round(row[2]/(row[2]+row[3])*100),
                    'FailurePercentage': round(row[3]/(row[2]+row[3])*100)
                })
                ByC_Cinema_Count_ParticularSuccess = ByC_Cinema_Count_ParticularSuccess + row[
                    2]
                ByC_Cinema_Count_ParticularFailure = ByC_Cinema_Count_ParticularFailure + row[
                    3]
            ByC_Cinema_TotalAttempts = (ByC_Cinema_Count_ParticularSuccess +
                                        ByC_Cinema_Count_ParticularFailure)
            if ByC_Cinema_TotalAttempts == 0:
                ByC_Cinema_TotalAttempts = 1
            ByC_Cinema_Average_ParticularSuccess = int(
                (ByC_Cinema_Count_ParticularSuccess / ByC_Cinema_TotalAttempts)
                * 100)
            ByC_Cinema_Average_ParticularFailure = 100 - ByC_Cinema_Average_ParticularSuccess
            ByC_Cinema_SuccessVsFailure_GraphSize = len(
                Cinema_SuccessVsFailure_QueryResponse) * 50 + 20

            Cinema_SuccessVsFailureGeneral_query = getCinema_SuccessVsFailureGeneral(
                request)
            queries.append({
                "name": 'CINEMA: NUMBER OF SUCCESS V/S FAILURE (GENERAL)',
                "query": Cinema_SuccessVsFailureGeneral_query
            })
            cursor.execute(Cinema_SuccessVsFailureGeneral_query)
            Cinema_SuccessVsFailureGeneral_QueryResponse = cursor.fetchall()
            for row in Cinema_SuccessVsFailureGeneral_QueryResponse:
                ByC_Cinema_Count_Success = ByC_Cinema_Count_Success + row[2]
                ByC_Cinema_Count_Failure = ByC_Cinema_Count_Failure + row[3]
            ByC_Cinema_Count_Attempts = ByC_Cinema_Count_Success + ByC_Cinema_Count_Failure
            if ByC_Cinema_Count_Attempts == 0:
                ByC_Cinema_Count_Attempts = 1
            ByC_Cinema_Average_Success = round((ByC_Cinema_Count_Success/ByC_Cinema_Count_Attempts)*100)
            ByC_Cinema_Average_Failure = round((ByC_Cinema_Count_Failure/ByC_Cinema_Count_Attempts)*100)

            ##2.5.- CINEMA: SUCCESS PERCENTAGE IN TIME:
            Cinema_SuccessPercentageInTime_query = getCinema_SuccessPercentageInTime(
                request)
            queries.append({
                "name": 'CINEMA: NUMBER OF SUCCESS IN TIME',
                "query": Cinema_SuccessPercentageInTime_query
            })
            cursor.execute(Cinema_SuccessPercentageInTime_query)
            Cinema_SuccessPercentageInTime_QueryResponse = cursor.fetchall()
            for row in Cinema_SuccessPercentageInTime_QueryResponse:
                nombre = row[0]
                fecha = row[1]
                success = row[2]
                failure = row[3]
                attemps = success + failure
                if (attemps == 0):
                    attemps = 1
                percentage = int((success / attemps) * 100)
                ByC_Cinema_SuccessPercentageInTime_Dictionary.append({
                    'name':
                    nombre,
                    'fecha':
                    fecha,
                    'percentage':
                    percentage
                })
            ByC_Cinema_SuccessPercentageInTime_GraphSize = len(
                Cinema_SuccessPercentageInTime_QueryResponse) * 50 + 20

            ##2.6.- CINEMA: NUMBER OF SUCCESS V/S FAILURE PARTICULAR SEATS:
            Cinema_SuccessVsFailure_ParticularSeats_query = getCinema_SuccessVsFailure_ParticularSeats(
                request)
            queries.append({
                "name":
                'CINEMA: NUMBER OF SUCCESS V/S FAILURE (PARTICULAR SEATS)',
                "query":
                Cinema_SuccessVsFailure_ParticularSeats_query
            })
            cursor.execute(Cinema_SuccessVsFailure_ParticularSeats_query)
            Cinema_SuccessVsFailure_ParticularSeats_QueryResponse = cursor.fetchall(
            )
            for row in Cinema_SuccessVsFailure_ParticularSeats_QueryResponse:
                ByC_Cinema_SuccessVsFailure_ParticularSeats_Dictionary.append({
                    'id':
                    row[0],
                    'name_student':
                    row[1],
                    'name_assistant':
                    row[2],
                    'Success':
                    row[3],
                    'Failure':
                    row[4]
                })
            ByC_Cinema_SuccessVsFailure_ParticularSeats_GraphSize = len(
                Cinema_SuccessVsFailure_ParticularSeats_QueryResponse) * 50 + 20

            ##SCHOOL:

            ##3.1.- SCHOOL: NUMBER OF ENTRANCES:
            School_NumberOfEntrances_query = getSchoolNumberOfEntrances(
                request)
            queries.append({
                "name": 'NUMBER OF ENTRANCES',
                "query": School_NumberOfEntrances_query
            })
            cursor.execute(School_NumberOfEntrances_query)
            School_NumberOfEntrances_QueryResponse = cursor.fetchall()
            for row in School_NumberOfEntrances_QueryResponse:
                ByC_School_NumberOfEntrances_Dictionary.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'numberOfEntrances':
                    row[2],
                })
            ByC_School_NumberOfEntrances_GraphSize = len(
                School_NumberOfEntrances_QueryResponse) * 40 + 20

            ##3.2.- SCHOOL: ACTIVITY COMPLETE V/S INCOMPLETE:
            School_CompleteVsIncomplete_query = getSchool_CompleteVsIncomplete(
                request)
            queries.append({
                "name": 'School: ACTIVITY COMPLETE V/S INCOMPLETE',
                "query": School_CompleteVsIncomplete_query
            })
            cursor.execute(School_CompleteVsIncomplete_query)
            School_CompleteVsIncomplete_QueryResponse = cursor.fetchall()
            for row in School_CompleteVsIncomplete_QueryResponse:
                ByC_School_CompleteVsIncomplete_Dictionary.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'Complete':
                    row[2],
                    'Incomplete':
                    row[3]
                })
            ByC_School_CompleteVsIncomplete_GraphSize = len(
                School_CompleteVsIncomplete_QueryResponse) * 50 + 20

            ##3.3.- SCHOOL: NUMBER OF SUCCESS V/S FAILURE:
            School_SuccessVsFailure_query = getSchool_SuccessVsFailure(request)
            queries.append({
                "name": 'School: NUMBER OF SUCCESS V/S FAILURE',
                "query": School_SuccessVsFailure_query
            })
            cursor.execute(School_SuccessVsFailure_query)
            School_SuccessVsFailure_QueryResponse = cursor.fetchall()
            for row in School_SuccessVsFailure_QueryResponse:
                ByC_School_SuccessVsFailure_Dictionary.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'Success':
                    row[2],
                    'Failure':
                    row[3],
                    'SuccessPercentage': round(row[2]/(row[2]+row[3])*100),
                    'FailurePercentage': round(row[3]/(row[2]+row[3])*100)
                })
                ByC_School_Count_ParticularSuccess = ByC_School_Count_ParticularSuccess + row[2]
                ByC_School_Count_ParticularFailure = ByC_School_Count_ParticularFailure + row[3]
            ByC_School_TotalAttempts = (ByC_School_Count_ParticularSuccess +
                                        ByC_School_Count_ParticularFailure)
            if ByC_School_TotalAttempts == 0:
                ByC_School_TotalAttempts = 1
            ByC_School_Average_ParticularSuccess = int(
                (ByC_School_Count_ParticularSuccess / ByC_School_TotalAttempts)
                * 100)
            ByC_School_Average_ParticularFailure = 100 - ByC_School_Average_ParticularSuccess
            ByC_School_SuccessVsFailure_GraphSize = len(
                School_SuccessVsFailure_QueryResponse) * 50 + 20

            School_SuccessVsFailureGeneral_query = getSchool_SuccessVsFailureGeneral(
                request)
            queries.append({
                "name": 'School: NUMBER OF SUCCESS V/S FAILURE (GENERAL)',
                "query": School_SuccessVsFailureGeneral_query
            })
            cursor.execute(School_SuccessVsFailureGeneral_query)
            School_SuccessVsFailureGeneral_QueryResponse = cursor.fetchall()
            for row in School_SuccessVsFailureGeneral_QueryResponse:
                ByC_School_Count_Success = ByC_School_Count_Success + row[2]
                ByC_School_Count_Failure = ByC_School_Count_Failure + row[3]
            ByC_School_Count_Attempts = ByC_School_Count_Success + ByC_School_Count_Failure
            if ByC_School_Count_Attempts == 0:
                ByC_School_Count_Attempts = 1
            ByC_School_Average_Success = round((ByC_School_Count_Success / ByC_School_Count_Attempts)*100)
            ByC_School_Average_Failure = round((ByC_School_Count_Failure / ByC_School_Count_Attempts)*100)

            ##3.5.- SCHOOL: SUCCESS PERCENTAGE IN TIME:
            School_SuccessPercentageInTime_query = getSchool_SuccessPercentageInTime(
                request)
            queries.append({
                "name": 'School: NUMBER OF SUCCESS IN TIME',
                "query": School_SuccessPercentageInTime_query
            })
            cursor.execute(School_SuccessPercentageInTime_query)
            School_SuccessPercentageInTime_QueryResponse = cursor.fetchall()
            for row in School_SuccessPercentageInTime_QueryResponse:
                nombre = row[0]
                fecha = row[1]
                success = row[2]
                failure = row[3]
                attemps = success + failure
                if (attemps == 0):
                    attemps = 1
                percentage = int((success / attemps) * 100)
                ByC_School_SuccessPercentageInTime_Dictionary.append({
                    'name':
                    nombre,
                    'fecha':
                    fecha,
                    'percentage':
                    percentage
                })
            ByC_School_SuccessPercentageInTime_GraphSize = len(
                School_SuccessPercentageInTime_QueryResponse) * 50 + 20

            ##3.6.- SCHOOL: NUMBER OF SUCCESS V/S FAILURE PARTICULAR SEATS:
            School_SuccessVsFailure_ParticularSeats_query = getSchool_SuccessVsFailure_ParticularSeats(
                request)
            queries.append({
                "name":
                'School: NUMBER OF SUCCESS V/S FAILURE (PARTICULAR SEATS)',
                "query":
                School_SuccessVsFailure_ParticularSeats_query
            })
            cursor.execute(School_SuccessVsFailure_ParticularSeats_query)
            School_SuccessVsFailure_ParticularSeats_QueryResponse = cursor.fetchall(
            )
            for row in School_SuccessVsFailure_ParticularSeats_QueryResponse:
                ByC_School_SuccessVsFailure_ParticularSeats_Dictionary.append({
                    'id':
                    row[0],
                    'name_student':
                    row[1],
                    'name_assistant':
                    row[2],
                    'Success':
                    row[3],
                    'Failure':
                    row[4]
                })
            ByC_School_SuccessVsFailure_ParticularSeats_GraphSize = len(
                School_SuccessVsFailure_ParticularSeats_QueryResponse) * 50 + 20

            ##TAXI:
            ##4.1.- TAXI: NUMBER OF ENTRANCES:
            Taxi_NumberOfEntrances_query = getTaxiNumberOfEntrances(request)
            queries.append({
                "name": 'NUMBER OF ENTRANCES',
                "query": Taxi_NumberOfEntrances_query
            })
            cursor.execute(Taxi_NumberOfEntrances_query)
            Taxi_NumberOfEntrances_QueryResponse = cursor.fetchall()
            for row in Taxi_NumberOfEntrances_QueryResponse:
                ByC_Taxi_NumberOfEntrances_Dictionary.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'numberOfEntrances':
                    row[2]
                })
            ByC_Taxi_NumberOfEntrances_GraphSize = len(
                Taxi_NumberOfEntrances_QueryResponse) * 40 + 20

            ##4.2.- TAXI: ACTIVITY COMPLETE V/S INCOMPLETE:
            Taxi_CompleteVsIncomplete_query = getTaxi_CompleteVsIncomplete(
                request)
            queries.append({
                "name": 'Taxi: ACTIVITY COMPLETE V/S INCOMPLETE',
                "query": Taxi_CompleteVsIncomplete_query
            })
            cursor.execute(Taxi_CompleteVsIncomplete_query)
            Taxi_CompleteVsIncomplete_QueryResponse = cursor.fetchall()
            for row in Taxi_CompleteVsIncomplete_QueryResponse:
                ByC_Taxi_CompleteVsIncomplete_Dictionary.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'Complete':
                    row[2],
                    'Incomplete':
                    row[3]
                })
            ByC_Taxi_CompleteVsIncomplete_GraphSize = len(
                Taxi_CompleteVsIncomplete_QueryResponse) * 50 + 20

            ##4.3.- TAXI: NUMBER OF SUCCESS V/S FAILURE:
            Taxi_SuccessVsFailure_query = getTaxi_SuccessVsFailure(request)
            queries.append({
                "name": 'Taxi: NUMBER OF SUCCESS V/S FAILURE',
                "query": Taxi_SuccessVsFailure_query
            })
            cursor.execute(Taxi_SuccessVsFailure_query)
            Taxi_SuccessVsFailure_QueryResponse = cursor.fetchall()
            for row in Taxi_SuccessVsFailure_QueryResponse:
                ByC_Taxi_SuccessVsFailure_Dictionary.append({
                    'id': row[0],
                    'name': row[1],
                    'Success': row[2],
                    'Failure': row[3],
                    'SuccessPercentage': round(row[2]/(row[2]+row[3])*100),
                    'FailurePercentage': round(row[3]/(row[2]+row[3])*100)
                })
                ByC_Taxi_Count_ParticularSuccess = ByC_Taxi_Count_ParticularSuccess + row[2]
                ByC_Taxi_Count_ParticularFailure = ByC_Taxi_Count_ParticularFailure + row[3]
            ByC_Taxi_TotalAttempts = (ByC_Taxi_Count_ParticularSuccess +
                                      ByC_Taxi_Count_ParticularFailure)
            if ByC_Taxi_TotalAttempts == 0:
                ByC_Taxi_TotalAttempts = 1
            ByC_Taxi_Average_ParticularSuccess = round(
                (ByC_Taxi_Count_ParticularSuccess / ByC_Taxi_TotalAttempts) *
                100)
            ByC_Taxi_Average_ParticularFailure = 100 - ByC_Taxi_Average_ParticularSuccess
            ByC_Taxi_SuccessVsFailure_GraphSize = len(
                Taxi_SuccessVsFailure_QueryResponse) * 50 + 20

            Taxi_SuccessVsFailureGeneral_query = getTaxi_SuccessVsFailureGeneral(
                request)
            queries.append({
                "name": 'Taxi: NUMBER OF SUCCESS V/S FAILURE (GENERAL)',
                "query": Taxi_SuccessVsFailureGeneral_query
            })
            cursor.execute(Taxi_SuccessVsFailureGeneral_query)
            Taxi_SuccessVsFailureGeneral_QueryResponse = cursor.fetchall()
            for row in Taxi_SuccessVsFailureGeneral_QueryResponse:
                ByC_Taxi_Count_Success = ByC_Taxi_Count_Success + row[2]
                ByC_Taxi_Count_Failure = ByC_Taxi_Count_Failure + row[3]
                ByC_Taxi_Count_Attempts = ByC_Taxi_Count_Success + ByC_Taxi_Count_Failure
            if ByC_Taxi_Count_Attempts == 0:
                ByC_Taxi_Count_Attempts = 1
            ByC_Taxi_Average_Success = round((ByC_Taxi_Count_Success / ByC_Taxi_Count_Attempts)*100)
            ByC_Taxi_Average_Failure = round((ByC_Taxi_Count_Failure / ByC_Taxi_Count_Attempts)*100)

            ##4.5.- TAXI: SUCCESS PERCENTAGE IN TIME:
            Taxi_SuccessPercentageInTime_query = getTaxi_SuccessPercentageInTime(
                request)
            queries.append({
                "name": 'Taxi: NUMBER OF SUCCESS IN TIME',
                "query": Taxi_SuccessPercentageInTime_query
            })
            cursor.execute(Taxi_SuccessPercentageInTime_query)
            Taxi_SuccessPercentageInTime_QueryResponse = cursor.fetchall()
            for row in Taxi_SuccessPercentageInTime_QueryResponse:
                nombre = row[0]
                fecha = row[1]
                success = row[2]
                failure = row[3]
                attemps = success + failure
                if (attemps == 0):
                    attemps = 1
                percentage = round((success / attemps) * 100)
                ByC_Taxi_SuccessPercentageInTime_Dictionary.append({
                    'name':
                    nombre,
                    'fecha':
                    fecha,
                    'percentage':
                    percentage
                })
            ByC_Taxi_SuccessPercentageInTime_GraphSize = len(
                Taxi_SuccessPercentageInTime_QueryResponse) * 50 + 20

            ##4.6.- TAXI: NUMBER OF SUCCESS V/S FAILURE PARTICULAR SEATS:
            Taxi_SuccessVsFailure_ParticularSeats_query = getTaxi_SuccessVsFailure_ParticularSeats(
                request)
            queries.append({
                "name":
                'Taxi: NUMBER OF SUCCESS V/S FAILURE (PARTICULAR SEATS)',
                "query": Taxi_SuccessVsFailure_ParticularSeats_query
            })
            cursor.execute(Taxi_SuccessVsFailure_ParticularSeats_query)
            Taxi_SuccessVsFailure_ParticularSeats_QueryResponse = cursor.fetchall(
            )
            for row in Taxi_SuccessVsFailure_ParticularSeats_QueryResponse:
                ByC_Taxi_SuccessVsFailure_ParticularSeats_Dictionary.append({
                    'id':
                    row[0],
                    'name_student':
                    row[1],
                    'name_assistant':
                    row[2],
                    'Success':
                    row[3],
                    'Failure':
                    row[4]
                })
            ByC_Taxi_SuccessVsFailure_ParticularSeats_GraphSize = len(
                Taxi_SuccessVsFailure_ParticularSeats_QueryResponse) * 50 + 20
        ######END BUILD YOUR CITY######
            ##### INICIO PROTECT YOUR LAND

        PYL_numberOfSessions_Dictionary = []
        PYL_playTime_Dictionary = []
        PYL_touchCount_Dictionary = []
        PYL_activitiesPlayedCounter_Dictionary = []
        PYL_color_Dictionary = []
        PYLcorrects_quantity_Dictionary = []
        PYL_correctsxsession_Dictionary = []
        PYL_answer_Dictionary = []
        PYL_answerOA_Dictionary = []
        PYL_emociones_Dictionary = []
        PYL_timer_Dictionary = []
        PYL_ElemVisual_Dictionary = []

        PYL_playTime_GraphSize = 0
        PYL_touchCount_GraphSize = 0
        PYL_activitiesPlayedCounter_GraphSize = 0
        PYL_numberOfSessions_GraphSize = 0
        PYL_color_GraphSize = 0
        PYL_correctsxsession_GraphSize = 0
        PYLcorrects_quantity_graph = 0
        PYL_answer_GraphSize = 0
        PYL_answerOA_GraphSize = 0
        PYL_emociones_GraphSize = 0
        PYL_timer_GraphSize = 0
        PYL_ElemVisual_GraphSize = 0

        if reim_num == "202":

            ##GET NUMBER OF SESSIONS##
            PYLgetNumberOfSessions_query = get_number_of_sessionsPYL(request)
            cursor.execute(PYLgetNumberOfSessions_query)
            queries.append({
                "name": 'Get Number Of Sessions',
                "query": PYLgetNumberOfSessions_query
            })
            PYLnumberOfSessions_QueryResponse = cursor.fetchall()
            # print ("analytics1_co_quantity", analytics1_co_quantity)
            for row in PYLnumberOfSessions_QueryResponse:
                PYL_numberOfSessions_Dictionary.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
            PYL_numberOfSessions_GraphSize = len(PYLnumberOfSessions_QueryResponse) * 40 + 20

            ##PLAYTIME REIM##
            getPlayTimePYL = get_playtimePYL(request)
            cursor.execute(getPlayTimePYL)
            queries.append({
                "name": 'Get PlayTime of REIM',
                "query": getPlayTimePYL
            })
            PYLplayTime_QueryResponse = cursor.fetchall()
            print("playTime_QueryResponse", PYLplayTime_QueryResponse)
            for row in PYLplayTime_QueryResponse:
                PYL_playTime_Dictionary.append({
                    'id': row[0],
                    'name': row[1],
                    'playTime': row[2]
                })
            PYL_playTime_GraphSize = len(PYLplayTime_QueryResponse) * 40 + 20

            ##TOUCH COUNT REIM##
            PYLtouch_query = get_touch_count(request)
            queries.append({"name": 'Get Touch Count', "query": PYLtouch_query})
            cursor.execute(touch_query)
            PYLtouchCount_QueryResponse = cursor.fetchall()
            for row in PYLtouchCount_QueryResponse:
                PYL_touchCount_Dictionary.append({
                    'id': row[0],
                    'name': row[1],
                    'touchCount': row[2]
                })
            PYL_touchCount_GraphSize = len(PYLtouchCount_QueryResponse) * 40 + 20

            ##ACTIVITIES PLAYED COUNTER##
            PYLtouch_query = get_activities_played_counterPYL(request)
            queries.append({
                "name": 'Activities Played Counter',
                "query": PYLtouch_query
            })
            cursor.execute(PYLtouch_query)
            PYLactivitiesPlayedCounter_QueryResponse = cursor.fetchall()
            for row in PYLactivitiesPlayedCounter_QueryResponse:
                name = ''
                if row[0] == 280000:
                    name = 'Actividad 1: FootPrints'
                elif row[0] == 280001:
                    name = 'Actividad 2: Draw Solutions'
                elif row[0] == 280002:
                    name = 'Actividad 3: Art Gallery'
                elif row[0] == 280004:
                    name = 'Actividad 4: Build Your Land'
                PYL_activitiesPlayedCounter_Dictionary.append({
                    'id': row[0],
                    'name': name,
                    'counter': row[1]
                })
            PYL_activitiesPlayedCounter_GraphSize = len(
                PYLactivitiesPlayedCounter_QueryResponse) * 40 + 20
            ##ACTIVIDAD FOOT PRINTS

            correctsPYL_query = get_corrects_PYL(request)
            cursor.execute(correctsPYL_query)
            queries.append({
                "name": 'Corrects query',
                "query": correctsPYL_query
            })
            PYLcorrects_quantity = cursor.fetchall()
            for row in PYLcorrects_quantity:
                PYLcorrects_quantity_Dictionary.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
            PYLcorrects_quantity_graph = len(PYLcorrects_quantity) * 40 + 20

            ##CORRECTAS CAPTURADAS FOOTPRINTS
            get_correctsxsession_PYL_query = get_correctsxsession_PYL(request)
            cursor.execute(get_correctsxsession_PYL_query)
            queries.append({
                "name": 'Get Number Of Sessions',
                "query": get_correctsxsession_PYL_query
            })
            get_correctsxsession_PYLResponse = cursor.fetchall()
            for row in get_correctsxsession_PYLResponse:
                PYL_correctsxsession_Dictionary.append({
                    'name': row[0],
                    'fecha': row[1],
                    'quantity': row[2]
                })
            PYL_correctsxsession_GraphSize = len(get_correctsxsession_PYLResponse) * 40 + 20

            get_timer_PYL_query = PYL_getTimer(request)
            cursor.execute(get_timer_PYL_query)
            queries.append({
                "name": 'timer',
                "query": get_timer_PYL_query
            })
            get_timer_PYLResponse = cursor.fetchall()
            for row in get_timer_PYLResponse:
                PYL_timer_Dictionary.append({
                    'id': row[0],
                    'nombre': row[1],
                    'maximo': row[2],
                    'minimo': row[3]

                })
            PYL_timer_GraphSize = len(get_timer_PYLResponse) * 40 + 20

            ##ACTIVIDAD DRAW SOLUTIONS
            PYLcolor_query = get_activities_colorPYL(request)
            queries.append({
                "name": 'Activities Played Counter',
                "query": PYLcolor_query
            })
            cursor.execute(PYLcolor_query)
            PYLcolor_QueryResponse = cursor.fetchall()
            for row in PYLcolor_QueryResponse:
                name = ''
                if row[0] == 280100:
                    name = 'Rojo'
                elif row[0] == 280101:
                    name = 'Azúl'
                elif row[0] == 280102:
                    name = 'Verde'
                elif row[0] == 280103:
                    name = 'Amarillo'
                elif row[0] == 280104:
                    name = 'Negro'
                PYL_color_Dictionary.append({
                    'id': row[0],
                    'name': name,
                    'counter': row[1]
                })
            PYL_color_GraphSize = len(
                PYLcolor_QueryResponse) * 40 + 20
        ####
            PYL_ElemVisual_query = get_ElemVisual_PYL(request)
            cursor.execute(PYL_ElemVisual_query)
            queries.append({
                "name": 'Get Number Of reaccion',
                "query": PYL_ElemVisual_query
            })
            PYL_ElemVisual_query_Response = cursor.fetchall()
            for row in PYL_ElemVisual_query_Response:
                PYL_ElemVisual_Dictionary.append({
                    'id': row[0],
                    'nombre': row[1],
                    'Intensidad': row[2],
                    'Grosor': row[3],
                    'Borrar': row[4],
                })
            PYL_ElemVisual_GraphSize = len(PYL_ElemVisual_query_Response) * 40 + 20

            ### ACTIVIDAD GALLERY

            PYL_emociones_query = PYL_Get_Emociones(request)
            cursor.execute(PYL_emociones_query)
            queries.append({
                "name": 'Get Number Of reaccion',
                "query": PYL_emociones_query
            })
            PYL_emociones_query_Response = cursor.fetchall()
            for row in PYL_emociones_query_Response:
                PYL_emociones_Dictionary.append({
                    'id': row[0],
                    'nombre': row[1],
                    'Sorprendido': row[2],
                    'Triste': row[3],
                    'Encantado': row[4],
                    'Feliz': row[5],
                })
            PYL_emociones_GraphSize = len(PYL_emociones_query_Response) * 40 + 20

            ##ACTIVIDAD BUILD YOUR LAND

            PYL_answer_query = PYL_Get_Answer(request)
            cursor.execute(PYL_answer_query)
            queries.append({
                "name": 'Get Number Of Sessions',
                "query": PYL_answer_query
            })
            PYL_answer_query_Response = cursor.fetchall()
            for row in PYL_answer_query_Response:
                PYL_answer_Dictionary.append({
                    'id': row[0],
                    'nombre': row[1],
                    'Correcta': row[2],
                    'Incorrecta': row[3],
                    'Pregunta': row[4]
                })
            PYL_answer_GraphSize = len(PYL_answer_query_Response) * 40 + 20

            PYL_answerOA_query = PYL_Get_AnswerxOA(request)
            cursor.execute(PYL_answerOA_query)
            queries.append({
                "name": 'GetAnswerxOA',
                "query": PYL_answerOA_query
            })
            PYL_answerOA_query_Response = cursor.fetchall()
            for row in PYL_answerOA_query_Response:
                PYL_answerOA_Dictionary.append({
                    'Correcta': row[0],
                    'Incorrecta': row[1],
                    'id': row[2],
                    'OA': row[3]
                })
            PYL_answerOA_GraphSize = len(PYL_answerOA_query_Response) * 40 + 20

        #INICIO MUNDO ANIMAL
        piezas_quantity_response = []
        malas_quantity_response = []
        animales_quantity_response = []
        actividades_quantity_response = []
        interaccion_quantity_response = []
        tiempoact_quantity_response = []
        analytics1_co_quantity_response = []
        tiempo_total_quantity_response = []
        audios_quantity_response = []
        total_correctas = 0
        count1 = 1
        promedio_correctas = 0
        animales_quantity_graph = 0
        total_incorrectas = 0
        count2 = 1
        promedio_incorrectas = 0

        if reim_num == "1":

            analytics1_co_query = get_analytics1_co(request)
            cursor.execute(analytics1_co_query)
            queries.append({
                "name": 'Analytics1 co query',
                "query": analytics1_co_query
            })
            analytics1_co_quantity = cursor.fetchall()
            #print ("analytics1_co_quantity", analytics1_co_quantity)
            for row in analytics1_co_quantity:
                analytics1_co_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'act1': row[2],
                    'act2': row[3],
                    'act3': row[4],
                    'act4': row[5]
                })

            piezas_query = get_piezas(request)
            cursor.execute(piezas_query)
            queries.append({"name": 'Piezas query', "query": piezas_query})
            piezas_quantity = cursor.fetchall()
            #print ("piezas quantity", piezas_quantity)
            for row in piezas_quantity:
                piezas_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
                total_correctas += row[2]
                count1 = count1 + 1
            promedio_correctas = total_correctas / count1

            malas_query = get_malas(request)
            cursor.execute(malas_query)
            queries.append({"name": 'Malas query', "query": malas_query})
            malas_quantity = cursor.fetchall()
            #print("malas quantity", malas_quantity)
            for row in malas_quantity:
                malas_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
                total_incorrectas += row[2]
                count2 = count2 + 1
            promedio_incorrectas = total_incorrectas / count2

            animales_query = get_animals(request)
            cursor.execute(animales_query)
            queries.append({"name": 'Animales query', "query": animales_query})
            animales_quantity = cursor.fetchall()
            #print("animales quantity", animales_quantity)
            for row in animales_quantity:
                animales_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
            animales_quantity_graph = len(animales_quantity) * 40 + 20

            interaccion_query = get_interaccion(request)
            cursor.execute(interaccion_query)
            queries.append({
                "name": 'Interaccion query',
                "query": interaccion_query
            })
            interaccion_quantity = cursor.fetchall()
            #print("interacccion quantity", interaccion_quantity)
            for row in interaccion_quantity:
                interaccion_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })

            tiempoact_query = get_tiempoact(request)
            cursor.execute(tiempoact_query)
            queries.append({
                "name": 'Tiempoact query',
                "query": tiempoact_query
            })
            tiempoact_quantity = cursor.fetchall()
            #print("tiempoact quantity", tiempoact_quantity)
            for row in tiempoact_quantity:
                tiempoact_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })

            actividades_query = get_cant_touch(request)
            cursor.execute(actividades_query)
            queries.append({
                "name": 'Actividades query',
                "query": actividades_query
            })
            actividades_quantity = cursor.fetchall()
            #print("actividades quantity", actividades_quantity)
            for row in actividades_quantity:
                actividades_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })

            tiempo_total_query = get_tiempo_total_act(request)
            cursor.execute(tiempo_total_query)
            queries.append({
                "name": 'Tiempo total por act query',
                "query": tiempo_total_query
            })
            tiempo_total_quantity = cursor.fetchall()
            #print("tiempo total por act quantity", tiempo_total_quantity)
            for row in tiempo_total_quantity:
                tiempo_total_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })

            audios_query = get_audios(request)
            cursor.execute(audios_query)
            queries.append({"name": 'Audios query', "query": audios_query})
            audios_quantity = cursor.fetchall()
            for row in audios_quantity:
                audios_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })

        #FIN MUNDO ANIMAL

        #filtro estudiente
        activate_student_filter = False
        if request.GET.get('student') and request.GET.get('student') != "0":
            activate_student_filter = True

        #INICIO DIA MUNDIAL
        #Generales
        nombre = []
        sesiones_PS_quantity_response = []
        time_PS_quantity_response = []
        tiempoXact_quantity_responseDM = []  ##TIEMPO  POR ACTIVIDAD
        completa_incompleta_inactividad = []
        get_ganar_perder_DM_Quest_response = []

        #QUERYS LAB
        completa_incompleta_DM_quantity_response = []
        fruta_chatarra_DM_quantity_response = []
        muro_hoyo_DM_quantity_response = []
        col_vs_time = []
        #QUERYS RIO OCE
        tipo_basura_DM_quantity_response = []
        animales_nivel_DM_quantity_response = []
        #QUERYS LUCES
        touches_luces_DM_quantity_response = []
        #QUERYS ABEJA
        get_miel_cae_choca_DM_quantity_response = []
        #QUERYS ANIMALES
        get_animales_salvados_DM_quantity_response = []
        get_animales_salvados_pornivel_DM_quantity_response = []
        #QUERYS ARBOL
        correcta_incorrecta_arbol_DM_quantity_response = []
        crecimiento_arbol_DM_quantity_response = []

        #TAMAÑOS
        total_completa_incompleta = 0
        time_DM_graf = 0
        colisiones_tiempo_media = -1
        colisiones_muro_media = 0
        colisiones_hoyo_media = 0

        lista_alumnos_final = []
        lista_alumnos_final2 = []
        lista_unico_alumno = []

        if reim_num == "4":

            #GRAN GRAFICO
            lista_alumnos = get_alumnos_and_id(request)
            cursor.execute(lista_alumnos)
            lista_alumnos = cursor.fetchall()
            for alumnoo in lista_alumnos:
                alumnoC = [alumnoo[1], 0, 0, 0, 0, alumnoo[0]]
                sesiones_lab = get_laberinto_porniño(request, alumnoo[0])
                cursor.execute(sesiones_lab)
                sesiones_lab = cursor.fetchall()
                if len(sesiones_lab) > 3:
                    a = 0
                    error_max = 0
                    porcent = 0
                    for sesion_lab in sesiones_lab:
                        if a == 2:
                            error_max = sesion_lab[2]
                        else:
                            if a > 2 and error_max > 0:
                                b = (100 * sesion_lab[2]) / error_max
                                porcent += b
                        a += 1
                    porcent = porcent / (len(sesiones_lab) - 3)
                    alumnoC[1] = porcent
                sesiones_abejas = get_abejas_porniño(request, alumnoo[0])
                cursor.execute(sesiones_abejas)
                sesiones_abejas = cursor.fetchall()
                if len(sesiones_abejas) > 3:
                    a = 0
                    error_max = 0
                    porcentt = 0
                    for sesion_lab in sesiones_abejas:
                        if a == 2:
                            error_max = sesion_lab[2]
                        else:
                            if a > 2 and error_max > 0:
                                b = (100 * sesion_lab[2]) / error_max
                                porcentt += b
                        a += 1
                    porcentt = porcentt / (len(sesiones_abejas) - 3)
                    alumnoC[2] = porcentt
                sesiones_luces = get_luces_porniño(request, alumnoo[0])
                cursor.execute(sesiones_luces)
                sesiones_luces = cursor.fetchall()
                if len(sesiones_luces) > 3:
                    a = 0
                    error_max = 0
                    porcenttt = 0
                    for sesion_lab in sesiones_luces:
                        if a == 2:
                            error_max = sesion_lab[2]
                        else:
                            if a > 2 and error_max > 0:
                                b = (100 * sesion_lab[2]) / error_max
                                porcenttt += b
                        a += 1
                    porcenttt = porcenttt / (len(sesiones_luces) - 3)
                    alumnoC[3] = porcenttt
                sesiones_ocerio = get_oceanorio_porniño(request, alumnoo[0])
                cursor.execute(sesiones_ocerio)
                sesiones_ocerio = cursor.fetchall()
                if len(sesiones_ocerio) > 3:
                    a = 0
                    error_max = 0
                    porcentttt = 0
                    for sesion_lab in sesiones_ocerio:
                        if a == 2:
                            error_max = sesion_lab[2]
                        else:
                            if a > 2 and error_max > 0:
                                b = (100 * sesion_lab[2]) / error_max
                                porcentttt += b
                        a += 1
                    porcentttt = porcentttt / (len(sesiones_ocerio) - 3)
                    alumnoC[4] = porcentttt
                lista_alumnos_final.append(alumnoC)
            lista_unico_alumno = []
            for alm in lista_alumnos_final:
                if int(student_num) == int(alm[5]):
                    print(
                        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
                    )
                    lista_unico_alumno.append({
                        'name': alm[0],
                        'lab': int(alm[1]),
                        'abejas': int(alm[2]),
                        'luces': int(alm[3]),
                        'ocerio': int(alm[4]),
                        'id': alm[5]
                    })
                prcentt = 0
                bb = 0
                if alm[1] != 0:
                    prcentt += alm[1]
                    bb += 1
                if alm[2] != 0:
                    prcentt += alm[2]
                    bb += 1
                if alm[3] != 0:
                    prcentt += alm[3]
                    bb += 1
                if alm[4] != 0:
                    prcentt += alm[4]
                    bb += 1
                if bb > 0:
                    prcentt = int(prcentt / bb)
                    prcentt = 100 - prcentt
                lista_alumnos_final2.append({
                    'name': alm[0],
                    'porcent': prcentt
                })
            print(lista_alumnos_final)
            print(
                "---------------------------------------------O---------------------------------------------------"
            )
            print(lista_alumnos_final2)

            #General
            nombre_query = get_name_student(request)
            queries.append({
                "name": 'nombre estudiante',
                "query": nombre_query
            })
            cursor.execute(nombre_query)
            nombre_quantity = cursor.fetchall()
            for row in nombre_quantity:
                nombre.append({'name': row[0]})

            sesiones_PS_query = get_time_act_co(request)
            queries.append({
                "name": 'Tiempo Actividad sesion query',
                "query": sesiones_PS_query
            })
            cursor.execute(sesiones_PS_query)
            sesiones_PS_quantity = cursor.fetchall()
            for row in sesiones_PS_quantity:
                sesiones_PS_quantity_response.append({'id': row[0]})

            time_PS_query = get_time_act_co(request)
            queries.append({
                "name": 'Tiempo Actividad query',
                "query": time_PS_query
            })
            cursor.execute(time_PS_query)
            time_PS_quantity = cursor.fetchall()
            for row in time_PS_quantity:
                time_PS_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })

        #tiempo por actividad general
            tiempoXact_query = get_tiempoactDM(request)
            cursor.execute(tiempoXact_query)
            queries.append({
                "name": 'TiempoXact query',
                "query": tiempoXact_query
            })
            tiempoXact_quantity = cursor.fetchall()
            print("tiempoXact quantity", tiempoXact_quantity)
            for row in tiempoXact_quantity:
                tiempoXact_quantity_responseDM.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })

        #QUEST DM
            completa_incompleta_PS_query = get_ganar_perder_DM_Quest(request)
            queries.append({
                "name": 'Correcta Incorrecta Quest DM query',
                "query": completa_incompleta_PS_query
            })
            cursor.execute(completa_incompleta_PS_query)
            completa_incompleta_PS_quantity = cursor.fetchall()
            for row in completa_incompleta_PS_quantity:
                get_ganar_perder_DM_Quest_response.append({
                    'id': row[0],
                    'name': row[1],
                    'correcta': row[2],
                    'incorrecta': row[3]
                })

        ##JUEGO LABERINTO
        #Colisiones en el tiempo
            colission_analitica_query = get_colisiones_analitica_DM(request)
            queries.append({
                "name": 'colisiones tiempo',
                "query": colission_analitica_query
            })
            cursor.execute(colission_analitica_query)
            colission_analitica_quantity = cursor.fetchall()
            a = 0
            for row in colission_analitica_quantity:
                col_vs_time.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
                if a == 3:
                    colisiones_tiempo_media += row[2]
                a += 1
            for row in colission_analitica_quantity:
                col_vs_time.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })

        #CompletavsIncompleta
            completa_incompleta_PS_query = get_completa_incompleta_PS(request)
            queries.append({
                "name": 'Completas incompletas DM query',
                "query": completa_incompleta_PS_query
            })
            cursor.execute(completa_incompleta_PS_query)
            completa_incompleta_PS_quantity = cursor.fetchall()
            for row in completa_incompleta_PS_quantity:
                completa_incompleta_inactividad.append({
                    'id': row[0],
                    'name': row[1],
                    'completa': row[2],
                    'incompleta': row[3],
                    'inactiva': row[4]
                })

        #Fruta vs Chatarra
            elementos_PS_query = get_ganar_perder_lab(request)
            queries.append({
                "name": 'Fruta Chatarra DM query',
                "query": elementos_PS_query
            })
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                fruta_chatarra_DM_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'fruta': row[2],
                    'chatarra': row[3],
                })

        #Muro vs Hoyo
            muro_hoyo = get_colision_muro_hoyo(request)
            queries.append({"name": 'Muro Hoyo DM query', "query": muro_hoyo})
            cursor.execute(muro_hoyo)
            muro_hoyo_quantity = cursor.fetchall()
            for row in muro_hoyo_quantity:
                muro_hoyo_DM_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'muro': row[2],
                    'hoyo': row[3]
                })
                colisiones_muro_media += row[2]
                colisiones_hoyo_media += row[3]

        ##JUEGO RIO OCEANO
        #Tipo basura
            elementos_PS_query = get_tipo_basura(request)
            queries.append({
                "name": 'Tipo Basura DM query',
                "query": elementos_PS_query
            })
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                tipo_basura_DM_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'bolsa': row[2],
                    'botella': row[3],
                    'mancha': row[4],
                    'red': row[5],
                    'zapato': row[6],
                })

        #Animal Nivel
            elementos_PS_query = get_animales_nivel(request)
            queries.append({
                "name": 'Animales Nivel DM query',
                "query": elementos_PS_query
            })
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                animales_nivel_DM_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'animalesoceano':
                    row[2],
                    'animalesrio':
                    row[3],
                    'basuraoceano':
                    row[4],
                    'basurario':
                    row[5],
                })

        ##JUEGO LUCES
        #Touches Luces
            elementos_PS_query = get_touches_luces(request)
            queries.append({
                "name": 'Touches Luces DM query',
                "query": elementos_PS_query
            })
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                touches_luces_DM_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'touches':
                    row[2],
                    'lucescorrectas':
                    row[3],
                })

        ##JUEGO ABEJA
        #GET MIEL
            elementos_PS_query = get_miel_cae_choca(request)
            queries.append({
                "name": 'Get Miel DM query',
                "query": elementos_PS_query
            })
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                get_miel_cae_choca_DM_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'colisionpanal':
                    row[2],
                    'colisionsuelo':
                    row[3],
                    'colisionosoavispa':
                    row[4],
                })

        ##JUEGO ANIMALES
        #ANIMALES SALVADOS
            elementos_PS_query = get_animales_salvados(request)
            queries.append({
                "name": 'Animales Salvados DM query',
                "query": elementos_PS_query
            })
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                get_animales_salvados_DM_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'ballena':
                    row[2],
                    'oso':
                    row[3],
                    'pinguino':
                    row[4],
                    'pepino':
                    row[5],
                    'pajaro':
                    row[6],
                    'foca':
                    row[7],
                    'tigre':
                    row[8],
                    'cocodrilo':
                    row[9],
                    'mono':
                    row[10],
                    'serpiente':
                    row[11],
                    'perezoso':
                    row[12],
                    'rana':
                    row[13],
                    'lagartija':
                    row[14],
                    'lemur':
                    row[15],
                    'camaleon':
                    row[16],
                    'tortuga':
                    row[17],
                    'leon':
                    row[18],
                    'fosa':
                    row[19]
                })

        #ANIMALES SALVADOS POR NIVEL
            elementos_PS_query = get_animales_salvados_pornivel(request)
            queries.append({
                "name": 'Animales Salvados Por Nivel DM query',
                "query": elementos_PS_query
            })
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                get_animales_salvados_pornivel_DM_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'animalesantartica':
                    row[2],
                    'animalesselva':
                    row[3],
                    'animalesmadagascar':
                    row[4],
                })

        ##JUEGO ARBOL
        #Correcta Incorrecta
            elementos_PS_query = get_correcta_incorrecta_arbol(request)
            queries.append({
                "name": 'Correcta Incorrecta Arbol DM query',
                "query": elementos_PS_query
            })
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                correcta_incorrecta_arbol_DM_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'perdida':
                    row[2],
                    'atino':
                    row[3],
                })

        #Crecimiento Arbol
            colission_analitica_query = get_crecimiento_arbol(request)
            queries.append({
                "name": 'Crecer Árbol en el tiempo',
                "query": colission_analitica_query
            })
            cursor.execute(colission_analitica_query)
            colission_analitica_quantity = cursor.fetchall()
            for row in colission_analitica_quantity:
                crecimiento_arbol_DM_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'quantity':
                    row[2]
                })

        #OTROS
            if len(col_vs_time) > 3 and len(
                    muro_hoyo_DM_quantity_response) > 0:
                colisiones_tiempo_media = colisiones_tiempo_media * 0.6
                colisiones_muro_media = (colisiones_muro_media /
                                         len(muro_hoyo_DM_quantity_response))
                colisiones_hoyo_media = (colisiones_hoyo_media /
                                         len(muro_hoyo_DM_quantity_response))

            lista_alumnos_final2.sort(key=order_list_alm, reverse=True)

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
        element_colission_alum_quantity_response = []
        posicionamiento_alu_PS_quantity_response = []
        acierto_cuida_alu_quantity_response = []
        time_PS_graf = 0
        correctas_PS_graf = 0
        move_element_graf = 0
        elementos_PS_graf = 0
        element_colission_graf = 0
        posicionamiento_PS_graf = 0
        jump_alternativas_graf = 0
        acierto_cuida_graf = 0
        completa_incompleta_PS_graf = 0
        sesiones_PS_quantity_response = []
        #analitica PS
        elementos_analitica_PS_quantity_response = []
        colission_analitica_quantity_response = []
        touch_puzzle_quantity_response = []
        nombre = []



        if reim_num == "2":

            #General
            nombre_query = get_name_student(request)
            queries.append({
                "name": 'nombre estudiante',
                "query": nombre_query
            })
            cursor.execute(nombre_query)
            nombre_quantity = cursor.fetchall()
            for row in nombre_quantity:
                nombre.append({'name': row[0]})

            sesiones_PS_query = get_time_act_co(request)
            queries.append({
                "name": 'Tiempo Actividad query',
                "query": sesiones_PS_query
            })
            cursor.execute(sesiones_PS_query)
            sesiones_PS_quantity = cursor.fetchall()
            for row in sesiones_PS_quantity:
                sesiones_PS_quantity_response.append({'id': row[0]})

            time_PS_query = get_time_act_co(request)
            queries.append({
                "name": 'Tiempo Actividad query',
                "query": time_PS_query
            })
            cursor.execute(time_PS_query)
            time_PS_quantity = cursor.fetchall()
            for row in time_PS_quantity:
                time_PS_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
        #tiempo por actividad general
            tiempoXact_query = get_tiempoact(request)
            cursor.execute(tiempoXact_query)
            queries.append({
                "name": 'TiempoXact query',
                "query": tiempoXact_query
            })
            tiempoXact_quantity = cursor.fetchall()
            for row in tiempoXact_quantity:
                tiempoXact_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })

        #CREACION
        #Elemento desplazado
            move_element_query = get_move_element_query(request)
            queries.append({
                "name": 'Desplazado query',
                "query": move_element_query
            })
            cursor.execute(move_element_query)
            move_element_quantity = cursor.fetchall()
            for row in move_element_quantity:
                move_element_quantity_response.append({
                    'id': row[0],
                    'fila': row[1],
                    'columna': row[2]
                })
                print(row[1])
                print(row[2])
        #ELEMENTOS creacion
            elementos_PS_query = get_elementos_PS(request)
            queries.append({
                "name": 'planet creacion query',
                "query": elementos_PS_query
            })
            cursor.execute(elementos_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                elementos_PS_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'planeta': row[2],
                    'planetaCS': row[3],
                    'planetaCA': row[4],
                    'estrella': row[5],
                    'supernova': row[6],
                    'nebulosa': row[7],
                    'galaxia': row[8]
                })
        #ELEMENTOS creacion analitica
            elementos_analitica_PS_query = get_elementos_alu_PS(request)
            queries.append({
                "name": 'creacion analitica query',
                "query": elementos_analitica_PS_query
            })
            cursor.execute(elementos_analitica_PS_query)
            elementos_PS_quantity = cursor.fetchall()
            for row in elementos_PS_quantity:
                elementos_analitica_PS_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'quantity':
                    row[2]
                })

        #LABERINTO
        #posicionamiento
            posicionamiento_PS_query = get_posicionamiento_PS(request)
            queries.append({
                "name": 'posicionamiento_PS query',
                "query": posicionamiento_PS_query
            })
            cursor.execute(posicionamiento_PS_query)
            posicionamiento_PS_quantity = cursor.fetchall()
            for row in posicionamiento_PS_quantity:
                posicionamiento_PS_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'tierra': row[2],
                    'neptuno': row[3],
                    'jupiter': row[4],
                    'saturno': row[5],
                    'urano': row[6],
                    'venus': row[7],
                    'mercurio': row[8],
                    'marte': row[9]
                })

        #colisiones
            element_colission_query = get_element_colission_query(request)
            queries.append({
                "name": 'colisiones query',
                "query": element_colission_query
            })
            cursor.execute(element_colission_query)
            element_colission_quantity = cursor.fetchall()
            for row in element_colission_quantity:
                element_colission_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
        #colisiones analitica
            colission_analitica_query = get_colisiones_analitica_PS(request)
            queries.append({
                "name": 'colisiones analitica query',
                "query": colission_analitica_query
            })
            cursor.execute(colission_analitica_query)
            colission_analitica_quantity = cursor.fetchall()
            for row in colission_analitica_quantity:
                colission_analitica_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
        #ALTERNATIVAS
        #saltos
            jump_alternativas_query = get_jump_alternativas_query(request)
            queries.append({
                "name": 'Saltos query',
                "query": jump_alternativas_query
            })
            cursor.execute(jump_alternativas_query)
            jump_alternativas_quantity = cursor.fetchall()
            for row in jump_alternativas_quantity:
                jump_alternativas_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
        #saltosxalumno
            jumpxalumno_query = get_jump_alternativas_alu_query(request)
            queries.append({
                "name": 'Saltosxalumno query',
                "query": jumpxalumno_query
            })
            cursor.execute(jumpxalumno_query)
            jumpxalumno_quantity = cursor.fetchall()
            for row in jumpxalumno_quantity:
                jumpxalumno_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
        #busca
        #CORRECTAS INCORRECTAS
            correctas_PS_query = get_corrects_incorrects_co(request)
            queries.append({
                "name": 'Correctas PS query',
                "query": correctas_PS_query
            })
            cursor.execute(correctas_PS_query)
            correctas_PS_quantity = cursor.fetchall()
            for row in correctas_PS_quantity:
                correctas_PS_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'correct': row[2],
                    'incorrect': row[3]
                })
    #COMPLETAS INCOMPLETAS
            completa_incompleta_PS_query = get_completa_incompleta_PS(request)
            queries.append({
                "name": 'Completas incompletas query',
                "query": completa_incompleta_PS_query
            })
            cursor.execute(completa_incompleta_PS_query)
            completa_incompleta_PS_quantity = cursor.fetchall()
            for row in completa_incompleta_PS_quantity:
                completa_incompleta_PS_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'completa':
                    row[2],
                    'incompleta':
                    row[3],
                    'inactiva':
                    row[4]
                })
    #cuida
    #acierto
            acierto_cuida_query = get_acierto_cuida_query(request)
            queries.append({
                "name": 'Acierto Cuida query',
                "query": acierto_cuida_query
            })
            cursor.execute(acierto_cuida_query)
            acierto_cuida_quantity = cursor.fetchall()
            for row in acierto_cuida_quantity:
                acierto_cuida_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
        #puzzle
            touch_puzzle_query = get_touch_analitica_query(request)
            queries.append({
                "name": 'touch puzzle query',
                "query": touch_puzzle_query
            })
            cursor.execute(touch_puzzle_query)
            touch_puzzle_quantity = cursor.fetchall()
            for row in touch_puzzle_quantity:
                touch_puzzle_quantity_response.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2]
                })
        #otros
        time_PS_graf = len(time_PS_quantity_response) * 40 + 20
        correctas_PS_graf = len(correctas_PS_quantity_response) * 40 + 100
        elementos_PS_graf = len(elementos_PS_quantity_response) * 40 + 100
        element_colission_graf = len(
            element_colission_quantity_response) * 40 + 20
        posicionamiento_PS_graf = len(
            posicionamiento_PS_quantity_response) * 40 + 100
        jump_alternativas_graf = len(
            jump_alternativas_quantity_response) * 40 + 20
        acierto_cuida_graf = len(acierto_cuida_quantity_response) * 40 + 20
        completa_incompleta_PS_graf = len(
            completa_incompleta_PS_quantity_response) * 40 + 100
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

        if reim_num == "3":
            if activity_num == "3004" or activity_num == "3002" or activity_num == "3006":
                #actividad 3004, 3002, 3006
                colision_query = get_colision_co(request)
                cursor.execute(colision_query)
                queries.append({
                    "name": 'Colision query',
                    "query": colision_query
                })
                colision_quantity = cursor.fetchall()
                #print ("colision quantity" , colision_quantity)
                for row in colision_quantity:
                    colision_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                    total_colisions += row[2]
                    countCO = countCO + 1
                if (countCO != 0):
                    promedio_colisions = total_colisions / countCO
                else:
                    promedio_colisions = total_colisions / 1
                colision_quantity_graph = len(colision_quantity) * 40 + 20

            if activity_num == "3005":
                #3005
                corrects_query = get_corrects_co(request)
                cursor.execute(corrects_query)
                queries.append({
                    "name": 'Corrects query',
                    "query": corrects_query
                })
                corrects_quantity = cursor.fetchall()
                for row in corrects_quantity:
                    corrects_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                corrects_quantity_graph = len(corrects_quantity) * 40 + 20

                jumps_query = get_jumps_co(request)
                cursor.execute(jumps_query)
                queries.append({"name": 'Jumps query', "query": jumps_query})
                jumps_quantity = cursor.fetchall()
                for row in jumps_quantity:
                    jumps_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                    total_jumps += row[2]
                    countCO = countCO + 1
                if (countCO != 0):
                    promedio_saltos = total_jumps / countCO
                else:
                    promedio_saltos = total_jumps / 1
                jumps_quantity_graph = len(jumps_quantity) * 40 + 20

            if activity_num == "3002" or activity_num == "3003" or activity_num == "3004" or activity_num == "3006" or activity_num == "3007":
                #3002 3003 3004 3006 3007
                corrects_incorrects_query = get_corrects_incorrects_co(request)
                cursor.execute(corrects_incorrects_query)
                queries.append({
                    "name": 'Correctas e incorrectas query',
                    "query": corrects_incorrects_query
                })
                corrects_incorrects_quantity = cursor.fetchall()
                for row in corrects_incorrects_quantity:
                    corrects_incorrects_quantity_response.append({
                        'id':
                        row[0],
                        'name':
                        row[1],
                        'corrects':
                        row[2],
                        'incorrects':
                        row[3]
                    })
                    total_corrects_co += row[2]
                    total_incorrects_co += row[3]
                    countCO = countCO + 1
                if (countCO != 0):
                    promedio_correctas_co = total_corrects_co / countCO
                    promedio_incorrectas_co = total_incorrects_co / countCO
                else:
                    promedio_correctas_co = total_corrects_co / 1
                    promedio_incorrectas_co = total_incorrects_co / 1
                corrects_incorrects_quantity_graph = len(
                    corrects_incorrects_quantity) * 40 + 20

            if activity_num == "0":
                # act = 0
                analytics_co_query = get_analytics_co(request)
                cursor.execute(analytics_co_query)
                queries.append({
                    "name": 'Analytics co query',
                    "query": analytics_co_query
                })
                analytics_co_quantity = cursor.fetchall()
                #print ("analytics_co_quantity", analytics_co_quantity)
                for row in analytics_co_quantity:
                    analytics_co_quantity_response.append({
                        'id':
                        row[0],
                        'name':
                        row[1],
                        'correctsact1':
                        row[2],
                        'correctsact2':
                        row[3]
                    })
                analytics_co_quantity_graph = len(
                    analytics_co_quantity) * 40 + 20

                actividades_co_query = get_cant_touch_act_co(request)
                cursor.execute(actividades_co_query)
                queries.append({
                    "name": 'Actividades CO query',
                    "query": actividades_co_query
                })
                actividades_co_quantity = cursor.fetchall()
                #print("actividades CO quantity", actividades_co_quantity)
                for row in actividades_co_quantity:
                    actividades_co_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                actividades_co_quantity_graph = len(
                    actividades_co_quantity) * 40 + 20

            if student_num != "0":
                #student =!0
                exit_lab_query = get_exit_lab(request)
                cursor.execute(exit_lab_query)
                queries.append({
                    "name": 'Exit lab query',
                    "query": exit_lab_query
                })
                exit_lab_quantity = cursor.fetchall()
                for row in exit_lab_quantity:
                    exit_lab_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                exit_lab_quantity_graph = len(exit_lab_quantity) * 40 + 20

                touch_trash_co_query = get_touch_trash_co(request)
                cursor.execute(touch_trash_co_query)
                queries.append({
                    "name": 'Touch trash co query',
                    "query": touch_trash_co_query
                })
                touch_trash_co_quantity = cursor.fetchall()
                #print ("Touch trash co quantity" , touch_trash_co_quantity)
                for row in touch_trash_co_quantity:
                    touch_trash_co_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                touch_trash_co_quantity_graph = len(
                    touch_trash_co_quantity) * 40 + 20

                # student=! 0
                #correctas e incorrectas para c/ alumno x actividad
                corrects_student_co_query = get_corrects_student_co(request)
                cursor.execute(corrects_student_co_query)
                queries.append({
                    "name": 'Corrects students CO query',
                    "query": corrects_student_co_query
                })
                corrects_student_co_quantity = cursor.fetchall()
                #print ("Corrects students CO quantity" , corrects_student_co_quantity)
                for row in corrects_student_co_quantity:
                    corrects_student_co_quantity_response.append({
                        'id':
                        row[0],
                        'name':
                        row[1],
                        'correct':
                        row[2],
                        'incorrect':
                        row[3]
                    })
                corrects_student_co_quantity_graph = len(
                    corrects_student_co_quantity) * 40 + 20

            # touch_animals_co_query = get_touch_animals_co(request)
            # cursor.execute(touch_animals_co_query)
            # queries.append({"name": 'Touch animals co query', "query": touch_animals_co_query})
            # touch_animals_co_quantity = cursor.fetchall()
            # #print ("Touch animals co quantity" , touch_animals_co_quantity)
            # for row in touch_animals_co_quantity:
            #     touch_animals_co_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            if activity_num == "3002":
                colision_trash_query = get_colision_trash(request)
                cursor.execute(colision_trash_query)
                queries.append({
                    "name": 'Colision trash query',
                    "query": colision_trash_query
                })
                colision_trash_quantity = cursor.fetchall()
                #print("Colision trash quantity", colision_trash_quantity)
                for row in colision_trash_quantity:
                    colision_trash_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                colision_trash_quantity_graph = len(
                    colision_trash_quantity) * 40 + 20

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
                queries.append({
                    "name": 'Exits lab co query',
                    "query": exits_lab_co_query
                })
                exits_lab_co_quantity = cursor.fetchall()
                #print ("Exits lab co quantity" , exits_lab_co_quantity)
                for row in exits_lab_co_quantity:
                    exits_lab_co_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                exits_lab_co_quantity_graph = len(
                    exits_lab_co_quantity) * 40 + 20

            if activity_num == "3000":
                # act 3000
                touch_all_trash_query = get_touch_all_trash(request)
                cursor.execute(touch_all_trash_query)
                queries.append({
                    "name": 'Touch all trash query',
                    "query": touch_all_trash_query
                })
                touch_all_trash_quantity = cursor.fetchall()
                #print ("Touch all trash quantity" , touch_all_trash_quantity)
                for row in touch_all_trash_quantity:
                    touch_all_trash_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                touch_all_trash_quantity_graph = len(
                    touch_all_trash_quantity) * 40 + 20

            if activity_num != "0":
                #3000 3001 3002 3003 3004 3005 3006 3007
                buttons_co_query = get_buttons_co(request)
                cursor.execute(buttons_co_query)
                queries.append({
                    "name": 'Buttons CO query',
                    "query": buttons_co_query
                })
                buttons_co_quantity = cursor.fetchall()
                #print ("Buttons CO quantity" , buttons_co_quantity)
                for row in buttons_co_quantity:
                    buttons_co_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                buttons_co_quantity_graph = len(buttons_co_quantity) * 40 + 20

            if activity_num == "3007":
                trash_clean_co_query = get_trash_clean_co(request)
                cursor.execute(trash_clean_co_query)
                queries.append({
                    "name": 'Trash clean CO query',
                    "query": trash_clean_co_query
                })
                trash_clean_co_quantity = cursor.fetchall()
                #print ("Trash clean CO quantity" , trash_clean_co_quantity)
                for row in trash_clean_co_quantity:
                    trash_clean_co_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                trash_clean_co_quantity_graph = len(
                    trash_clean_co_quantity) * 40 + 20

            if activity_num != "3000" and activity_num != "3001" and activity_num != "0":
                time_act_co_query = get_time_act_co(request)
                cursor.execute(time_act_co_query)
                queries.append({
                    "name": 'Time act CO query',
                    "query": time_act_co_query
                })
                time_act_co_quantity = cursor.fetchall()
                #print ("Time act CO quantity" , time_act_co_quantity)
                for row in time_act_co_quantity:
                    time_act_co_quantity_response.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2]
                    })
                time_act_co_quantity_graph = len(
                    time_act_co_quantity) * 40 + 20

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

        if reim_num == "77":
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

                    lista_actividad = [[7705, 50], [7706, 50], [7707, 50],
                                       [7708, 65], [7709, 70], [7710, 80]]
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

                        if (tipo_grafico == 1):
                            print('\n\nAlumno', alumno["id"], ' nombre: ',
                                  alumno["name"])
                            queryXactividad = get_figura_simple_estandar_por_curso(
                                request, actividad_77, alumno["id"])
                            #print("ESTANDAR")
                        if (tipo_grafico == 2):
                            queryXactividad = get_figura_simple_promedio_por_curso(
                                request, actividad_77, alumno["id"])
                            #print("PROMEDIO")
                        if (tipo_grafico == 3):
                            queryXactividad = get_figura_simple_ultimos_registros_por_curso(
                                request, actividad_77, alumno["id"])
                            #print("FINAL")
                        cursor.execute(queryXactividad)
                        queries.append({
                            "name": 'TiempoXact query',
                            "query": queryXactividad
                        })
                        resultado_query = cursor.fetchall()
                        for row in resultado_query:

                            if (len(row[5]) > 0):
                                nombre_alumno = row[5]
                                #print("nombre: " + nombre_alumno)
                            nombre_actividad = row[4]
                            if (contador_tiempo == 0):
                                contador_tiempo += 1
                                rango_tiempo = row[2]
                                fecha_inicial = rango_tiempo + timedelta(
                                    seconds=actividad_77[1])
                                try:
                                    if (int(request.GET.get('rango')) != 0):
                                        valor = actividad_77[1] + (
                                            (actividad_77[1] *
                                             int(request.GET.get('rango'))) /
                                            100)
                                        #print("VALOR: ", valor)
                                        fecha_inicial = rango_tiempo + timedelta(
                                            seconds=valor)
                                except:
                                    valor = actividad_77[1] + (
                                        (actividad_77[1] * int("50")) / 100)
                                    #print("VALOR: ", valor)
                                    fecha_inicial = rango_tiempo + timedelta(
                                        seconds=valor)
                            #print("\n\n\n\nFECHA INICIAL: ",fecha_inicial, " Nombre: ", actividad_77[0], " Segundos: ", actividad_77[1])
                            #print("Contador 1: ", contador_complejo_1)
                            #print(row[1]," == 7728 and ", contador_complejo_1, " == 0 and correcta ", row[3], " == 1 and ", row[2], " <= " , fecha_inicial )
                            if (row[1] == 7728 and contador_complejo_1 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                #print("Entro actividad 7728 7705")
                                contador_complejo_1 += 1
                                completada_total += 1
                            if (row[1] == 7729 and contador_complejo_2 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                #print("Entro actividad 7729 7705")
                                completada_total += 1
                                contador_complejo_2 += 1
                            if (row[1] == 7730 and contador_complejo_3 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                completada_total += 1
                                contador_complejo_3 += 1
                            if (row[1] == 7731 and contador_complejo_4 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                completada_total += 1
                                contador_complejo_4 += 1
                            if (row[1] == 7732 and contador_complejo_5 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                completada_total += 1
                                contador_complejo_5 += 1
                            if (row[1] == 7733 and contador_complejo_6 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                completada_total += 1
                                contador_complejo_6 += 1
                            if (row[1] == 7734 and contador_complejo_7 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                completada_total += 1
                                contador_complejo_7 += 1
                            if (row[1] == 7735 and contador_complejo_8 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                completada_total += 1
                                contador_complejo_8 += 1
                            if (row[1] == 7736 and contador_complejo_9 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                completada_total += 1
                                contador_complejo_9 += 1
                            if (row[1] == 7737 and contador_complejo_10 == 0
                                    and row[3] == 1
                                    and row[2] <= fecha_inicial):
                                completada_total += 1
                                contador_complejo_10 += 1
                        if (int(completada_total) < 10
                                and len(nombre_actividad) != 0):
                            total_incompletas = (10 - completada_total)
                            actividad_1_volcan.append({
                                'name':
                                nombre_actividad,
                                'completada':
                                completada_total,
                                'no_completada':
                                total_incompletas
                            })

                        Total_Completas_Actividad += completada_total

                    Nombre_Estilo_Cognitivo = ''
                    if (Total_Completas_Actividad > 0
                            and Total_Completas_Actividad < 11):
                        Nombre_Estilo_Cognitivo = 'Muy Dependiente del Campo'
                        color_base = '(119,170,255)'
                        lista_alumno_cognitivo_muy_dependiente.append({
                            'alumno':
                            nombre_alumno,
                            'name':
                            Nombre_Estilo_Cognitivo,
                            'cantidad':
                            Total_Completas_Actividad
                        })
                    if (Total_Completas_Actividad > 10
                            and Total_Completas_Actividad < 21):
                        Nombre_Estilo_Cognitivo = 'Dependiente del Campo'
                        color_base = '(153,204,255)'
                        lista_alumno_cognitivo_dependiente.append({
                            'alumno':
                            nombre_alumno,
                            'name':
                            Nombre_Estilo_Cognitivo,
                            'cantidad':
                            Total_Completas_Actividad
                        })
                    if (Total_Completas_Actividad > 20
                            and Total_Completas_Actividad < 31):
                        Nombre_Estilo_Cognitivo = 'Intermedio del Campo'
                        color_base = '(187,238,255)'
                        lista_alumno_cognitivo_intermedio.append({
                            'alumno':
                            nombre_alumno,
                            'name':
                            Nombre_Estilo_Cognitivo,
                            'cantidad':
                            Total_Completas_Actividad
                        })
                    if (Total_Completas_Actividad > 30
                            and Total_Completas_Actividad < 41):
                        Nombre_Estilo_Cognitivo = 'Independiente del Campo'
                        color_base = 'rgb(85,136,255)'
                        lista_alumno_cognitivo_independiente.append({
                            'alumno':
                            nombre_alumno,
                            'name':
                            Nombre_Estilo_Cognitivo,
                            'cantidad':
                            Total_Completas_Actividad
                        })
                    if (Total_Completas_Actividad > 40
                            and Total_Completas_Actividad < 51):
                        Nombre_Estilo_Cognitivo = 'Muy Dependiente del Campo'
                        color_base = '(51,102,255)'
                        lista_alumno_cognitivo_muy_independiente.append({
                            'alumno':
                            nombre_alumno,
                            'name':
                            Nombre_Estilo_Cognitivo,
                            'cantidad':
                            Total_Completas_Actividad
                        })
                    #print("Nombre: ", nombre_alumno)

                    if (len(nombre_alumno) > 0):
                        lista_alumno_cognitivo.append({
                            'alumno': nombre_alumno,
                            'name': Nombre_Estilo_Cognitivo,
                            'cantidad': Total_Completas_Actividad,
                            'color': color_base
                        })

                    nombre_alumno = ''
                    Nombre_Estilo_Cognitivo = ''
                    Total_Completas_Actividad = 0
                    completada_total = 0
                    #print('\n\nAlumno', nombre_alumno,' Nomnre', Nombre_Estilo_Cognitivo, 'Cantidad: ', Total_Completas_Actividad )
                    #

            #----------------------por CURSO----------------------------- 22

        #---------------------------------por alumno---------------------------------------------------
            if request.GET.get(
                    'student') and request.GET.get('student') != '0':
                print("\n\n\nPASOS")
                lista_actividad = [[7705, 50], [7706, 50], [7707, 50],
                                   [7708, 65], [7709, 70], [7710, 80]]
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

                    if (tipo_grafico == 1):
                        queryXactividad = get_figura_simple_volcan(
                            request, actividad_77)
                        print("ESTANDAR")
                    if (tipo_grafico == 2):
                        queryXactividad = get_figura_simple_promedio(
                            request, actividad_77)
                        print("PROMEDIO")
                    if (tipo_grafico == 3):
                        queryXactividad = get_figura_simple_ultimos_registros(
                            request, actividad_77)
                        print("FINAL")
                    cursor.execute(queryXactividad)
                    queries.append({
                        "name": 'TiempoXact query',
                        "query": queryXactividad
                    })
                    resultado_query = cursor.fetchall()
                    for row in resultado_query:

                        if (len(row[5]) > 0):
                            nombre_alumno = row[5]
                        nombre_actividad = row[4]
                        if (contador_tiempo == 0):
                            contador_tiempo += 1
                            rango_tiempo = row[2]
                            fecha_inicial = rango_tiempo + timedelta(
                                seconds=actividad_77[1])
                            if (int(request.GET.get('rango')) != 0):
                                valor = actividad_77[1] + (
                                    (actividad_77[1] *
                                     int(request.GET.get('rango'))) / 100)
                                #print("VALOR: ", valor)
                                fecha_inicial = rango_tiempo + timedelta(
                                    seconds=valor)
                        print("\n\n\n\nFECHA INICIAL: ", fecha_inicial,
                              " Nombre: ", actividad_77[0], " Segundos: ",
                              actividad_77[1])
                        #print("Contador 1: ", contador_complejo_1)
                        #print(row[1]," == 7728 and ", contador_complejo_1, " == 0 and correcta ", row[3], " == 1 and ", row[2], " <= " , fecha_inicial )
                        if (row[1] == 7728 and contador_complejo_1 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            print("Entro actividad 7728 7705")
                            contador_complejo_1 += 1
                            completada_total += 1
                        if (row[1] == 7729 and contador_complejo_2 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            print("Entro actividad 7729 7705")
                            completada_total += 1
                            contador_complejo_2 += 1
                        if (row[1] == 7730 and contador_complejo_3 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            completada_total += 1
                            contador_complejo_3 += 1
                        if (row[1] == 7731 and contador_complejo_4 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            completada_total += 1
                            contador_complejo_4 += 1
                        if (row[1] == 7732 and contador_complejo_5 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            completada_total += 1
                            contador_complejo_5 += 1
                        if (row[1] == 7733 and contador_complejo_6 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            completada_total += 1
                            contador_complejo_6 += 1
                        if (row[1] == 7734 and contador_complejo_7 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            completada_total += 1
                            contador_complejo_7 += 1
                        if (row[1] == 7735 and contador_complejo_8 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            completada_total += 1
                            contador_complejo_8 += 1
                        if (row[1] == 7736 and contador_complejo_9 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            completada_total += 1
                            contador_complejo_9 += 1
                        if (row[1] == 7737 and contador_complejo_10 == 0
                                and row[3] == 1 and row[2] <= fecha_inicial):
                            completada_total += 1
                            contador_complejo_10 += 1
                    if (int(completada_total) < 10
                            and len(nombre_actividad) != 0):
                        total_incompletas = (10 - completada_total)
                        actividad_1_volcan.append({
                            'name':
                            nombre_actividad,
                            'completada':
                            completada_total,
                            'no_completada':
                            total_incompletas
                        })

                    Total_Completas_Actividad += completada_total

                Nombre_Estilo_Cognitivo = ''
                if (Total_Completas_Actividad > 0
                        and Total_Completas_Actividad < 11):
                    Nombre_Estilo_Cognitivo = 'Muy Dependiente'
                    nombre_estilo_cognitivo_alumno = 'Muy Dependiente del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })
                if (Total_Completas_Actividad > 10
                        and Total_Completas_Actividad < 21):
                    Nombre_Estilo_Cognitivo = 'Dependiente'
                    nombre_estilo_cognitivo_alumno = 'Dependiente del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })
                if (Total_Completas_Actividad > 20
                        and Total_Completas_Actividad < 31):
                    Nombre_Estilo_Cognitivo = 'Intermedio'
                    nombre_estilo_cognitivo_alumno = 'Intermedio del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })
                if (Total_Completas_Actividad > 30
                        and Total_Completas_Actividad < 41):
                    Nombre_Estilo_Cognitivo = 'Independiente'
                    nombre_estilo_cognitivo_alumno = 'Independiente del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })
                if (Total_Completas_Actividad > 40
                        and Total_Completas_Actividad < 51):
                    Nombre_Estilo_Cognitivo = 'Muy Dependiente'
                    nombre_estilo_cognitivo_alumno = 'Muy Independiente del Campo'
                    #Estilo_cognitivo_por_niño.append({'alumno': nombre_alumno,'name': Nombre_Estilo_Cognitivo, 'quantity': Total_Completas_Actividad })

                Estilo_cognitivo_por_niño.append({
                    'alumno':
                    nombre_alumno,
                    'name':
                    Nombre_Estilo_Cognitivo,
                    'quantity':
                    Total_Completas_Actividad
                })

            #----------------------por alumno----------------------------- 22
            if request.GET.get(
                    'student') and request.GET.get('student') != '0':
                buenas_malas = get_Actividad_Buenas_Mala(request)
                cursor.execute(buenas_malas)
                queries.append({
                    "name": 'TiempoXact query',
                    "query": buenas_malas
                })
                tiempoXact_quantity = cursor.fetchall()
                for row in tiempoXact_quantity:
                    nombre_actividad = row[7]
                    nombre_actividad = nombre_actividad.replace(
                        "Btn-Aceptar-Figura-", "Figura Compleja ")
                    buenas_malas_x_figura_compleja.append({
                        'name': nombre_actividad,
                        'completa': row[4],
                        'no_completa': row[5]
                    })

            #--------------------------------------------------- 33
            if request.GET.get(
                    'student') and request.GET.get('student') != '0':
                tiem_acti_sesion = get_tiempoact_sesion(request)
                cursor.execute(tiem_acti_sesion)
                queries.append({
                    "name": 'TiempoXact query',
                    "query": tiem_acti_sesion
                })
                tiempoXact_quantity = cursor.fetchall()
                for row in tiempoXact_quantity:
                    tiempoxactxsesion.append({
                        'name': row[1],
                        'quantity': row[2]
                    })

            #--------------------------------------------------- 33
            #Estilo_cognitivo_por_niño.append({'name': Nombre_Estilo_Cognitivo, 'quantity': Valor_Total_Figuras_complejas })

        #TAMAÑO GRAFICOS
        time_ps_query_77 = len(tiempo_x_actividad_response) * 40 + 20
        identificar_estilo_cognitivo = len(
            identificar_estilo_cognitivo_response) * 40 + 20
        tamaño_curso = len(lista_alumno_cognitivo) * 40 + 20
        tamaña_grafico_por_alumno = len(actividad_1_volcan) * 40 + 20
        tamaña_grafico_por_actividad = len(
            buenas_malas_x_figura_compleja) * 40 + 20

        print("Tamaño: ", tamaño_curso)
        for item in lista_alumno_cognitivo:
            print("Nombre: ", item["alumno"], "item: ", item["cantidad"],
                  "Estilo del campo: ", item["name"])


#FIN REIM ID = 77, NOMBRE = BUSCANDO EL TESORO PERDIDO

        # INICIO Reciclando Construyo ---
        porcentaje_llave_quantity_response = []
        promedio_intentos_response = []
        promedio_intentos_totales_response = []
        elementos_reciclados_usuario_response = []
        elementos_reciclados_usuario_incorrecto_response = []
        Respuestas_Usuario_VencerAlConstructorresponse = []
        ElementosRecicladosGeneral_tipo_response = []
        ElementosRecicladosGeneralIncorrectamente_tipo_response = []
        Llave_tipo_response = []
        Respuestas_General_VencerAlConstructor_response = []
        Historial_Respuestas_response = []
        Historial_Respuestas_Anexar_response = []
        Historial_Respuestas_Dividir_response = []
        Historial_movimientos_response = []
        Historial_movimientos_Sol_response = []
        Historial_movimientos_Nube_response = []
        Historial_movimientos_Triangulo_response = []
        tiempo_size = 0;
        Llave_tipo_size = 0;

        if reim_num=="201":
            Llave_tipo_query = get_llave_Tipo(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'porcentaje llave query', "query": Llave_tipo_query})
            cursor.execute(Llave_tipo_query)
            Llave_tipo_query = cursor.fetchall()

            for row in Llave_tipo_query:
                Llave_tipo_response.append({ 'name': row[0], 'Total': row[1], 'Incorrectas': row[2] , 'Correctas': row[3] })
            Llave_tipo_size = len(Llave_tipo_response)*40+20;

            Respuestas_General_VencerAlConstructor_query = get_Respuestas_General_VencerAlConstructor(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'porcentaje llave query', "query": Respuestas_General_VencerAlConstructor_query})
            cursor.execute(Respuestas_General_VencerAlConstructor_query)
            Respuestas_General_VencerAlConstructor_query = cursor.fetchall()

            for row in Respuestas_General_VencerAlConstructor_query:
                Respuestas_General_VencerAlConstructor_response.append({ 'name': row[0], 'Total': row[4], 'Incorrectas': row[5] , 'Correctas': row[6] })

            get_Historial_Respuestas_query = get_Historial_Respuestas(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'Historial Respuestas', "query": get_Historial_Respuestas_query})
            cursor.execute(get_Historial_Respuestas_query)
            get_Historial_Respuestas_query = cursor.fetchall()

            for row in get_Historial_Respuestas_query:
                Historial_Respuestas_response.append({ 'name': row[0], 'Total': row[4], 'Incorrectas': row[5] , 'Correctas': row[6], 'Fecha': row[7] })

            get_Historial_Respuestas_Anexar_query = get_Historial_Respuestas_Anexar(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'Historial Respuestas Anexar', "query": get_Historial_Respuestas_Anexar_query})
            cursor.execute(get_Historial_Respuestas_Anexar_query)
            get_Historial_Respuestas_Anexar_query = cursor.fetchall()

            for row in get_Historial_Respuestas_Anexar_query:
                Historial_Respuestas_Anexar_response.append({ 'name': row[0], 'Total': row[4], 'Incorrectas': row[5] , 'Correctas': row[6], 'Fecha': row[7] })

            get_Historial_Respuestas_Dividir_query = get_Historial_Respuestas_Dividir(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'Historial Respuestas Anexar', "query": get_Historial_Respuestas_Dividir_query})
            cursor.execute(get_Historial_Respuestas_Dividir_query)
            get_Historial_Respuestas_Dividir_query = cursor.fetchall()

            for row in get_Historial_Respuestas_Dividir_query:
                Historial_Respuestas_Dividir_response.append({ 'name': row[0], 'Total': row[4], 'Incorrectas': row[5] , 'Correctas': row[6], 'Fecha': row[7] })


            get_Historial_movimientos_query = get_Historial_movimientos(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'Historial Movimientos', "query": get_Historial_movimientos_query})
            cursor.execute(get_Historial_movimientos_query)
            get_Historial_movimientos_query = cursor.fetchall()

            for row in get_Historial_movimientos_query:
                Historial_movimientos_response.append({ 'name': row[0], 'Total': row[4], 'Incorrectas': row[5] , 'Correctas': row[6], 'Fecha': row[7] })

            get_Historial_movimientos_Sol_query = get_Historial_movimientos_Sol(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'Historial Movimientos Sol', "query": get_Historial_movimientos_Sol_query})
            cursor.execute(get_Historial_movimientos_Sol_query)
            get_Historial_movimientos_Sol_query = cursor.fetchall()

            for row in get_Historial_movimientos_Sol_query:
                Historial_movimientos_Sol_response.append({ 'name': row[0], 'Total': row[4], 'Incorrectas': row[5] , 'Correctas': row[6], 'Fecha': row[7] })

            get_Historial_movimientos_Nube_query = get_Historial_movimientos_Nube(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'Historial Movimientos Sol', "query": get_Historial_movimientos_Nube_query})
            cursor.execute(get_Historial_movimientos_Nube_query)
            get_Historial_movimientos_Nube_query = cursor.fetchall()

            for row in get_Historial_movimientos_Nube_query:
                Historial_movimientos_Nube_response.append({ 'name': row[0], 'Total': row[4], 'Incorrectas': row[5] , 'Correctas': row[6], 'Fecha': row[7] })

            get_Historial_movimientos_Triangulo_query = get_Historial_movimientos_Triangulo(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'Historial Movimientos Sol', "query": get_Historial_movimientos_Triangulo_query})
            cursor.execute(get_Historial_movimientos_Triangulo_query)
            get_Historial_movimientos_Triangulo_query = cursor.fetchall()

            for row in get_Historial_movimientos_Triangulo_query:
                Historial_movimientos_Triangulo_response.append({ 'name': row[0], 'Total': row[4], 'Incorrectas': row[5] , 'Correctas': row[6], 'Fecha': row[7] })


            ElementosRecicladosGeneral_tipo_query = get_ElementosRecicladosCorrectamente_Tipo(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'porcentaje llave query', "query": ElementosRecicladosGeneral_tipo_query})
            cursor.execute(ElementosRecicladosGeneral_tipo_query)
            ElementosRecicladosGeneral_tipo_query = cursor.fetchall()

            for row in ElementosRecicladosGeneral_tipo_query:
                ElementosRecicladosGeneral_tipo_response.append({ 'id': row[0], 'Tipo': row[1], 'cantidad': row[2] })


            ElementosRecicladosGeneralIncorrectamente_tipo_query = get_ElementosRecicladosIncorrectamente_Tipo(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'porcentaje llave query', "query": ElementosRecicladosGeneralIncorrectamente_tipo_query})
            cursor.execute(ElementosRecicladosGeneralIncorrectamente_tipo_query)
            ElementosRecicladosGeneralIncorrectamente_tipo_query = cursor.fetchall()

            for row in ElementosRecicladosGeneralIncorrectamente_tipo_query:
                ElementosRecicladosGeneralIncorrectamente_tipo_response.append({ 'id': row[0], 'Tipo': row[1], 'cantidad': row[2] })

            #Porcentaje_Llaves
            Respuestas_Usuario_VencerAlConstructor_query = get_Respuestas_Usuario_VencerAlConstructor(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'Respuestas Vencer al constructor', "query": Respuestas_Usuario_VencerAlConstructor_query})
            cursor.execute(Respuestas_Usuario_VencerAlConstructor_query)
            Respuestas_Usuario_VencerAlConstructor_query = cursor.fetchall()

            for row in Respuestas_Usuario_VencerAlConstructor_query:

                Respuestas_Usuario_VencerAlConstructorresponse.append({ 'id': row[0], 'CantidadTotal': row[2], 'Incorrectas': row[3], 'Correctas': row[4]})

            #Porcentaje_Llaves
            porcentaje_llave_query = get_porcentaje_llave(request)
            #print(porcentaje_llave_query)
            queries.append({"name": 'porcentaje llave query', "query": porcentaje_llave_query})
            cursor.execute(porcentaje_llave_query)
            porcentaje_llave_query = cursor.fetchall()
            for row in porcentaje_llave_query:
                porcentaje_llave_quantity_response.append({ 'id': row[0], 'name': row[0], 'porcentaje': row[1] })
            #promedio_intentos_satisfactorios
            promedio_intentos_query = get_promedio_intentos(request)
            queries.append({"name": 'promedio intentos query', "query": promedio_intentos_query})
            cursor.execute(promedio_intentos_query)
            promedio_intentos_query = cursor.fetchall()
            for row in promedio_intentos_query:
                promedio_intentos_response.append({ 'id': row[0], 'name': row[0], 'promedio': row[1] })
            #promedio_intentos_totales
            promedio_intentos_totales_query = get_promedio_intentos_totales(request)
            queries.append({"name": 'promedio intentos totales query', "query": promedio_intentos_totales_query})
            cursor.execute(promedio_intentos_totales_query)
            #print(promedio_intentos_totales_query)
            promedio_intentos_totales_query = cursor.fetchall()
            for row in promedio_intentos_totales_query:
                promedio_intentos_totales_response.append({ 'id': row[0], 'name': row[0], 'promedio': row[1] })


            elementos_reciclados_usuario_query = get_elementos_reciclados_usuario(request)
            queries.append({"name": 'elementos reciclados query', "query": elementos_reciclados_usuario_query})
            cursor.execute(elementos_reciclados_usuario_query)
            elementos_reciclados_usuario_query = cursor.fetchall()
            for row in elementos_reciclados_usuario_query:
                elementos_reciclados_usuario_response.append({'nombre': row[0], 'cantidad': row[1], 'nombreElemento': row[2]})

            elementos_reciclados_usuario_incorrecto_query = get_elementos_reciclados_incorrecto_usuario(request)
            queries.append({"name": 'elementos reciclados incorrecto query', "query": elementos_reciclados_usuario_incorrecto_query})
            cursor.execute(elementos_reciclados_usuario_incorrecto_query)
            elementos_reciclados_usuario_incorrecto_query = cursor.fetchall()
            for row in elementos_reciclados_usuario_incorrecto_query:
                elementos_reciclados_usuario_incorrecto_response.append(
                    {'nombre': row[0], 'cantidad': row[1], 'nombreElemento': row[2]})

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
            tiempo_size = len(time_PS_quantity) * 40 + 20;

            #tiempo por actividad general
            tiempoXact_query = get_tiempoact(request)
            cursor.execute(tiempoXact_query)
            queries.append({"name": 'TiempoXact query', "query": tiempoXact_query})
            tiempoXact_quantity = cursor.fetchall()
            #print("tiempoXact quantity", tiempoXact_quantity)
            for row in tiempoXact_quantity:
                tiempoXact_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })


        # FIN Reciclando Construyo ---

        ################################################################
        ############################RECICLANDO##########################
        #################################################################
        

        #List Querys
        touch_all_act206_quantity_response = []
        time_act_RCO_quantity_response = []
        time_act_RCOTotal_quantity_response = []
        corrects_incorrects_quantity_response = []
        corrects_quantity_response = []
        incorrects_quantity_response = []
        corrects_student_RCO_quantity_response = []
        completa_incompleta_RCO_quantity_response = []
        analytics1_1_co_quantity_act_3_response=[]
        analytics1_co_quantity_act_3_response=[]
        posicionamiento_RCO_quantity_response = []
        get_OA_Desafios_RCO_quantity_response = []
        get_OA2_Desafios_RCO_quantity_response = []
        get_OA2_2_Desafios_RCO_quantity_response = []
        get_OA3_Desafios_RCO_quantity_response = []
        get_OA3_2_Desafios_RCO_quantity_response = []
        get_OA4_Desafios_RCO_quantity_response = []
        get_OA4_2_Desafios_RCO_quantity_response = []
        get_OA5_Desafios_RCO_quantity_response = []
        get_OA5_2_Desafios_RCO_quantity_response = []
        get_victorias_Desafios_RCO_quantity_response = []
        get_derrotas_Desafios_RCO_quantity_response = []
        get_mov_multi_RCO_quantity_response = []
        touch_all_OA1Bien_quantity_response = []
        elementos_analitica_RCO_quantity_response = []
        #Promedios
        countRCO = 0
        promedio_correctas_RCO = 0
        promedio_incorrectas_RCO = 0
        total_corrects_RCO = 0
        total_incorrects_RCO = 0
        #Size Graphs
        touch_all_act206_quantity_graph = 0
        time_act_RCO_quantity_graph = 0
        time_act_RCOTotal_quantity_graph = 0
        corrects_quantity_graph = 0
        corrects_incorrects_quantity_graph = 0
        posicionamiento_RCO_graf = 0
        get_OA_Desafios_RCO_graf = 0
        get_OA2_Desafios_RCO_graf = 0
        get_OA2_2_Desafios_RCO_graf = 0
        get_OA3_Desafios_RCO_graf = 0
        get_OA3_2_Desafios_RCO_graf = 0
        get_OA4_Desafios_RCO_graf = 0
        get_OA4_2_Desafios_RCO_graf = 0
        get_OA5_Desafios_RCO_graf = 0
        get_OA5_2_Desafios_RCO_graf = 0
        get_victorias_Desafios_RCO_graf = 0
        get_derrotas_Desafios_RCO_graf = 0
        get_mov_multi_RCO_graf = 0        
        touch_all_OA1Bien_quantity_graph = 0

        if reim_num=="206":
            if activity_num=="9004":
                # act 3000
                touch_all_act206_query = get_touch_all_act206(request)
                cursor.execute(touch_all_act206_query)
                queries.append({"name": 'Touch all act206 query', "query": touch_all_act206_query})
                touch_all_act206_quantity = cursor.fetchall()
                #print ("Touch all trash quantity" , touch_all_trash_quantity)
                for row in touch_all_act206_quantity:
                    touch_all_act206_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                touch_all_act206_quantity_graph = len(touch_all_act206_quantity)*40+20
            
            if activity_num!="3000" and activity_num!="3001" and activity_num!="0":
                time_act_RCO_query = get_time_act_RCO(request)
                cursor.execute(time_act_RCO_query)
                queries.append({"name": 'Time act RCO query', "query": time_act_RCO_query})
                time_act_RCO_quantity = cursor.fetchall()
                #print ("Time act RCO quantity" , time_act_RCO_quantity)
                for row in time_act_RCO_quantity:
                    time_act_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                time_act_RCO_quantity_graph = len(time_act_RCO_quantity)*40+20
            
            #########################################################
            if activity_num=="0":
                time_act_RCOTotal_query = get_time_act_RCOTotal(request)
                cursor.execute(time_act_RCOTotal_query)
                queries.append({"name": 'Time act RCOTotal query', "query": time_act_RCOTotal_query})
                time_act_RCOTotal_quantity = cursor.fetchall()
                #print ("Time act RCOTotal quantity" , time_act_RCOTotal_quantity)
                for row in time_act_RCOTotal_quantity:
                    time_act_RCOTotal_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                time_act_RCOTotal_quantity_graph = len(time_act_RCOTotal_quantity)*40+20
            #########################################################

            if activity_num=="9000" or activity_num=="9001" or activity_num=="9002" or activity_num=="9009" or activity_num=="9010":
                #9000 9001 9002 9009 9010
                corrects_incorrects_query = get_corrects_incorrects_RCO(request)
                cursor.execute(corrects_incorrects_query)
                queries.append({"name": 'Correctas e incorrectas query', "query": corrects_incorrects_query})
                corrects_incorrects_quantity = cursor.fetchall()
                for row in corrects_incorrects_quantity:
                    corrects_incorrects_quantity_response.append({ 'id': row[0], 'name': row[1], 'corrects': row[2], 'incorrects': row[3] })
                    total_corrects_RCO += row[2]
                    total_incorrects_RCO += row[3]
                    countRCO = countRCO+1
                if (countRCO!=0):
                    promedio_correctas_RCO = total_corrects_RCO / countRCO
                    promedio_incorrectas_RCO = total_incorrects_RCO / countRCO
                else:
                    promedio_correctas_RCO = total_corrects_RCO / 1
                    promedio_incorrectas_RCO = total_incorrects_RCO / 1
                corrects_incorrects_quantity_graph = len(corrects_incorrects_quantity)*40+20
            
            #COMPLETAS INCOMPLETAS
            completa_incompleta_RCO_query = get_completa_incompleta_RCO(request)
            queries.append({"name": 'Completas incompletas query', "query": completa_incompleta_RCO_query})
            cursor.execute(completa_incompleta_RCO_query)
            completa_incompleta_RCO_quantity = cursor.fetchall()
            for row in completa_incompleta_RCO_quantity:
                completa_incompleta_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'completa': row[2], 'incompleta': row[3], 'inactiva': row[4] })

            analytics1_1_co_query = get_analytics1_1_co_act_3(request)
            cursor.execute(analytics1_1_co_query)
            queries.append({"name": 'Analytics1_1 co query', "query": analytics1_1_co_query})
            analytics1_1_co_quantity_act_3 = cursor.fetchall()
            #print ("analytics1_co_quantity_act_3", analytics1_co_quantity_act_3)
            for row in analytics1_1_co_quantity_act_3:
                analytics1_1_co_quantity_act_3_response.append({ 'id': row[0], 'name': row[1], 'act1': row[2], 'act2': row[3], 'act3': row[4], 'act4': row[5]  })
            
            analytics1_co_query = get_analytics1_co_act_3(request)
            cursor.execute(analytics1_co_query)
            queries.append({"name": 'Analytics1 co query', "query": analytics1_co_query})
            analytics1_co_quantity_act_3 = cursor.fetchall()
            #print ("analytics1_co_quantity_act_3", analytics1_co_quantity_act_3)
            for row in analytics1_co_quantity_act_3:
                analytics1_co_quantity_act_3_response.append({ 'id': row[0], 'name': row[1], 'act1': row[2], 'act2': row[3], 'act3': row[4], 'act4': row[5]  })
            
            #LABERINTO
            #posicionamiento
            posicionamiento_RCO_query = get_posicionamiento_RCO(request)
            queries.append({"name": 'posicionamiento_RCO query', "query": posicionamiento_RCO_query})
            cursor.execute(posicionamiento_RCO_query)
            posicionamiento_RCO_quantity = cursor.fetchall()
            for row in posicionamiento_RCO_quantity:
                posicionamiento_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'a_metal': row[2], 'desa_metal': row[3], 'a_carton': row[4], 'desa_carton': row[5], 'a_plastico': row[6], 'desa_plastico': row[7], 'a_vidrio': row[8], 'desa_vidrio': row[9] })

            #otros
            posicionamiento_RCO_graf = len(posicionamiento_RCO_quantity_response) * 40+100

            #get_OA_Desafios22
            get_OA_Desafios_RCO_query = get_OA_Desafios_RCO(request)
            queries.append({"name": 'get_OA_Desafios_RCO query', "query": get_OA_Desafios_RCO_query})
            cursor.execute(get_OA_Desafios_RCO_query)
            get_OA_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_OA_Desafios_RCO_quantity:
                get_OA_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'bn_total': row[2], 'ml_total': row[3], 'bn_CN05OAAC': row[4], 'ml_CN05OAAC': row[5], 'bn_MA04OA17': row[6], 'ml_MA04OA17': row[7], 'bn_MA04OA18': row[8], 'ml_MA04OA18': row[9], 'bn_MA04OAH': row[10], 'ml_MA04OAH': row[11] })


            #get_OA_2_bien
            get_OA2_Desafios_RCO_query = get_OA2_Desafios_RCO(request)
            queries.append({"name": 'get_OA2_Desafios_RCO query', "query": get_OA2_Desafios_RCO_query})
            cursor.execute(get_OA2_Desafios_RCO_query)
            get_OA2_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_OA2_Desafios_RCO_quantity:
                get_OA2_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'bn_CN05OAAC': row[2] })

            #get_OA_2_mal
            get_OA2_2_Desafios_RCO_query = get_OA2_2_Desafios_RCO(request)
            queries.append({"name": 'get_OA2_2_Desafios_RCO query', "query": get_OA2_2_Desafios_RCO_query})
            cursor.execute(get_OA2_2_Desafios_RCO_query)
            get_OA2_2_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_OA2_2_Desafios_RCO_quantity:
                get_OA2_2_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'ml_CN05OAAC': row[2] })

            #get_OA_3_bien
            get_OA3_Desafios_RCO_query = get_OA3_Desafios_RCO(request)
            queries.append({"name": 'get_OA3_Desafios_RCO query', "query": get_OA3_Desafios_RCO_query})
            cursor.execute(get_OA3_Desafios_RCO_query)
            get_OA3_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_OA3_Desafios_RCO_quantity:
                get_OA3_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'bn_MA04OA17': row[2] })

            #get_OA_3_mal
            get_OA3_2_Desafios_RCO_query = get_OA3_2_Desafios_RCO(request)
            queries.append({"name": 'get_OA3_2_Desafios_RCO query', "query": get_OA3_2_Desafios_RCO_query})
            cursor.execute(get_OA3_2_Desafios_RCO_query)
            get_OA3_2_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_OA3_2_Desafios_RCO_quantity:
                get_OA3_2_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'ml_MA04OA17': row[2] })
            
            #get_OA_4_bien
            get_OA4_Desafios_RCO_query = get_OA4_Desafios_RCO(request)
            queries.append({"name": 'get_OA4_Desafios_RCO query', "query": get_OA4_Desafios_RCO_query})
            cursor.execute(get_OA4_Desafios_RCO_query)
            get_OA4_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_OA4_Desafios_RCO_quantity:
                get_OA4_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'bn_MA04OA18': row[2] })

            #get_OA_4_mal
            get_OA4_2_Desafios_RCO_query = get_OA4_2_Desafios_RCO(request)
            queries.append({"name": 'get_OA4_2_Desafios_RCO query', "query": get_OA4_2_Desafios_RCO_query})
            cursor.execute(get_OA4_2_Desafios_RCO_query)
            get_OA4_2_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_OA4_2_Desafios_RCO_quantity:
                get_OA4_2_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'ml_MA04OA18': row[2] })

            #get_OA_5_bien
            get_OA5_Desafios_RCO_query = get_OA5_Desafios_RCO(request)
            queries.append({"name": 'get_OA5_Desafios_RCO query', "query": get_OA5_Desafios_RCO_query})
            cursor.execute(get_OA5_Desafios_RCO_query)
            get_OA5_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_OA5_Desafios_RCO_quantity:
                get_OA5_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'bn_MA04OAHA': row[2] })

            #get_OA_5_mal
            get_OA5_2_Desafios_RCO_query = get_OA5_2_Desafios_RCO(request)
            queries.append({"name": 'get_OA5_2_Desafios_RCO query', "query": get_OA5_2_Desafios_RCO_query})
            cursor.execute(get_OA5_2_Desafios_RCO_query)
            get_OA5_2_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_OA5_2_Desafios_RCO_quantity:
                get_OA5_2_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'ml_MA04OAHA': row[2] })

            #get_victorias
            get_victorias_Desafios_RCO_query = get_victorias_Desafios_RCO(request)
            queries.append({"name": 'get_victorias_Desafios_RCO query', "query": get_victorias_Desafios_RCO_query})
            cursor.execute(get_victorias_Desafios_RCO_query)
            get_victorias_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_victorias_Desafios_RCO_quantity:
                get_victorias_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'victorias': row[2] })

            #get_derrotas
            get_derrotas_Desafios_RCO_query = get_derrotas_Desafios_RCO(request)
            queries.append({"name": 'get_derrotas_Desafios_RCO query', "query": get_derrotas_Desafios_RCO_query})
            cursor.execute(get_derrotas_Desafios_RCO_query)
            get_derrotas_Desafios_RCO_quantity = cursor.fetchall()
            for row in get_derrotas_Desafios_RCO_quantity:
                get_derrotas_Desafios_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'derrotas': row[2] })

            #get_movimientos
            get_mov_multi_RCO_query = get_mov_multi_RCO(request)
            queries.append({"name": 'get_mov_multi_RCO query', "query": get_mov_multi_RCO_query})
            cursor.execute(get_mov_multi_RCO_query)
            get_mov_multi_RCO_quantity = cursor.fetchall()
            for row in get_mov_multi_RCO_quantity:
                get_mov_multi_RCO_quantity_response.append({ 'id': row[0], 'name': row[1], 'movimientos': row[2] })


            #ELEMENTOS creacion analitica
            elementos_analitica_RCO_query = get_elementos_alu_RCO(request)
            queries.append({
                "name": 'creacion analitica query',
                "query": elementos_analitica_RCO_query
            })
            cursor.execute(elementos_analitica_RCO_query)
            elementos_RCO_quantity = cursor.fetchall()
            for row in elementos_RCO_quantity:
                elementos_analitica_RCO_quantity_response.append({
                    'id':
                    row[0],
                    'name':
                    row[1],
                    'quantity':
                    row[2]
                })

            #otros
            #posicionamiento_RCO_graf = len(posicionamiento_RCO_quantity_response) * 40+100
            get_OA_Desafios_RCO_graf = len(get_OA_Desafios_RCO_quantity_response) * 40+100
            get_OA2_Desafios_RCO_graf = len(get_OA2_Desafios_RCO_quantity_response) * 40+100
            get_OA2_2_Desafios_RCO_graf = len(get_OA2_2_Desafios_RCO_quantity_response) * 40+100
            get_OA3_Desafios_RCO_graf = len(get_OA3_Desafios_RCO_quantity_response) * 40+100
            get_OA3_2_Desafios_RCO_graf = len(get_OA3_2_Desafios_RCO_quantity_response) * 40+100
            get_OA4_Desafios_RCO_graf = len(get_OA4_Desafios_RCO_quantity_response) * 40+100
            get_OA4_2_Desafios_RCO_graf = len(get_OA4_2_Desafios_RCO_quantity_response) * 40+100
            get_OA5_Desafios_RCO_graf = len(get_OA5_Desafios_RCO_quantity_response) * 40+100
            get_OA5_2_Desafios_RCO_graf = len(get_OA5_2_Desafios_RCO_quantity_response) * 40+100
            get_victorias_Desafios_RCO_graf = len(get_victorias_Desafios_RCO_quantity_response) * 40+100
            get_derrotas_Desafios_RCO_graf = len(get_derrotas_Desafios_RCO_quantity_response) * 40+100
            get_mov_multi_RCO_graf = len(get_mov_multi_RCO_quantity_response) * 40+100
            
            if activity_num=="9009":
                # act 9009
                touch_all_OA1Bien_query = get_touch_all_OA1Bien(request)
                cursor.execute(touch_all_OA1Bien_query)
                queries.append({"name": 'Touch all OA1Bien query', "query": touch_all_OA1Bien_query})
                touch_all_OA1Bien_quantity = cursor.fetchall()
                #print ("Touch all OA1Bien quantity" , touch_all_OA1Bien_quantity)
                for row in touch_all_OA1Bien_quantity:
                    touch_all_OA1Bien_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
                touch_all_OA1Bien_quantity_graph = len(touch_all_OA1Bien_quantity)*40+20

            ######INICIO TOYS COLECTION#####
        
        #Cantidad Sesiones
        cant_sesiones = get_sesiones(request)
        #print(cant_sesiones)
        queries.append({"name": 'Sesiones', "query": cant_sesiones})
        cursor.execute(cant_sesiones)
        sesion_quantity1 = cursor.fetchall()
        sesion_quantity1_response = []
        for row in sesion_quantity1:
            sesion_quantity1_response.append({ 'name': row[0], 'quantity': row[1] })
        #print("sesion_quantity1_response")
        #print(sesion_quantity1_response)
        sesion_quantity1_graph = len(sesion_quantity1)*120+20

        #Tiempo Sesiones
        play_time = get_tiempo_total(request)
        #print(play_time)
        queries.append({"name": 'Sesiones', "query": play_time})
        #print(queries)
        cursor.execute(play_time)
        tiempo_total_quantity1 = cursor.fetchall()
        #print(tiempo_total_quantity)
        tiempo_total_quantity1_response = []
        for row in tiempo_total_quantity1:
            tiempo_total_quantity1_response.append({ 'name': row[0], 'quantity': row[1] })
        tiempo_total_quantity1_graph = len(tiempo_total_quantity1)*120+20


        #Tiempo Promedio Sesiones
        tiempo_promedio = get_tiempo_promedio(request)
        queries.append({"name": 'Tiempo Promedio', "query": tiempo_promedio})
        cursor.execute(tiempo_promedio)
        tiempo_promedio_quantity1 = cursor.fetchall()
        tiempo_promedio_quantity1_response = []
        for row in tiempo_promedio_quantity1:
            tiempo_promedio_quantity1_response.append({ 'id': row[0], 'name': row[1], 'time': row[2] })
        tiempo_promedio_quantity1_graph = len(tiempo_promedio_quantity1)*40+20
        #Solicitudes
        solicitar = get_solicitudes(request)
        queries.append({"name": 'Solicitudes Realizadas', "query": solicitar})
        cursor.execute(solicitar)
        solicitar_quantity1 = cursor.fetchall()
        solicitar_quantity1_response = []
        for row in solicitar_quantity1:
            solicitar_quantity1_response.append({ 'name': row[0], 'quantity': row[1] })
        solicitar_quantity1_graph = len(solicitar_quantity1)*40+20
        #Colaboracion
        colaborar = get_colaboraciones(request)
        queries.append({"name": 'Colaboraciones Realizadas', "query": colaborar})
        cursor.execute(colaborar)
        colaborar_quantity1 = cursor.fetchall()
        colaborar_quantity1_response = []
        for row in colaborar_quantity1:
            colaborar_quantity1_response.append({ 'name': row[0], 'quantity': row[1] })
        colaborar_quantity1_graph = len(colaborar_quantity1)*40+20
        #Colaboracion Recibida
        colaborar_rec = get_colaboraciones_rec(request)
        queries.append({"name": 'Colaboraciones Realizadas', "query": colaborar_rec})
        cursor.execute(colaborar_rec)
        colaborar_rec_quantity1 = cursor.fetchall()
        colaborar_rec_quantity1_response = []
        for row in colaborar_rec_quantity1:
            colaborar_rec_quantity1_response.append({ 'name': row[1], 'quantity': row[2] })
        colaborar_rec_quantity1_graph = len(colaborar_rec_quantity1)*40+20

        #Lugares Elegidos
        lugar_elegido = get_Lugar_Buscado(request)
        queries.append({"name": 'Lugar Elegido', "query": lugar_elegido})
        cursor.execute(lugar_elegido)
        lugar_elegido_quantity1 = cursor.fetchall()
        lugar_elegido_quantity1_response = []
        for row in lugar_elegido_quantity1:
            lugar_elegido_quantity1_response.append({ 'name': row[0], 'casa': row[1] , 'parque': row[2] , 'colegio': row[3] })
        lugar_elegido_quantity1_graph = len(lugar_elegido_quantity1)*40+20
        #Habitacion Elegidos
        habitacion_elegido1 = get_Habitacion_Buscado1(request)
        queries.append({"name": 'Habitacion Elegido 1', "query": habitacion_elegido1})
        cursor.execute(habitacion_elegido1)
        habitacion_elegido1_quantity1 = cursor.fetchall()
        habitacion_elegido1_quantity1_response = []
        for row in habitacion_elegido1_quantity1:
            habitacion_elegido1_quantity1_response.append({ 'name': row[0], 'dormitorio': row[1] , 'cocina': row[2] , 'bano': row[3] , 'living': row[4] ,  'comedor': row[5] })
        habitacion_elegido1_quantity1_graph = len(habitacion_elegido1_quantity1)*40+20
        #Habitacion Elegidos
        habitacion_elegido2 = get_Habitacion_Buscado2(request)
        queries.append({"name": 'Habitacion Elegido 2', "query": habitacion_elegido2})
        cursor.execute(habitacion_elegido2)
        habitacion_elegido2_quantity1 = cursor.fetchall()
        habitacion_elegido2_quantity1_response = []
        for row in habitacion_elegido2_quantity1:
            habitacion_elegido2_quantity1_response.append({ 'name': row[0], 'parque': row[1] })
        habitacion_elegido2_quantity1_graph = len(habitacion_elegido2_quantity1)*40+20
        #Habitacion Elegidos
        habitacion_elegido3 = get_Habitacion_Buscado3(request)
        queries.append({"name": 'Habitacion Elegido 3', "query": habitacion_elegido3})
        cursor.execute(habitacion_elegido3)
        habitacion_elegido3_quantity1 = cursor.fetchall()
        habitacion_elegido3_quantity1_response = []
        for row in habitacion_elegido3_quantity1:
            habitacion_elegido3_quantity1_response.append({ 'name': row[0], 'pasillo': row[1] , 'sala': row[2] })
        habitacion_elegido3_quantity1_graph = len(habitacion_elegido3_quantity1)*40+20
        #General Desafíos
        desafio = get_desafios(request)
        queries.append({"name": 'Desafío', "query": desafio})
        cursor.execute(desafio)
        desafio_quantity1 = cursor.fetchall()
        desafio_quantity2_response = []
        for row in desafio_quantity1:
            desafio_quantity2_response.append({ 'name': row[1] , 'no_realizado': row[2] , 'correctas': row[3] , 'incorrectas': row[4] })
        desafio_quantity1_graph = len(desafio_quantity1)*40+20
        #General Desafíos Porcentual
        desafio_porcentual = get_desafios_porcentual(request)
        queries.append({"name": 'Desafío Porcentual', "query": desafio_porcentual})
        cursor.execute(desafio_porcentual)
        desafio_porcentual_quantity1 = cursor.fetchall()
        desafio_porcentual_quantity1_response = []
        i=0
        for row in desafio_porcentual_quantity1:
            i=i+1
            desafio_porcentual_quantity1_response.append({ 'name': i , 'correctas': row[1] })
        desafio_porcentual_quantity1_graph = len(desafio_porcentual_quantity1)*40+20
        #General no Desafíos
        no_desafio = get_no_desafios(request)
        queries.append({"name": 'Desafío', "query": no_desafio})
        cursor.execute(no_desafio)
        no_desafio_quantity1 = cursor.fetchall()
        no_desafio_quantity1_response = []
        for row in no_desafio_quantity1:
            no_desafio_quantity1_response.append({ 'name': row[0] , 'cantidad': row[1]})
        no_desafio_quantity1_graph = len(no_desafio_quantity1)*40+20
        #desafio colores
        colores=get_colores(request)
        queries.append({"name": 'Colores General', "query": colores})
        cursor.execute(colores)
        colores_quantity1 = cursor.fetchall()
        colores_quantity1_response=[]
        for row in colores_quantity1:
            colores_quantity1_response.append({ 'colores': row[1] , 'correctas': row[2] , 'incorrectas': row[3] })
        colores_quantity1_graph = len(colores_quantity1)*40+20
        #desafio formas
        formas=get_formas(request)
        queries.append({"name": 'Formas General', "query": formas})
        cursor.execute(formas)
        formas_quantity1 = cursor.fetchall()
        formas_quantity1_response=[]
        for row in formas_quantity1:
            formas_quantity1_response.append({ 'formas': row[1] , 'correctas': row[2] , 'incorrectas': row[3] })
        formas_quantity1_graph = len(formas_quantity1)*40+20
        #desafio vocales
        vocales=get_vocales(request)
        queries.append({"name": 'Vocales General', "query": vocales})
        cursor.execute(vocales)
        vocales_quantity1 = cursor.fetchall()
        vocales_quantity1_response=[]
        for row in vocales_quantity1:
            vocales_quantity1_response.append({ 'vocales': row[1] , 'correctas': row[2] , 'incorrectas': row[3] })
        vocales_quantity1_graph = len(vocales_quantity1)*40+20
        #desafio numeros
        numeros=get_numeros(request)
        queries.append({"name": 'Numeros General', "query": numeros})
        cursor.execute(numeros)
        numeros_quantity1 = cursor.fetchall()
        numeros_quantity1_response=[]
        for row in numeros_quantity1:
            numeros_quantity1_response.append({ 'numeros': row[1] , 'correctas': row[2] , 'incorrectas': row[3] })
        numeros_quantity1_graph = len(numeros_quantity1)*40+20
        #ordenar
        ordenar=get_ordenar(request)
        queries.append({"name": 'Ordenar General', "query": ordenar})
        cursor.execute(ordenar)
        ordenar_quantity1 = cursor.fetchall()
        ordenar_quantity1_response=[]
        i=0
        for row in ordenar_quantity1:
            i=i+1
            ordenar_quantity1_response.append({ 'name': i , 'correctas': row[1] })
        ordenar_quantity1_graph = len(ordenar_quantity1)*40+20
        #ordenar Resultados
        ordenar_res=get_ordenar_resultados(request)
        queries.append({"name": 'Ordenar Resultados General', "query": ordenar_res})
        cursor.execute(ordenar_res)
        ordenar_res_quantity1 = cursor.fetchall()
        ordenar_res_quantity1_response=[]
        i=0
        for row in ordenar_res_quantity1:
            ordenar_res_quantity1_response.append({ 'name': row[1] , 'correctas': row[2] , 'incorrectas': row[3] })
        ordenar_res_quantity1_graph = len(ordenar_res_quantity1)*40+20
        #buscar
        buscar=get_buscar(request)
        queries.append({"name": 'Buscar General', "query": buscar})
        cursor.execute(buscar)
        buscar_quantity1 = cursor.fetchall()
        buscar_quantity1_response=[]
        i=0
        for row in buscar_quantity1:
            i=i+1
            buscar_quantity1_response.append({ 'name': i , 'correctas': row[1] })
        #print(buscar_quantity1_response)
        buscar_quantity1_graph = len(buscar_quantity1)*40+20
        #buscar Resultados.
        buscar_res=get_buscar_resultados(request)
        queries.append({"name": 'Buscar General', "query": buscar_res})
        cursor.execute(buscar_res)
        buscar_res_quantity1 = cursor.fetchall()
        buscar_res_quantity1_response=[]
        for row in buscar_res_quantity1:
            buscar_res_quantity1_response.append({ 'name': row[1] , 'correctas': row[2] , 'incorrectas': row[3] })
        buscar_res_quantity1_graph = len(buscar_res_quantity1)*40+20
        #donaciones
        donaciones= get_donaciones(request)
        queries.append({"name": 'Donaciones', "query": donaciones})
        cursor.execute(donaciones)
        donaciones_quantity1 = cursor.fetchall()
        donaciones_quantity1_response=[]
        i=0
        for row in donaciones_quantity1:
            donaciones_quantity1_response.append({ 'name': row[0] , 'cantidad': row[1]  })
        donaciones_quantity1_graph = len(donaciones_quantity1)*40+20

        ######FIN TOYS COLECTION#####
                
        ################################################################
        ############################RECICLANDO##########################
        #################################################################

#Cantidad de Sesiones
        session_query = get_session_query(request)
        cursor.execute(session_query)
        queries.append({"name": 'Session query', "query": session_query})
        sesion_quantity = cursor.fetchall()
        sesion_quantity_response = []
        for row in sesion_quantity:
            sesion_quantity_response.append({
                'id': row[0],
                'name': row[1],
                'quantity': row[2]
            })
        sesion_quantity_graph = len(sesion_quantity) * 40 + 20

        activate_graphics = activate_course_filter and activate_school_filter and activate_reim_filter
        activate_graphics_general = activate_activity_filter and activate_course_filter and activate_school_filter and activate_reim_filter
        activate_graphics_student = activate_course_filter and activate_school_filter and activate_reim_filter and activate_student_filter

        return render(
            request,
            "users/welcome.html",
            {
                # Show graphics at the init
                'activate_graphics':
                activate_graphics,
                'activate_graphics_general':
                activate_graphics_general,
                'activate_graphics_student':
                activate_graphics_student,
                # Other context var
                'queries':
                queries,
                'schools':
                schools_response,
                'reims':
                reims_response,
                'game_time':
                game_time_response,
                'courses':
                courses_response,
                'activities':
                activities_response,
                'students':
                students_response,
                'touch_quantity':
                touch_quantity_response,
                'touch_quantity_len':
                len(touch_quantity_response),
                'sesion_quantity':
                sesion_quantity_response,
                'cant_usuarios':
                cant_usuarios,
                'activity_num':
                activity_num,
                'student_num':
                student_num,
                'reim_num':
                reim_num,
                #size graphs
                'sesion_quantity_graph':
                sesion_quantity_graph,
                'touch_quantity_graph':
                touch_quantity_graph,
                'game_time_graph':
                game_time_graph,
                #CLEAN OCEAN
                'colision_quantity':
                colision_quantity_response,
                'corrects_quantity':
                corrects_quantity_response,
                'incorrects_quantity':
                incorrects_quantity_response,
                'corrects_incorrects_quantity':
                corrects_incorrects_quantity_response,
                'jumps_quantity':
                jumps_quantity_response,
                'analytics_co_quantity':
                analytics_co_quantity_response,
                'exit_lab_quantity':
                exit_lab_quantity_response,
                'touch_animals_co_quantity':
                touch_animals_co_quantity_response,
                'touch_trash_co_quantity':
                touch_trash_co_quantity_response,
                'actividades_co_quantity':
                actividades_co_quantity_response,
                'colision_trash_quantity':
                colision_trash_quantity_response,
                'touch_all_animals_quantity':
                touch_all_animals_quantity_response,
                'exits_lab_co_quantity':
                exits_lab_co_quantity_response,
                'touch_all_trash_quantity':
                touch_all_trash_quantity_response,
                'buttons_co_quantity':
                buttons_co_quantity_response,
                'trash_clean_co_quantity':
                trash_clean_co_quantity_response,
                'corrects_student_co_quantity':
                corrects_student_co_quantity_response,
                'time_act_co_quantity':
                time_act_co_quantity_response,
                #height graphs
                'colision_quantity_graph':
                colision_quantity_graph,
                'corrects_quantity_graph':
                corrects_quantity_graph,
                'corrects_incorrects_quantity_graph':
                corrects_incorrects_quantity_graph,
                'jumps_quantity_graph':
                jumps_quantity_graph,
                'analytics_co_quantity_graph':
                analytics_co_quantity_graph,
                'actividades_co_quantity_graph':
                actividades_co_quantity_graph,
                'exit_lab_quantity_graph':
                exit_lab_quantity_graph,
                'touch_trash_co_quantity_graph':
                touch_trash_co_quantity_graph,
                'corrects_student_co_quantity_graph':
                corrects_student_co_quantity_graph,
                'colision_trash_quantity_graph':
                colision_trash_quantity_graph,
                'exits_lab_co_quantity_graph':
                exits_lab_co_quantity_graph,
                'touch_all_trash_quantity_graph':
                touch_all_trash_quantity_graph,
                'buttons_co_quantity_graph':
                buttons_co_quantity_graph,
                'trash_clean_co_quantity_graph':
                trash_clean_co_quantity_graph,
                'time_act_co_quantity_graph':
                time_act_co_quantity_graph,
                #promedios
                'promedio_correctas_co':
                int(promedio_correctas_co - 0.5) + 1,
                'promedio_incorrectas_co':
                int(promedio_incorrectas_co - 0.5) + 1,
                'promedio_saltos':
                int(promedio_saltos - 0.5) + 1,
                'promedio_colisions':
                int(promedio_colisions - 0.5) + 1,
                #MUNDO ANIMAL
                'piezas_quantity':
                piezas_quantity_response,
                'malas_quantity':
                malas_quantity_response,
                'animales_quantity':
                animales_quantity_response,
                'actividades_quantity':
                actividades_quantity_response,
                'interaccion_quantity':
                interaccion_quantity_response,
                'tiempoact_quantity':
                tiempoact_quantity_response,
                'promedio_correctas':
                int(promedio_correctas),
                'promedio_incorrectas':
                int(promedio_incorrectas),
                'analytics1_co_quantity':
                analytics1_co_quantity_response,
                'tiempo_total_quantity':
                tiempo_total_quantity_response,
                'audios_quantity':
                audios_quantity_response,
                'animales_quantity_graph':
                animales_quantity_graph,
                #Día Mundial
                'time_DM_quantity':
                time_PS_quantity_response,
                'completa_incompleta_DM_quantity':
                completa_incompleta_DM_quantity_response,
                'fruta_chatarra_DM_quantity_response':
                fruta_chatarra_DM_quantity_response,
                'muro_hoyo_DM_quantity_response':
                muro_hoyo_DM_quantity_response,
                'tipo_basura_DM_quantity_response':
                tipo_basura_DM_quantity_response,
                'animales_nivel_DM_quantity_response':
                animales_nivel_DM_quantity_response,
                'touches_luces_DM_quantity_response':
                touches_luces_DM_quantity_response,
                'get_miel_cae_choca_DM_quantity_response':
                get_miel_cae_choca_DM_quantity_response,
                'get_animales_salvados_DM_quantity_response':
                get_animales_salvados_DM_quantity_response,
                'get_animales_salvados_pornivel_DM_quantity_response':
                get_animales_salvados_pornivel_DM_quantity_response,
                'correcta_incorrecta_arbol_DM_quantity_response':
                correcta_incorrecta_arbol_DM_quantity_response,
                'crecimiento_arbol_DM_quantity_response':
                crecimiento_arbol_DM_quantity_response,
                'completa_incompleta_inactividad':
                completa_incompleta_inactividad,
                'col_vs_time':
                col_vs_time,
                'tiempoXact_quantity_responseDM':
                tiempoXact_quantity_responseDM,
                'get_ganar_perder_DM_Quest_response':
                get_ganar_perder_DM_Quest_response,
                'colisiones_tiempo_media':
                colisiones_tiempo_media,
                'colisiones_muro_media':
                colisiones_muro_media,
                'colisiones_hoyo_media':
                colisiones_hoyo_media,
                'lista_alumnos_final2':
                lista_alumnos_final2,
                'lista_unico_alumno':
                lista_unico_alumno,
                #PLUSSPACE
                'move_element_quantity':
                move_element_quantity_response,
                'elementos_PS_quantity':
                elementos_PS_quantity_response,
                'posicionamiento_PS_quantity':
                posicionamiento_PS_quantity_response,
                'element_colission_quantity':
                element_colission_quantity_response,
                'jump_alternativas_quantity':
                jump_alternativas_quantity_response,
                'acierto_cuida_quantity':
                acierto_cuida_quantity_response,
                'completa_incompleta_PS_quantity':
                completa_incompleta_PS_quantity_response,
                'correctas_PS_quantity':
                correctas_PS_quantity_response,
                'time_PS_quantity':
                time_PS_quantity_response,
                #por alumno
                'jumpxalumno_quantity':
                jumpxalumno_quantity_response,
                'elementosXalum_PS_quantity':
                elementosXalum_PS_quantity_response,
                'element_colission_alum_quantity':
                element_colission_alum_quantity_response,
                'posicionamiento_alu_PS_quantity':
                posicionamiento_alu_PS_quantity_response,
                'acierto_cuida_alu_quantity':
                acierto_cuida_alu_quantity_response,
                #tamaño de graficos
                'time_PS_graf':
                time_PS_graf,
                'correctas_PS_graf':
                correctas_PS_graf,
                'move_element_graf':
                move_element_graf,
                'elementos_PS_graf':
                elementos_PS_graf,
                'element_colission_graf':
                element_colission_graf,
                'posicionamiento_PS_graf':
                posicionamiento_PS_graf,
                'jump_alternativas_graf':
                jump_alternativas_graf,
                'acierto_cuida_graf':
                acierto_cuida_graf,
                'completa_incompleta_PS_graf':
                completa_incompleta_PS_graf,
                'tiempoXact_quantity':
                tiempoXact_quantity_response,
                #analitica
                'elementos_analitica_PS_quantity':
                elementos_analitica_PS_quantity_response,
                'colission_analitica_quantity':
                colission_analitica_quantity_response,
                'touch_puzzle_quantity':
                touch_puzzle_quantity_response,
                'nombre':
                nombre,
                #INICIO REIM ID = 77, NOMBRE = BUSCANDO EL TESORO PERDIDO
                'tiempo_x_actividad':
                tiempo_x_actividad_response,
                'respuesta_x_estilo':
                identificar_estilo_cognitivo_response,
                'estilo_x_cognitivo':
                Estilo_cognitivo_por_niño,
                'actividad_1_volcan_response':
                actividad_1_volcan,
                'figura_compleja_x_actividad':
                buenas_malas_x_figura_compleja,
                'tiempo_acti_sesion':
                tiempoxactxsesion,
                'grafico_curso_77':
                lista_alumno_cognitivo,
                'grafico_muy_dependiente':
                lista_alumno_cognitivo_muy_dependiente,
                'grafico_dependiente':
                lista_alumno_cognitivo_dependiente,
                'grafico_intermedio':
                lista_alumno_cognitivo_intermedio,
                'grafico_independiente':
                lista_alumno_cognitivo_independiente,
                'grafico_muy_independiente':
                lista_alumno_cognitivo_muy_independiente,
                'Reconocimiento_Alumno':
                nombre_estilo_cognitivo_alumno,
                #Tamaño Grafico
                'time_PS_graf_1':
                time_ps_query_77,
                'estilo_cognitivo':
                identificar_estilo_cognitivo,
                'tamaño_curso':
                tamaño_curso,
                'tamaña_grafico_por_alumno':
                tamaña_grafico_por_alumno,
                'tamaño_actividad_alumno':
                tamaña_grafico_por_actividad,
                #FIN REIM ID = 77, NOMBRE = BUSCANDO EL TESORO PERDIDO
                # INICIO RECICLANDO CONSTRUYO
                'Porcentaje_llave':porcentaje_llave_quantity_response,
                'Promedio_intentos_llave':promedio_intentos_response,
                'Promedio_intentos_totales_llave':promedio_intentos_totales_response,
                'Elementos_reciclados_usuario':elementos_reciclados_usuario_response,
                'Elementos_reciclados_usuario_incorrecto': elementos_reciclados_usuario_incorrecto_response,
                'Respuestas_Usuario_VencerAlConstructor': Respuestas_Usuario_VencerAlConstructorresponse,
                'ElementosRecicladosGeneral_tipo': ElementosRecicladosGeneral_tipo_response,
                'ElementosRecicladosGeneralIncorrectamente_tipo': ElementosRecicladosGeneralIncorrectamente_tipo_response,
                'Llave_tipo': Llave_tipo_response,
                'Llave_tipo_size': Llave_tipo_size,
                'Respuestas_General_VencerAlConstructor': Respuestas_General_VencerAlConstructor_response,
                'Historial_Respuestas': Historial_Respuestas_response,
                'Historial_Respuestas_Anexar': Historial_Respuestas_Anexar_response,
                'Historial_Respuestas_Dividir': Historial_Respuestas_Dividir_response,
                'Historial_movimientos': Historial_movimientos_response,
                'Historial_movimientos_Sol': Historial_movimientos_Sol_response,
                'Historial_movimientos_Nube': Historial_movimientos_Nube_response,
                'Historial_movimientos_Triangulo': Historial_movimientos_Triangulo_response,
                'tiempo_size' : tiempo_size,
                # FIN RECICLANDO CONSTRUYO
                #########################Inicio Reciclando cuido el oceano###############################
                'touch_all_act206_quantity':touch_all_act206_quantity_response,
                'time_act_RCO_quantity':time_act_RCO_quantity_response,
                'time_act_RCOTotal_quantity':time_act_RCOTotal_quantity_response,
                'corrects_incorrects_quantity':corrects_incorrects_quantity_response,
                'corrects_quantity':corrects_quantity_response,
                'incorrects_quantity':incorrects_quantity_response,
                'completa_incompleta_RCO_quantity':completa_incompleta_RCO_quantity_response,
                'analytics1_1_co_quantity_act_3':analytics1_1_co_quantity_act_3_response,
                'analytics1_co_quantity_act_3':analytics1_co_quantity_act_3_response,
                'posicionamiento_RCO_quantity':posicionamiento_RCO_quantity_response,
                'get_OA_Desafios_RCO_quantity':get_OA_Desafios_RCO_quantity_response,
                'get_OA2_Desafios_RCO_quantity':get_OA2_Desafios_RCO_quantity_response,
                'get_OA2_2_Desafios_RCO_quantity':get_OA2_2_Desafios_RCO_quantity_response,
                'get_OA3_Desafios_RCO_quantity':get_OA3_Desafios_RCO_quantity_response,
                'get_OA3_2_Desafios_RCO_quantity':get_OA3_2_Desafios_RCO_quantity_response,
                'get_OA4_Desafios_RCO_quantity':get_OA4_Desafios_RCO_quantity_response,
                'get_OA4_2_Desafios_RCO_quantity':get_OA4_2_Desafios_RCO_quantity_response,
                'get_OA5_Desafios_RCO_quantity':get_OA5_Desafios_RCO_quantity_response,
                'get_OA5_2_Desafios_RCO_quantity':get_OA5_2_Desafios_RCO_quantity_response,
                'get_victorias_Desafios_RCO_quantity':get_victorias_Desafios_RCO_quantity_response,
                'get_derrotas_Desafios_RCO_quantity':get_derrotas_Desafios_RCO_quantity_response,
                'get_mov_multi_RCO_quantity':get_mov_multi_RCO_quantity_response,
                'touch_all_OA1Bien_quantity':touch_all_OA1Bien_quantity_response,
                'elementos_analitica_RCO_quantity':elementos_analitica_RCO_quantity_response,
                'time_act_RCO_quantity_graph':time_act_RCO_quantity_graph,
                'time_act_RCOTotal_quantity_graph':time_act_RCOTotal_quantity_graph,
                'touch_all_OA1Bien_quantity_graph':touch_all_OA1Bien_quantity_graph,
                ########################FinReciclando###############################
                #####BEGIN BUILD YOUR CITY#####
                #LISTS OF DUMMY VALUES (FRONTEND TEST):
                'listOfFirst50Numbers': [
                    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                    '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                    '22', '23', '24', '25', '26', '27', '28', '29', '30', '31',
                    '32', '33', '34', '35', '36', '37', '38', '39', '40', '41',
                    '42', '43', '44', '45', '46', '47', '48', '49', '50'
                ],
                'listOf100to2000by100': [
                    100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100,
                    1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000
                ],
                'listOf25To42': [
                    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                    40, 41, 42
                ],
                'listOfFirst10Numbers':
                ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                'listOfDates': [
                    '10/05/2020', '11/05/2020', '12/05/2020', '13/05/2020',
                    '14/05/2020', '15/05/2020', '16/05/2020', '17/05/2020',
                    '18/05/2020'
                ],
                'activities_ByC': [
                    "Actividad 1: Mapa de Construccion", "Actividad 2: Cine",
                    "Actividad 3: Escuela", "Actividad 4: Taxi"
                ],
                'ByC_UrbanElements': [
                    'Casa Azul', 'Casa Roja', 'Casa Verde', 'Edificio Azul',
                    'Fuente de Agua', 'Semaforo', 'Arbol', 'Obelisco', 'Taxi',
                    'Policia', 'Ambulancia', 'Camion de Bomberos'
                ],

                #GRAPHS SIZE:
                'ByC_numberOfSessions_GraphSize':
                ByC_numberOfSessions_GraphSize,
                'ByC_playTime_GraphSize':
                ByC_playTime_GraphSize,
                'ByC_touchCount_GraphSize':
                ByC_touchCount_GraphSize,
                'ByC_activitiesPlayedCounter_GraphSize':
                ByC_activitiesPlayedCounter_GraphSize,
                'ByC_built_elementsCounter_GraphSize':
                ByC_built_elementsCounter_GraphSize,
                'ByC_built_elementsCounter_perCategory_GraphSize':
                ByC_built_elementsCounter_perCategory_GraphSize,
                'ByC_maxNumberOfAssistants_GraphSize':
                ByC_maxNumberOfAssistants_GraphSize,
                'ByC_Cinema_CompleteVsIncomplete_GraphSize':
                ByC_Cinema_CompleteVsIncomplete_GraphSize,
                'ByC_Cinema_SuccessVsFailure_GraphSize':
                ByC_Cinema_SuccessVsFailure_GraphSize,
                'ByC_Cinema_SuccessVsFailure_ParticularSeats_GraphSize':
                ByC_Cinema_SuccessVsFailure_ParticularSeats_GraphSize,
                'ByC_Cinema_NumberOfEntrances_GraphSize':
                ByC_Cinema_NumberOfEntrances_GraphSize,
                'ByC_School_CompleteVsIncomplete_GraphSize':
                ByC_School_CompleteVsIncomplete_GraphSize,
                'ByC_School_SuccessVsFailure_GraphSize':
                ByC_School_SuccessVsFailure_GraphSize,
                'ByC_School_SuccessVsFailure_ParticularSeats_GraphSize':
                ByC_School_SuccessVsFailure_ParticularSeats_GraphSize,
                'ByC_School_NumberOfEntrances_GraphSize':
                ByC_School_NumberOfEntrances_GraphSize,
                'ByC_Taxi_CompleteVsIncomplete_GraphSize':
                ByC_Taxi_CompleteVsIncomplete_GraphSize,
                'ByC_Taxi_SuccessVsFailure_GraphSize':
                ByC_Taxi_SuccessVsFailure_GraphSize,
                'ByC_Taxi_SuccessVsFailure_ParticularSeats_GraphSize':
                ByC_Taxi_SuccessVsFailure_ParticularSeats_GraphSize,
                'ByC_Taxi_NumberOfEntrances_GraphSize':
                ByC_Taxi_NumberOfEntrances_GraphSize,

                #RESPONSE TO QUERYS:
                'ByC_numberOfSessions_Dictionary':
                ByC_numberOfSessions_Dictionary,
                'ByC_playTime_Dictionary':
                ByC_playTime_Dictionary,
                'ByC_touchCount_Dictionary':
                ByC_touchCount_Dictionary,
                'ByC_activitiesPlayedCounter_Dictionary':
                ByC_activitiesPlayedCounter_Dictionary,
                'ByC_built_elementsCounter_Dictionary':
                ByC_built_elementsCounter_Dictionary,
                'ByC_built_elementsCounter_perCategory_Dictionary':
                ByC_built_elementsCounter_perCategory_Dictionary,
                'ByC_maxNumberOfAssistants_Dictionary':
                ByC_maxNumberOfAssistants_Dictionary,
                'ByC_Cinema_CompleteVsIncomplete_Dictionary':
                ByC_Cinema_CompleteVsIncomplete_Dictionary,
                'ByC_Cinema_SuccessVsFailure_Dictionary':
                ByC_Cinema_SuccessVsFailure_Dictionary,
                'ByC_Cinema_SuccessVsFailure_ParticularSeats_Dictionary':
                ByC_Cinema_SuccessVsFailure_ParticularSeats_Dictionary,
                'ByC_Cinema_NumberOfEntrances_Dictionary':
                ByC_Cinema_NumberOfEntrances_Dictionary,
                'ByC_Cinema_Average_Success':
                int(ByC_Cinema_Average_Success),
                'ByC_Cinema_Average_Failure':
                int(ByC_Cinema_Average_Failure),
                'ByC_Cinema_Average_ParticularSuccess':
                int(ByC_Cinema_Average_ParticularSuccess),
                'ByC_Cinema_Average_ParticularFailure':
                int(ByC_Cinema_Average_ParticularFailure),
                'ByC_Cinema_SuccessPercentageInTime_Dictionary':
                ByC_Cinema_SuccessPercentageInTime_Dictionary,
                'ByC_School_CompleteVsIncomplete_Dictionary':
                ByC_School_CompleteVsIncomplete_Dictionary,
                'ByC_School_SuccessVsFailure_Dictionary':
                ByC_School_SuccessVsFailure_Dictionary,
                'ByC_School_SuccessVsFailure_ParticularSeats_Dictionary':
                ByC_School_SuccessVsFailure_ParticularSeats_Dictionary,
                'ByC_School_NumberOfEntrances_Dictionary':
                ByC_School_NumberOfEntrances_Dictionary,
                'ByC_School_Average_Success':
                int(ByC_School_Average_Success),
                'ByC_School_Average_Failure':
                int(ByC_School_Average_Failure),
                'ByC_School_Average_ParticularSuccess':
                int(ByC_School_Average_ParticularSuccess),
                'ByC_School_Average_ParticularFailure':
                int(ByC_School_Average_ParticularFailure),
                'ByC_School_SuccessPercentageInTime_Dictionary':
                ByC_School_SuccessPercentageInTime_Dictionary,
                'ByC_Taxi_CompleteVsIncomplete_Dictionary':
                ByC_Taxi_CompleteVsIncomplete_Dictionary,
                'ByC_Taxi_SuccessVsFailure_Dictionary':
                ByC_Taxi_SuccessVsFailure_Dictionary,
                'ByC_Taxi_SuccessVsFailure_ParticularSeats_Dictionary':
                ByC_Taxi_SuccessVsFailure_ParticularSeats_Dictionary,
                'ByC_Taxi_NumberOfEntrances_Dictionary':
                ByC_Taxi_NumberOfEntrances_Dictionary,
                'ByC_Taxi_Average_Success':
                int(ByC_Taxi_Average_Success),
                'ByC_Taxi_Average_Failure':
                int(ByC_Taxi_Average_Failure),
                'ByC_Taxi_Average_ParticularSuccess':
                int(ByC_Taxi_Average_ParticularSuccess),
                'ByC_Taxi_Average_ParticularFailure':
                int(ByC_Taxi_Average_ParticularFailure),
                'ByC_Taxi_SuccessPercentageInTime_Dictionary':
                ByC_Taxi_SuccessPercentageInTime_Dictionary,
                ######END BUILD YOUR CITY#####
                ##### BEING PROTECT YOUR LAND
                ####### GRAPHS SIZE
                'PYL_playTime_GraphSize':
                    PYL_playTime_GraphSize,
                'PYL_touchCount_GraphSize':
                    PYL_touchCount_GraphSize,
                'PYL_activitiesPlayedCounter_GraphSize':
                    PYL_activitiesPlayedCounter_GraphSize,
                'PYL_numberOfSessions_GraphSize':
                    PYL_numberOfSessions_GraphSize,
                'PYL_color_GraphSize':
                    PYL_color_GraphSize,
                'PYLcorrects_quantity_graph':
                    PYLcorrects_quantity_graph,
                'PYL_correctsxsession_GraphSize':
                    PYL_correctsxsession_GraphSize,
                'PYL_answer_GraphSize':
                    PYL_answer_GraphSize,
                'PYL_answerOA_GraphSize':
                    PYL_answerOA_GraphSize,
                'PYL_emociones_GraphSize':
                    PYL_emociones_GraphSize,
                'PYL_timer_GraphSize':
                    PYL_timer_GraphSize,
                'PYL_ElemVisual_GraphSize':
                    PYL_ElemVisual_GraphSize,


                'PYL_numberOfSessions_Dictionary':
                    PYL_numberOfSessions_Dictionary,
                'PYL_playTime_Dictionary':
                    PYL_playTime_Dictionary,
                'PYL_touchCount_Dictionary':
                    PYL_touchCount_Dictionary,
                'PYL_activitiesPlayedCounter_Dictionary':
                    PYL_activitiesPlayedCounter_Dictionary,
                'PYL_color_Dictionary':
                    PYL_color_Dictionary,
                'PYLcorrects_quantity_Dictionary':
                    PYLcorrects_quantity_Dictionary,
                'PYL_correctsxsession_Dictionary':
                    PYL_correctsxsession_Dictionary,
                'PYL_answer_Dictionary':
                    PYL_answer_Dictionary,
                'PYL_answerOA_Dictionary':
                    PYL_answerOA_Dictionary,
                'PYL_emociones_Dictionary':
                    PYL_emociones_Dictionary,
                'PYL_timer_Dictionary':
                    PYL_timer_Dictionary,
                'PYL_ElemVisual_Dictionary':
                    PYL_ElemVisual_Dictionary,
				######INICIO TOYS COLECTION
                'sesion_quantity1': sesion_quantity1_response,
                'tiempo_total_quantity1': tiempo_total_quantity1_response,
                'desafio_quantity1': desafio_quantity2_response,
                'desafio_porcentual_quantity1': desafio_porcentual_quantity1_response,
                'tiempo_promedio_quantity1': tiempo_promedio_quantity1_response,
                'lugar_elegido_quantity1': lugar_elegido_quantity1_response,
                'habitacion_elegido1_quantity1': habitacion_elegido1_quantity1_response,
                'habitacion_elegido2_quantity1': habitacion_elegido2_quantity1_response,
                'habitacion_elegido3_quantity1': habitacion_elegido3_quantity1_response,
                'solicitar_quantity1': solicitar_quantity1_response,
                'colaborar_quantity1': colaborar_quantity1_response,
                'colaborar_rec_quantity1': colaborar_rec_quantity1_response,
                'no_desafio_quantity1': no_desafio_quantity1_response,
                'colores_quantity1': colores_quantity1_response,
                'formas_quantity1': formas_quantity1_response,
                'vocales_quantity1': vocales_quantity1_response,
                'numeros_quantity1': numeros_quantity1_response,
                'ordenar_quantity1': ordenar_quantity1_response,
                'ordenar_res_quantity1': ordenar_res_quantity1_response,
                'buscar_quantity1': buscar_quantity1_response,
                'buscar_res_quantity1': buscar_res_quantity1_response,
                'donaciones_quantity1': donaciones_quantity1_response,

                'desafio': desafio,
                'desafio_porcentual': desafio_porcentual,
                'cant_usuarios': cant_usuarios,
                'cant_sesiones': cant_sesiones,
                'play_time': play_time,
                'tiempo_promedio': tiempo_promedio,
                'lugar_elegido': lugar_elegido,
                'habitacion_elegido1': habitacion_elegido1,
                'habitacion_elegido2': habitacion_elegido2,
                'habitacion_elegido3': habitacion_elegido3,
                'solicitar': solicitar,
                'colaborar': colaborar,
                'colaborar_rec': colaborar_rec,
                'no_desafio': no_desafio,
                'colores': colores,
                'formas': formas,
                'vocales': vocales,
                'numeros': numeros,
                'ordenar': ordenar,
                'ordenar_res': ordenar_res,
                'buscar': buscar,
                'buscar_res': buscar_res,
                'donaciones': donaciones,

                'desafio_graph': desafio_quantity1_graph,
                'desafio_porcentual_graph': desafio_porcentual_quantity1_graph,
                'tiempo_promedio_graph': tiempo_promedio_quantity1_graph,
                'tiempo_total_graph': tiempo_total_quantity1_graph,
                'lugar_elegido_graph': lugar_elegido_quantity1_graph,
                'habitacion_elegido1_graph': habitacion_elegido1_quantity1_graph,
                'habitacion_elegido2_graph': habitacion_elegido2_quantity1_graph,
                'habitacion_elegido3_graph': habitacion_elegido3_quantity1_graph,
                'solicitar_graph': solicitar_quantity1_graph,
                'colaborar_graph': colaborar_quantity1_graph,
                'no_desafio_graph': no_desafio_quantity1_graph,
                'colores_graph': colores_quantity1_graph,
                'formas_graph': formas_quantity1_graph,
                'vocales_graph': vocales_quantity1_graph,
                'numeros_graph': numeros_quantity1_graph,
                'sesion_graph': sesion_quantity1_graph,
                'ordenar_graph': ordenar_quantity1_graph,
                'ordenar_res_graph': ordenar_res_quantity1_graph,
                'buscar_graph': buscar_quantity1_graph,
                'buscar_res_graph': buscar_res_quantity1_graph,
                'donaciones_graph': donaciones_quantity1_graph,
				######FIN TOYS COLECTION#####
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
        query = 'SELECT username, email, password, nombres FROM usuario WHERE (tipo_usuario_id = 1 OR tipo_usuario_id = 2) AND (username="' + request.POST.get(
            'username') + '" AND password="' + request.POST.get(
                'password') + '")'
        cursor.execute(query)
        data = cursor.fetchone()

        if data:
            user, created = User.objects.get_or_create(username=data[0],
                                                       email=data[1],
                                                       first_name=data[3])
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