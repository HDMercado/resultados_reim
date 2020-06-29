import pymysql
from datetime import datetime

def get_from_db():
    db = pymysql.connect("ulearnet.org","reim_ulearnet","KsclS$AcSx.20Cv83xT","ulearnet_reim_pilotaje")
    cursor = db.cursor()
    return cursor

#INICIO QUERYS GENERALES

def get_date_param(request):

    date = ''

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_inicio >= TIMESTAMP("' + start + '") && a.datetime_termino <= TIMESTAMP("' + end + '")) &&'

    return date

def get_date_param_alumno_respuesta_actividad(request):

    date = ''

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    return date
    
def get_date_param_tiempoxactividad(request):

    date = ''

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.inicio >= TIMESTAMP("' + start + '") && a.final <= TIMESTAMP("' + end + '")) &&'

    return date

def get_time_query(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND c.id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND co.id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.usuario_id = " + request.GET.get('student')

    date = get_date_param(request)

    start_base = "SELECT u.id, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre_alumno, IF (ROUND((SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))))/60<1, 1,ROUND(SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))/60)) as total_horas, co.nombre as Colegio, concat(n.nombre, c.nombre) as Curso FROM asigna_reim_alumno a, usuario u, pertenece p , nivel n , curso c, colegio co WHERE" + date
    final_base = ' n.id=p.nivel_id and p.curso_id = c.id and  a.usuario_id = u.id and p.usuario_id=u.id and co.id = p.colegio_id AND p.colegio_id IN (SELECT colegio_id FROM pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND p.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

    return start_base + final_base

def get_session_query(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.usuario_id = " + request.GET.get('student')

    date = get_date_param(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.usuario_id) AS Sesiones, b.colegio_id, b.curso_id FROM asigna_reim_alumno a, usuario u, pertenece b WHERE' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

    return start_base + final_base
#sesiones tam
def get_session_PS_query(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.usuario_id = " + request.GET.get('student')

    date = get_date_param(request)

    start_base = 'SELECT a.sesion_id AS Sesiones FROM asigna_reim_alumno a, usuario u, pertenece b WHERE' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' '

    return start_base + final_base

def get_touch_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND a.id_actividad=' + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.id_user = " + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_alumnos(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.usuario_id) AS Sesiones, b.colegio_id, b.curso_id FROM asigna_reim_alumno a, usuario u, pertenece b WHERE' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'
    cursor.execute(start_base + final_base)
    usuarios = str(((len(cursor.fetchall())*40)+20))
    return usuarios 

# FIN QUERYS GENERALES

#INICIO QUERYS CLEAN OCEAN

#CANTIDAD DE COLISIONES
def get_colision_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS colisiones, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND a.correcta=3 GROUP BY u.id'
    return start_base + final_base


#CORRECTAS E INCORRECTAS

def get_corrects_incorrects_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.id_user = " + request.GET.get('student')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(correcta=1,1,NULL)) Correctas, count(if(correcta=0,1,NULL)) Incorrectas FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.id'
    return start_base + final_base

#CORRECTAS GENERALES
def get_corrects_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(correcta=1,1,NULL)) Correctas FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.id'
    return start_base + final_base

def get_incorrects_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(correcta=0,1,NULL)) Incorrectas FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=0 GROUP BY u.id'
    return start_base + final_base

def get_jumps_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS saltos, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=4 GROUP BY u.id'
    return start_base + final_base

def get_analytics_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if((a.id_actividad=3007 and correcta=1) or (a.id_actividad=3004 and correcta=1) or (a.id_actividad=3002 and correcta=1),1,NULL)) CorrectaAct1, count(if((a.id_actividad=3003 and correcta=1) or (a.id_actividad=3005 and correcta=1) ,1,NULL)) CorrectaAct2 FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.id'
    return start_base + final_base

def get_incorrects_act1_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS saltos, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=0 AND a.id_actividad = 3004 GROUP BY u.id'
    return start_base + final_base

def get_corrects_act2_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS saltos, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=1 AND a.id_actividad = 3007 GROUP BY u.id'
    return start_base + final_base

def get_incorrects_act2_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS saltos, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=0 AND a.id_actividad = 3007 GROUP BY u.id'
    return start_base + final_base

def get_exit_lab(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre as Destino, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' e.id=a.id_elemento and id_user="' + request.GET.get('student') + '" AND id_actividad=3004 and a.id_elemento>=3049 and a.id_elemento<=3052 group by a.id_elemento'
    return start_base + final_base

def get_touch_animals_co(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Animal from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + ' and (id_elemento = 3012 or (id_elemento >= 3021 && id_elemento <= 3039) or (id_elemento >=3061 && id_elemento <= 3064) or id_elemento=3017 or id_elemento=3056) and correcta=2 group by id_elemento'
    return start_base + final_base

def get_touch_trash_co(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Animal from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento = 3019 or (id_elemento >= 3040 and id_elemento <= 3044)) and correcta=2 group by id_elemento '
    return start_base + final_base

def get_cant_touch_act_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT o.id, o.nombre, count(o.id) AS actividades FROM actividad o, alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_actividad=o.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND o.id>3000 AND o.id<3007 GROUP BY o.id'
    return start_base + final_base

def get_colision_trash(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = ' a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and correcta=3 group by id_elemento;'
    return start_base + final_base

def get_touch_all_animals(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and (id_elemento = 3012 or (id_elemento >= 3021 && id_elemento <= 3039) or (id_elemento >=3061 && id_elemento <= 3064) or id_elemento=3017 or id_elemento=3056) and correcta=2 group by id_elemento;'
    return start_base + final_base

def get_touch_all_trash(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and correcta=2 and (id_elemento=3019 or (id_elemento>=3041 and id_elemento<=3044) or (id_elemento>=3068 and id_elemento<=3069)) group by id_elemento;'
    return start_base + final_base

def get_exits_lab_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and id_actividad=3004 and (id_elemento>=3049 and id_elemento<=3052) group by id_elemento;'
    return start_base + final_base

def get_buttons_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and correcta=2 and (id_elemento=3013 or id_elemento=3067 or (id_elemento>=3000 and id_elemento<=3002) or (id_elemento>=3007 and id_elemento<=3009)) group by id_elemento;'
    return start_base + final_base

def get_trash_clean_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_user, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and id_elemento=3041 group by id_user;'
    return start_base + final_base

def get_corrects_student_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    # if request.GET.get('course') and request.GET.get('course') != '0':
    #     query_params += " AND b.curso_id = " + request.GET.get('course')
    # if request.GET.get('school') and request.GET.get('school') != '0':
    #     query_params += " AND b.colegio_id = " + request.GET.get('school')
    # if request.GET.get('activity') and request.GET.get('activity') != '0':
    #     query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select a.id_user, ac.nombre as Actividad, count(if(a.correcta=1,1,NULL)) Correcta, count(if(a.correcta=0,1,NULL)) Incorrecta FROM alumno_respuesta_actividad a, actividad ac where' + date
    final_base = '  ac.id=a.id_actividad && a.id_user="' + request.GET.get('student') + '" ' + query_params + ' and a.id_actividad>= 3002 and a.id_actividad<=3007 group by ac.nombre;'
    return start_base + final_base


def get_time_act_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.actividad_id = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.usuario_id = " + request.GET.get('student')

    date = get_date_param_tiempoxactividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, IF (ROUND((SUM(TIMESTAMPDIFF(SECOND, a.inicio, a.final))))/60<1, 1,ROUND(SUM(TIMESTAMPDIFF(SECOND, a.inicio, a.final))/60)) as total_min FROM tiempoxactividad a, usuario u, pertenece b , nivel n , curso c, colegio co WHERE' + date
    final_base = ' n.id=b.nivel_id and b.curso_id = c.id and a.usuario_id = u.id and b.usuario_id=u.id and co.id = b.colegio_id' + query_params + ' group by u.id;'
    return start_base + final_base


#FIN QUERYS CLEAN OCEAN

#INICIO QUERYS MUNDO ANIMAL 
def get_piezas(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS piezas, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' and ((a.correcta>9 and a.correcta<100) || (a.id_elemento = 35 and a.id_actividad = 5) || (a.id_elemento = 32 and a.id_actividad = 6)) GROUP BY u.id;'
    return start_base + final_base

def get_malas(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS malas, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND (a.correcta=0 OR a.correcta>999) GROUP BY u.id'

    return start_base + final_base

def get_animals(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT e.id, e.nombre, count(e.id) AS animales FROM elemento e, alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND e.id>10 AND e.id<26 GROUP BY e.id'
    return start_base + final_base

def get_actividades(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param(request)

    start_base = 'SELECT o.id, o.nombre, count(o.id) AS cantidad FROM actividad o WHERE'
    final_base = ' o.id>0 AND o.id<8 '
    cursor.execute(start_base + final_base)
    actividades = str(((len(cursor.fetchall())*40)+20))
    return actividades 
    
def get_cant_touch(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT o.id, o.nombre, count(o.id) AS actividades FROM actividad o, alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_actividad=o.id && a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND o.id>0 AND o.id<8 GROUP BY o.id'
    return start_base + final_base

def get_interaccion(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND e.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND e.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT c.usuario_id, concat(d.nombres, " ", d.apellido_paterno," ", d.apellido_materno) as Nombre , count(a.id_reim) as Cantidad FROM alumno_respuesta_actividad a, `Avatar-Sesion` b, asigna_reim_alumno c, usuario d, pertenece e where' + date
    final_base = ' e.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND e.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND c.usuario_id = d.id and c.usuario_id = e.usuario_id and a.correcta = b.elemento_id and b.asigna_reim_alumno_sesion_id = c.sesion_id and a.datetime_touch > c.datetime_inicio and a.datetime_touch < c.datetime_termino and correcta >9 and correcta<100 group by c.usuario_id;'
    return start_base + final_base

def get_tiempoact(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND e.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND e.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.usuario_id=' + request.GET.get('student')
        
    date = get_date_param_tiempoxactividad(request)

    start_base = 'SELECT a.actividad_id, b.nombre, round((sum(timestampdiff(minute, inicio, final))/60)) as tiempo FROM tiempoxactividad a, actividad b, pertenece e where'
    final_base = ' e.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND e.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.actividad_id = b.id group by actividad_id;'
    return start_base + final_base

# Avance en query tiempo total del curso por actividad
# SELECT t.id, t.inicio, t.final, t.actividad_id, t.usuario_id, (sum(timestampdiff(minute, inicio, final)))/60 FROM tiempoxactividad t, actividad b, pertenece e where e.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="163465639") AND e.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "163465639")) AND t.reim_id = 1 AND e.curso_id = 5 AND e.colegio_id = 3 AND t.actividad_id = b.id group by usuario_id;

def get_analytics1_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
     
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=7,1,NULL)) Actividad1, count(if(a.id_elemento=8,1,NULL)) Actividad2, count(if(a.id_elemento=9,1,NULL)) Actividad3, count(if(a.id_elemento=10,1,NULL)) Actvidad4, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b where' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'
    return start_base + final_base

def get_tiempo_total_act(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.actividad_id = " + request.GET.get('activity')

    date = get_date_param_tiempoxactividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, IF (ROUND((SUM(TIMESTAMPDIFF(SECOND, a.inicio, a.final))))/60<1, 1,ROUND(SUM(TIMESTAMPDIFF(SECOND, a.inicio, a.final))/60)) as total_min FROM tiempoxactividad a, usuario u, pertenece b , nivel n , curso c, colegio co WHERE' + date
    final_base = ' n.id=b.nivel_id and b.curso_id = c.id and a.usuario_id = u.id and b.usuario_id=u.id and co.id = b.colegio_id' + query_params + ' group by u.id;'
    return start_base + final_base

def get_audios(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.id_elemento) AS audios, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND (a.id_elemento = 28 OR a.id_elemento = 36 OR a.id_elemento = 48 OR a.id_elemento = 52 OR a.id_elemento = 63 OR a.id_elemento = 64 OR a.id_elemento = 65 OR a.id_elemento = 66 ) GROUP BY u.id'
    return start_base + final_base



#FIN QUERYS MUNDO ANIMAL 

#INICIO QUERYS PLUS SPACE
def get_completa_incompleta_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.actividad_id = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.usuario_id=' + request.GET.get('student')

    date = get_date_param_tiempoxactividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.causa=2,1,NULL)) completas, count(if(a.causa=1,1,NULL)) incompletas, count(if(a.causa=0,1,NULL)) inactividad  FROM tiempoxactividad a, usuario u, pertenece b WHERE ' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id' + query_params + ' GROUP BY u.apellido_paterno'
    return start_base + final_base
def get_elementos_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=2018,1,NULL)) planeta, count(if(a.id_elemento=2019,1,NULL)) planetaCS, count(if(a.id_elemento=2020,1,NULL)) planetaCA , count(if(a.id_elemento=2021,1,NULL)) estrella, count(if(a.id_elemento=2022,1,NULL)) supernova, count(if(a.id_elemento=2023,1,NULL)) nebulosa, count(if(a.id_elemento=2024,1,NULL)) galaxia FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base

def get_elementos_alu_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS ocurrecias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND (a.id_elemento=2018 OR a.id_elemento=2019 OR a.id_elemento=2020 OR a.id_elemento=2021 OR a.id_elemento=2022 OR a.id_elemento=2023 OR a.id_elemento=2024) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base
    
def get_construccion_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND ( a.id_elemento=2018 OR a.id_elemento=2019 OR a.id_elemento=2020 OR a.id_elemento=2021 OR a.id_elemento=2022 OR a.id_elemento=2023 OR a.id_elemento=2024) '
    
    return start_base + final_base
def get_saltos_analitica_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND a.id_elemento=2070 '
    
    return start_base + final_base
def get_colisiones_analitica_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS ocurrecias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND (a.id_elemento=2091 OR a.id_elemento=2092 OR a.id_elemento=2093 OR a.id_elemento=2094 OR a.id_elemento=2095 OR a.id_elemento=2096 OR a.id_elemento=2097 OR a.id_elemento=2098) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base
def get_puzzle_PS(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND a.id_elemento= 2128 '
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT u.id, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base

def get_ingreso_puzzle_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND a.id_elemento=2031' 
    
    return start_base + final_base

def get_move_element_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, CEILING(a.fila/100), CEILING(a.columna/100) FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' AND (a.id_elemento= 2133 OR a.id_elemento= 2134 OR a.id_elemento= 2135 OR a.id_elemento= 2136 OR a.id_elemento= 2137 OR a.id_elemento= 2138 OR a.id_elemento= 2139)'

    return start_base + final_base

#LABERINTO
def get_posicionamiento_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=2099,1,NULL)) tierra, count(if(a.id_elemento=2100,1,NULL)) neptuno, count(if(a.id_elemento=2101,1,NULL)) jupiter , count(if(a.id_elemento=2102,1,NULL)) saturno, count(if(a.id_elemento=2103,1,NULL)) urano, count(if(a.id_elemento=2104,1,NULL)) venus, count(if(a.id_elemento=2105,1,NULL)) mercurio, count(if(a.id_elemento=2106,1,NULL)) marte FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta = 1 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base

def get_element_colission_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (a.id_elemento= 2091 OR a.id_elemento= 2092 OR a.id_elemento= 2093 OR a.id_elemento= 2094 OR a.id_elemento= 2095 OR a.id_elemento= 2096 OR a.id_elemento= 2097 OR a.id_elemento= 2098)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

def get_element_colission_alu_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (a.id_elemento= 2091 OR a.id_elemento= 2092 OR a.id_elemento= 2093 OR a.id_elemento= 2094 OR a.id_elemento= 2095 OR a.id_elemento= 2096 OR a.id_elemento= 2097 OR a.id_elemento= 2098)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base

#ALTERNATIVAS
def get_jump_alternativas_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2070 AND a.correcta = 1'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    
    #print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

def get_jump_alternativas_alu_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2070 AND a.correcta = 1'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base    

#CUIDA
def get_acierto_cuida_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2120'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    
    #print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

def get_acierto_cuida_alu_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2120'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base
#puzzle
def get_touch_analitica_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, COALESCE(round(count((if(a.id_elemento=2128,1,null)))/count((if (a.id_elemento=2031,1,null)))),0) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base 

def get_name_student(request):
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre FROM  usuario u WHERE u.id= ' + request.GET.get('student')

    return start_base
  
#FIN QUERY PLUS SPACE------------------------
#
#
#INICIO QUERY BUSCANDO EL TESORO PERDIDO

def get_touch_analitica_prueba_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, COALESCE(round(count((if(a.id_elemento=2128,1,null)))/count((if (a.id_elemento=2031,1,null)))),0) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base 

def get_tiempoXact77(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND e.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND e.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.usuario_id=' + request.GET.get('student')
        
    date = get_date_param_tiempoxactividad(request)

    start_base = 'SELECT a.actividad_id, b.nombre, round((sum(timestampdiff(minute, inicio, final))/60)) as tiempo FROM tiempoxactividad a, actividad b, pertenece e where'
    final_base = ' e.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND e.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.actividad_id = b.id group by actividad_id;'
    return start_base + final_base

def get_reconocer_estilo_cognitivo(request):
    curso = get_from_db()
    query_params = ''
    query_id_reim = ''
    query_id_user = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
        query_id_reim = request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND e.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND e.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_id_user = "respuesta.id_user = " + request.GET.get('student') + " and" 

    #print("USER: " + query_id_user)
    #print("\n\nHORA-HORA-HORA\n: ", request.GET.get('clock'))

    query_parte_1 =  " SELECT respuesta.id_actividad, activ.nombre, count(respuesta.correcta) AS acertada, (10 - COUNT(respuesta.correcta )) AS no_acertada " 
    query_parte_2 =  " FROM ulearnet_reim_pilotaje.alumno_respuesta_actividad respuesta, ulearnet_reim_pilotaje.actividad activ " 
    query_parte_3 =  " WHERE respuesta.id_reim = "+ query_id_reim +" and respuesta.id_elemento = 7723 and " 
    query_parte_4 =  query_id_user
    query_parte_5 =  " respuesta.id_actividad = activ.id and " 
    query_parte_6 =  " respuesta.datetime_touch BETWEEN (SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " +query_id_reim+ " AND '2020-05-30 21:58:00' BETWEEN datetime_inicio AND datetime_termino) AND " 
    query_parte_7 =  " (SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " +query_id_reim+ " AND '2020-05-30 21:58:00' BETWEEN datetime_inicio AND datetime_termino) " 
    query_parte_8 =  " GROUP BY respuesta.id_actividad, respuesta.correcta HAVING respuesta.correcta = 1; "

    query_final = query_parte_1 + query_parte_2 + query_parte_3 + query_parte_4 + query_parte_5 + query_parte_6 + query_parte_7 + query_parte_8

    #print("QUERY: " + query_final)
    return query_final


def get_reconocer_estilo_cognitivo_v2(request):
    curso = get_from_db()
    query_params = ''
    query_id_reim = ''
    query_id_user = ''
    filtro_hora = ''
    fecha_inicio = ''
    fecha_final = ''
    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
        query_id_reim = request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND e.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND e.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_id_user = " AND respuesta.id_user = " + request.GET.get('student')
    if request.GET.get('clock') and request.GET.get('clock') != '0':
        filtro_hora =  request.GET.get('clock')
        filtro_hora += ":00"
    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        fecha_inicio = start + " " + filtro_hora
        fecha_final = end + " " + filtro_hora

    print("\n\FECHA: " + fecha_inicio +" \n\n")
    print("\n\nHora: " + filtro_hora+" \n\n")

    query_parte_1 =  "SELECT respuesta.id_actividad, activ.nombre, respuesta.id_elemento, respuesta.correcta " 
    query_parte_2 =  "FROM ulearnet_reim_pilotaje.alumno_respuesta_actividad respuesta, ulearnet_reim_pilotaje.actividad activ " 
    query_parte_3 =  "WHERE respuesta.id_reim = " + query_id_reim + " AND respuesta.id_elemento > 7727 AND respuesta.id_elemento < 7738 " 
    query_parte_4 =  "AND respuesta.id_actividad = activ.id " + query_id_user +" "
    query_parte_5 =  "AND respuesta.datetime_touch BETWEEN (SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " " + query_id_user + " AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino) AND " 
    query_parte_6 =  "(SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " +query_id_reim+ " "+query_id_user+" AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino) " 
    query_parte_7 =  "GROUP BY respuesta.id_actividad, respuesta.id_elemento" 
    query_parte_8 = " ORDER BY respuesta.datetime_touch DESC;"


    query_final = query_parte_1 + query_parte_2 + query_parte_3 + query_parte_4 + query_parte_5 + query_parte_6 + query_parte_7 + query_parte_8

    return query_final


def get_figura_simple_volcan(request, lista):

        #print("\n\nENTRO EN QUERY: ", lista[0], lista[1])    
        curso = get_from_db()
        query_params = ''
        query_id_reim = ''
        query_id_user = ''
        filtro_hora = ''
        fecha_inicio = ''
        fecha_final = ''
        userid = ''
        if request.GET.get('reim') and request.GET.get('reim') != '0':
            query_params += " AND a.reim_id = " + request.GET.get('reim')
            query_id_reim = request.GET.get('reim')
        if request.GET.get('course') and request.GET.get('course') != '0':
            query_params += " AND e.curso_id = " + request.GET.get('course')
        if request.GET.get('school') and request.GET.get('school') != '0':
            query_params += " AND e.colegio_id = " + request.GET.get('school')
        if request.GET.get('student') and request.GET.get('student') != '0':
            query_id_user = " AND respuesta.id_user = " + request.GET.get('student') + " AND respuesta.id_user = u.id "
            userid = request.GET.get('student')
        if request.GET.get('clock') and request.GET.get('clock') != '0':
            filtro_hora =  request.GET.get('clock')
            filtro_hora += ":00"
        if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
         #   print("\n\STAR: " + str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date()) + " \n\n")
         #   print("\n\END: " + str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date()) +" \n\n")
            start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
            end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
            fecha_inicio = start + " " + filtro_hora
            fecha_final = end + " " + filtro_hora
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " " + query_id_user + " AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " +query_id_reim+ " "+query_id_user+" AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
        if request.GET.get('start') and (request.GET.get('start') == 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') == 'dd/mm/aaaa'):
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + "  ORDER BY datetime_inicio desc LIMIT 1  "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " ORDER BY datetime_inicio desc LIMIT 1 "
            print("NO HAY RANGO")

        query_1 = "SELECT DISTINCT respuesta.id_actividad, respuesta.id_elemento, respuesta.datetime_touch, respuesta.correcta, activ.nombre, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre  FROM ulearnet_reim_pilotaje.alumno_respuesta_actividad respuesta, ulearnet_reim_pilotaje.actividad activ, ulearnet_reim_pilotaje.usuario u "
        query_2 = " WHERE respuesta.id_reim = 77 AND respuesta.id_elemento > 7727 AND respuesta.id_elemento < 7738 "
        query_3 = " AND respuesta.id_actividad = " + str(lista[0]) +" " + query_id_user +" AND respuesta.id_actividad = activ.id "
        query_4 = " AND respuesta.datetime_touch BETWEEN (" + query_sesion_inicio  +") AND " 
        query_5 = " (" + query_sesion_fin + ") " 
        query_6 = " ORDER BY respuesta.datetime_touch;"
        query_final = query_1 + query_2 + query_3 + query_4 + query_5 + query_6
        print("\n\n:: " + query_final + "\n\n:: ")

        return query_final


def get_figura_simple_promedio(request, lista):

        #print("\n\nENTRO EN QUERY: ", lista[0], lista[1])    
        curso = get_from_db()
        query_params = ''
        query_id_reim = ''
        query_id_user = ''
        filtro_hora = ''
        fecha_inicio = ''
        fecha_final = ''
        userid = ''
        if request.GET.get('reim') and request.GET.get('reim') != '0':
            query_params += " AND a.reim_id = " + request.GET.get('reim')
            query_id_reim = request.GET.get('reim')
        if request.GET.get('course') and request.GET.get('course') != '0':
            query_params += " AND e.curso_id = " + request.GET.get('course')
        if request.GET.get('school') and request.GET.get('school') != '0':
            query_params += " AND e.colegio_id = " + request.GET.get('school')
        if request.GET.get('student') and request.GET.get('student') != '0':
            query_id_user = " AND respuesta.id_user = " + request.GET.get('student') + " AND respuesta.id_user = u.id "
            userid = request.GET.get('student')
        if request.GET.get('clock') and request.GET.get('clock') != '0':
            filtro_hora =  request.GET.get('clock')
            filtro_hora += ":00"
        if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
         #   print("\n\STAR: " + str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date()) + " \n\n")
         #   print("\n\END: " + str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date()) +" \n\n")
            start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
            end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
            fecha_inicio = start + " " + filtro_hora
            fecha_final = end + " " + filtro_hora
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " " + query_id_user + " AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " +query_id_reim+ " "+query_id_user+" AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
        if request.GET.get('start') and (request.GET.get('start') == 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') == 'dd/mm/aaaa'):
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + "  ORDER BY datetime_inicio desc LIMIT 1  "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " ORDER BY datetime_inicio desc LIMIT 1 "
            print("NO HAY RANGO")

        query_1 = "SELECT DISTINCT respuesta.id_actividad, respuesta.id_elemento, respuesta.datetime_touch, ROUND(AVG(respuesta.correcta)) as correcta, activ.nombre, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre  FROM ulearnet_reim_pilotaje.alumno_respuesta_actividad respuesta, ulearnet_reim_pilotaje.actividad activ, ulearnet_reim_pilotaje.usuario u "
        query_2 = " WHERE respuesta.id_reim = 77 AND respuesta.id_elemento > 7727 AND respuesta.id_elemento < 7738 "
        query_3 = " AND respuesta.id_actividad = " + str(lista[0]) +" " + query_id_user +" AND respuesta.id_actividad = activ.id "
        query_4 = " AND respuesta.datetime_touch BETWEEN (" + query_sesion_inicio  +") AND " 
        query_5 = " (" + query_sesion_fin + ") " 
        query_6 = " GROUP BY respuesta.id_elemento ORDER BY respuesta.datetime_touch;"
        query_final = query_1 + query_2 + query_3 + query_4 + query_5 + query_6

        return query_final

def get_figura_simple_ultimos_registros(request, lista):

        #print("\n\nENTRO EN QUERY: ", lista[0], lista[1])    
        curso = get_from_db()
        query_params = ''
        query_id_reim = ''
        query_id_user = ''
        filtro_hora = ''
        fecha_inicio = ''
        fecha_final = ''
        query_sesion_inicio = ''
        query_sesion_fin = ''
        userid = ''

        if request.GET.get('reim') and request.GET.get('reim') != '0':
            query_params += " AND a.reim_id = " + request.GET.get('reim')
            query_id_reim = request.GET.get('reim')
        if request.GET.get('course') and request.GET.get('course') != '0':
            query_params += " AND e.curso_id = " + request.GET.get('course')
        if request.GET.get('school') and request.GET.get('school') != '0':
            query_params += " AND e.colegio_id = " + request.GET.get('school')
        if request.GET.get('student') and request.GET.get('student') != '0':
            query_id_user = " AND respuesta.id_user = " + request.GET.get('student') + " AND respuesta.id_user = u.id "
            userid = request.GET.get('student')
        if request.GET.get('clock') and request.GET.get('clock') != '0':
            filtro_hora =  request.GET.get('clock')
            filtro_hora += ":00"
        if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
            start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
            end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
            fecha_inicio = start + " " + filtro_hora
            fecha_final = end + " " + filtro_hora
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " " + query_id_user + " AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " +query_id_reim+ " "+query_id_user+" AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
        if request.GET.get('start') and (request.GET.get('start') == 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') == 'dd/mm/aaaa'):
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + "  ORDER BY datetime_inicio desc LIMIT 1  "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " ORDER BY datetime_inicio desc LIMIT 1 "
            print("NO HAY RANGO")

        query_1 = "SELECT DISTINCT respuesta.id_actividad, respuesta.id_elemento, respuesta.datetime_touch, respuesta.correcta, activ.nombre, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre  FROM ulearnet_reim_pilotaje.alumno_respuesta_actividad respuesta, ulearnet_reim_pilotaje.actividad activ, ulearnet_reim_pilotaje.usuario u "
        query_2 = " WHERE respuesta.id_reim = 77 AND respuesta.id_elemento > 7727 AND respuesta.id_elemento < 7738 "
        query_3 = " AND respuesta.id_actividad = " + str(lista[0]) +" " + query_id_user +" AND respuesta.id_actividad = activ.id "
        query_4 = " AND respuesta.datetime_touch BETWEEN (" + query_sesion_inicio  +") AND " 
        query_5 = " (" + query_sesion_fin + ") " 
        query_6 = " ORDER BY respuesta.datetime_touch DESC;"
        query_final = query_1 + query_2 + query_3 + query_4 + query_5 + query_6

        return query_final
#GRAFICOS POR ACTIVIDAD REIM 77
def get_Actividad_Buenas_Mala(request):
        curso = get_from_db()
        query_params = ''
        query_id_reim = ''
        query_id_user = ''
        filtro_hora = ''
        fecha_inicio = ''
        fecha_final = ''
        actividad = ''
        query_sesion_inicio = ''
        query_sesion_fin = ''
        userid = ''

        if request.GET.get('activity') and request.GET.get('activity') != '0':
            actividad = " AND respuesta.id_actividad =  " + request.GET.get('activity')
        if request.GET.get('reim') and request.GET.get('reim') != '0':
            query_params += " AND a.reim_id = " + request.GET.get('reim')
            query_id_reim = request.GET.get('reim')
        if request.GET.get('course') and request.GET.get('course') != '0':
            query_params += " AND e.curso_id = " + request.GET.get('course')
        if request.GET.get('school') and request.GET.get('school') != '0':
            query_params += " AND e.colegio_id = " + request.GET.get('school')
        if request.GET.get('student') and request.GET.get('student') != '0':
            query_id_user = " AND respuesta.id_user = " + request.GET.get('student') + " AND respuesta.id_user = u.id "
            userid = request.GET.get('student') 
        if request.GET.get('clock') and request.GET.get('clock') != '0':
            filtro_hora =  request.GET.get('clock')
            filtro_hora += ":00"
        if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
            start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
            end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
            fecha_inicio = start + " " + filtro_hora
            fecha_final = end + " " + filtro_hora
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " " + query_id_user + " AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " +query_id_reim+ " "+query_id_user+" AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
        if request.GET.get('start') and (request.GET.get('start') == 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') == 'dd/mm/aaaa'):
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + "  ORDER BY datetime_inicio desc LIMIT 1  "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " ORDER BY datetime_inicio desc LIMIT 1 "
            print("NO HAY RANGO")

        query_1 = " SELECT respuesta.id_actividad, respuesta.id_elemento, respuesta.datetime_touch, respuesta.correcta, SUM(IF (respuesta.correcta = 1, 1, 0 )) as completada , SUM(IF (respuesta.correcta = 0, 1, 0 )) as no_completada  ,activ.nombre,  elemento.nombre FROM ulearnet_reim_pilotaje.alumno_respuesta_actividad respuesta, ulearnet_reim_pilotaje.actividad activ, ulearnet_reim_pilotaje.usuario u, ulearnet_reim_pilotaje.elemento elemento  "
        query_2 = " WHERE respuesta.id_reim = 77 AND respuesta.id_elemento > 7727 AND respuesta.id_elemento < 7738 "
        query_3 = " " + actividad + " AND respuesta .id_actividad = activ.id "
        query_4 = query_id_user
        query_5 = " AND respuesta.id_elemento = elemento.id AND respuesta.datetime_touch BETWEEN (" + query_sesion_inicio + ") AND " 
        query_6 = " ("+ query_sesion_fin  +") " 
        query_7 = " GROUP by respuesta.id_elemento ORDER BY respuesta.datetime_touch DESC; "

        #print("\n\n BUENA Y MALA query: "+ query_1 + query_2 + query_3 + query_4 + query_5 + query_6 + query_7)
        return query_1 + query_2 + query_3 + query_4 + query_5 + query_6 + query_7

def get_tiempoact_sesion(request):
    cursor = get_from_db()
    query_params = ''
    query_id_reim = ''
    query_id_user = ''
    query_id_activ = ''
    query_sesion_inicio = ''
    query_sesion_fin = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
        query_id_reim = request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND e.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND e.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.usuario_id=' + request.GET.get('student')
        query_id_user = request.GET.get('student')
    if request.GET.get('clock') and request.GET.get('clock') != '0':
            filtro_hora =  request.GET.get('clock')
            filtro_hora += ":00"
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_id_activ = " and a.actividad_id = " + request.GET.get('activity') 
    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        fecha_inicio = start + " " + filtro_hora
        fecha_final = end + " " + filtro_hora
        query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + query_id_user + " AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
        query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " +query_id_reim+ " AND usuario_id = "+query_id_user+" AND '" + fecha_inicio + "' BETWEEN datetime_inicio AND datetime_termino "
    if request.GET.get('start') and (request.GET.get('start') == 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') == 'dd/mm/aaaa'):
        query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + query_id_user + "  ORDER BY datetime_inicio desc LIMIT 1  "
        query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + query_id_user + " ORDER BY datetime_inicio desc LIMIT 1 "
        print("NO HAY RANGO")
        
    date = get_date_param_tiempoxactividad(request)

    start_base = 'SELECT a.actividad_id, b.nombre, round((sum(timestampdiff(SECOND, inicio, final))/60)) as tiempo FROM tiempoxactividad a, actividad b, pertenece e where'
    intermedio_sesion =  " a.inicio BETWEEN (" +query_sesion_inicio + ") AND  (" +query_sesion_fin+") AND" 
    final_base = ' e.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND e.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.actividad_id = b.id '+ query_id_activ  +' group by actividad_id;'
    
    #print("\n\n TIEMPO Query: " +start_base + intermedio_sesion + final_base)

    return start_base + intermedio_sesion + final_base
#POR ACTIVIDAD
#GRAFICO GENERARL DE RECONOCER ESTILO COGNITIVO
#
#GRAFICOS POR CURSO REIM 77
def get_figura_simple_estandar_por_curso(request, lista, userid):

        print("\n\nENTRO EN QUERY: ", lista[0], lista[1])    
        #print("user: ", userid)
        print("Primero registro")
        curso = get_from_db()
        query_params = ''
        query_id_reim = ''
        query_id_user = ''
        filtro_hora = ''
        fecha_inicio = ''
        fecha_final = ''
        query_sesion_inicio = ''
        query_sesion_fin = ''
        if request.GET.get('reim') and request.GET.get('reim') != '0':
            query_params += " AND a.reim_id = " + request.GET.get('reim')
            query_id_reim = request.GET.get('reim')
        if request.GET.get('course') and request.GET.get('course') != '0':
            query_params += " AND e.curso_id = " + request.GET.get('course')
        if request.GET.get('school') and request.GET.get('school') != '0':
            query_params += " AND e.colegio_id = " + request.GET.get('school')
        if request.GET.get('student') == '0':
            query_id_user = " AND respuesta.id_user = " + str(userid) + " AND respuesta.id_user = u.id "
        if request.GET.get('clock') and request.GET.get('clock') != '0':
            filtro_hora =  request.GET.get('clock')
            filtro_hora += ":00"
        if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
         #   print("\n\STAR: " + str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date()) + " \n\n")
         #   print("\n\END: " + str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date()) +" \n\n")
            start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
            end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
            fecha_inicio = start + " " + filtro_hora
            fecha_final = end + " " + filtro_hora
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " AND datetime_inicio <= '" + fecha_inicio + "' ORDER BY datetime_inicio desc LIMIT 1 "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " AND datetime_inicio <= '" + fecha_inicio + "' ORDER BY datetime_inicio desc LIMIT 1 "
        if request.GET.get('start') and (request.GET.get('start') == 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') == 'dd/mm/aaaa'):
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + "  ORDER BY datetime_inicio desc LIMIT 1  "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " ORDER BY datetime_inicio desc LIMIT 1 "
            print("NO HAY RANGO")

        query_1 = "SELECT DISTINCT respuesta.id_actividad, respuesta.id_elemento, respuesta.datetime_touch, respuesta.correcta, activ.nombre, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre  FROM ulearnet_reim_pilotaje.alumno_respuesta_actividad respuesta, ulearnet_reim_pilotaje.actividad activ, ulearnet_reim_pilotaje.usuario u "
        query_2 = " WHERE respuesta.id_reim = 77 AND respuesta.id_elemento > 7727 AND respuesta.id_elemento < 7738 "
        query_3 = " AND respuesta.id_actividad = " + str(lista[0]) +" AND respuesta.id_user = " + str(userid) +" AND respuesta.id_user = u.id  AND respuesta.id_actividad = activ.id "
        query_4 = " AND respuesta.datetime_touch BETWEEN (" +query_sesion_inicio+ " ) AND " 
        query_5 = " ( "+query_sesion_fin+" ) " 
        query_6 = " ORDER BY respuesta.datetime_touch;"
        query_final = query_1 + query_2 + query_3 + query_4 + query_5 + query_6

        print("\n\nQUERY por cursor: " + query_final)

        return query_final

def get_figura_simple_promedio_por_curso(request, lista, userid):

        #print("\n\nENTRO EN QUERY: ", lista[0], lista[1])
        print("Promedio registro")    
        curso = get_from_db()
        query_params = ''
        query_id_reim = ''
        query_id_user = ''
        filtro_hora = ''
        fecha_inicio = ''
        fecha_final = ''
        query_sesion_inicio = ''
        query_sesion_fin = ''
        if request.GET.get('reim') and request.GET.get('reim') != '0':
            query_params += " AND a.reim_id = " + request.GET.get('reim')
            query_id_reim = request.GET.get('reim')
        if request.GET.get('course') and request.GET.get('course') != '0':
            query_params += " AND e.curso_id = " + request.GET.get('course')
        if request.GET.get('school') and request.GET.get('school') != '0':
            query_params += " AND e.colegio_id = " + request.GET.get('school')
        if request.GET.get('student') and request.GET.get('student') != '0':
            query_id_user = " AND respuesta.id_user = " + request.GET.get('student') + " AND respuesta.id_user = u.id "
        if request.GET.get('clock') and request.GET.get('clock') != '0':
            filtro_hora =  request.GET.get('clock')
            filtro_hora += ":00"
        if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
         #   print("\n\STAR: " + str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date()) + " \n\n")
         #   print("\n\END: " + str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date()) +" \n\n")
            start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
            end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
            fecha_inicio = start + " " + filtro_hora
            fecha_final = end + " " + filtro_hora
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " AND datetime_inicio <= '" + fecha_inicio + "' ORDER BY datetime_inicio desc LIMIT 1 "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " AND datetime_inicio <= '" + fecha_inicio + "' ORDER BY datetime_inicio desc LIMIT 1 "
        if request.GET.get('start') and (request.GET.get('start') == 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') == 'dd/mm/aaaa'):
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + "  ORDER BY datetime_inicio desc LIMIT 1  "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " ORDER BY datetime_inicio desc LIMIT 1 "
            print("NO HAY RANGO")

        query_1 = "SELECT DISTINCT respuesta.id_actividad, respuesta.id_elemento, respuesta.datetime_touch, ROUND(AVG(respuesta.correcta)) as correcta, activ.nombre, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre  FROM ulearnet_reim_pilotaje.alumno_respuesta_actividad respuesta, ulearnet_reim_pilotaje.actividad activ, ulearnet_reim_pilotaje.usuario u "
        query_2 = " WHERE respuesta.id_reim = 77 AND respuesta.id_elemento > 7727 AND respuesta.id_elemento < 7738 "
        query_3 = " AND respuesta.id_actividad = " + str(lista[0]) +" AND respuesta.id_user = " + str(userid) +" AND respuesta.id_user = u.id AND respuesta.id_actividad = activ.id "
        query_4 = " AND respuesta.datetime_touch BETWEEN (" +query_sesion_inicio+ ") AND " 
        query_5 = " ("+query_sesion_fin+" ) " 
        query_6 = " GROUP BY respuesta.id_elemento ORDER BY respuesta.datetime_touch;"
        query_final = query_1 + query_2 + query_3 + query_4 + query_5 + query_6

        return query_final

def get_figura_simple_ultimos_registros_por_curso(request, lista, userid):

        #print ultimo registro
        print("Ultimo registro")
        #print("\n\nENTRO EN QUERY: ", lista[0], lista[1])    
        curso = get_from_db()
        query_params = ''
        query_id_reim = ''
        query_id_user = ''
        filtro_hora = ''
        fecha_inicio = ''
        fecha_final = ''
        query_sesion_inicio = ''
        query_sesion_fin = ''
        if request.GET.get('reim') and request.GET.get('reim') != '0':
            query_params += " AND a.reim_id = " + request.GET.get('reim')
            query_id_reim = request.GET.get('reim')
        if request.GET.get('course') and request.GET.get('course') != '0':
            query_params += " AND e.curso_id = " + request.GET.get('course')
        if request.GET.get('school') and request.GET.get('school') != '0':
            query_params += " AND e.colegio_id = " + request.GET.get('school')
        if request.GET.get('student') and request.GET.get('student') != '0':
            query_id_user = " AND respuesta.id_user = " + request.GET.get('student') + " AND respuesta.id_user = u.id "
        if request.GET.get('clock') and request.GET.get('clock') != '0':
            filtro_hora =  request.GET.get('clock')
            filtro_hora += ":00"
        if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
            print("SI HAY RANGO")
            start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
            end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
            fecha_inicio = start + " " + filtro_hora
            fecha_final = end + " " + filtro_hora
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " AND datetime_inicio <= '" + fecha_inicio + "' ORDER BY datetime_inicio desc LIMIT 1 "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " AND datetime_inicio <= '" + fecha_inicio + "' ORDER BY datetime_inicio desc LIMIT 1 "
        if request.GET.get('start') and (request.GET.get('start') == 'dd/mm/aaaa') or request.GET.get('end') and (request.GET.get('end') == 'dd/mm/aaaa'):
            query_sesion_inicio = " SELECT sesion.datetime_inicio FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + "  ORDER BY datetime_inicio desc LIMIT 1  "
            query_sesion_fin = " SELECT sesion.datetime_termino FROM ulearnet_reim_pilotaje.asigna_reim_alumno sesion WHERE reim_id = " + query_id_reim + " AND usuario_id = " + str(userid) + " ORDER BY datetime_inicio desc LIMIT 1 "
            print("NO HAY RANGO")

        query_1 = "SELECT DISTINCT respuesta.id_actividad, respuesta.id_elemento, respuesta.datetime_touch, respuesta.correcta, activ.nombre, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre  FROM ulearnet_reim_pilotaje.alumno_respuesta_actividad respuesta, ulearnet_reim_pilotaje.actividad activ, ulearnet_reim_pilotaje.usuario u "
        query_2 = " WHERE respuesta.id_reim = 77 AND respuesta.id_elemento > 7727 AND respuesta.id_elemento < 7738 "
        query_3 = " AND respuesta.id_actividad = " + str(lista[0]) +" AND respuesta.id_user = " + str(userid) +" AND respuesta.id_user = u.id  AND respuesta.id_actividad = activ.id "
        query_4 = " AND respuesta.datetime_touch BETWEEN (" +query_sesion_inicio+ ") AND " 
        query_5 = " ( "+query_sesion_fin+" ) " 
        query_6 = " ORDER BY respuesta.datetime_touch DESC;"
        query_final = query_1 + query_2 + query_3 + query_4 + query_5 + query_6

        #print("\n\n: " + query_final)
        return query_final
#GRAFICOS POR CURSO REIM 77

#FIN QUERY BUSCANDO EL TESORO PERDIDO