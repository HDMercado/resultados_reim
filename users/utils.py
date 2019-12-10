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

def get_time_query(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND c.id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND co.id = " + request.GET.get('school')

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

    date = get_date_param(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.usuario_id) AS Sesiones, b.colegio_id, b.curso_id FROM asigna_reim_alumno a, usuario u, pertenece b WHERE' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

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
    print(query_params)

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
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.correcta=3 GROUP BY u.id'
    return start_base + final_base

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
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS colisiones, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.correcta=1 GROUP BY u.id'
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
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS colisiones, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.correcta=0 GROUP BY u.id'
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
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.correcta=4 GROUP BY u.id'
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
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_actividad=3007 and correcta=1,1,NULL)) CorrectaAct1, count(if(a.id_actividad=3007 and correcta=0,1,NULL)) IncorrectaAct1, count(if(a.id_actividad=3003 and correcta=1,1,NULL)) CorrectaAct2, count(if(a.id_actividad=3003 and correcta=0,1,NULL)) IncorrectaAct1, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'
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
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.correcta=0 AND a.id_actividad = 3004 GROUP BY u.id'
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
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.correcta=1 AND a.id_actividad = 3007 GROUP BY u.id'
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
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.correcta=0 AND a.id_actividad = 3007 GROUP BY u.id'
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
    print (start_base + final_base)
    return start_base + final_base

def get_touch_trash_co(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Animal from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento = 3019 or (id_elemento >= 3040 and id_elemento <= 3044)) and correcta=2 group by id_elemento '
    print (start_base + final_base)
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
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.id_elemento=32 GROUP BY u.id'
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

#FIN QUERYS MUNDO ANIMAL 

#INICIO QUERYS PLUS SPACE
def get_move_element_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (a.id_elemento= 2133 OR a.id_elemento= 2134 OR a.id_elemento= 2135 OR a.id_elemento= 2136 OR a.id_elemento= 2137 OR a.id_elemento= 2138 OR a.id_elemento= 2139)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base
def get_element_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (a.id_elemento= 2018 OR a.id_elemento= 2019 OR a.id_elemento= 2020 OR a.id_elemento= 2021 OR a.id_elemento= 2022 OR a.id_elemento= 2023 OR a.id_elemento= 2024)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_planet_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND a.id_actividad= 9'
        query_params += ' AND a.id_elemento= 2018'
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_planet_satelite_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND a.id_actividad= 9'
        query_params += ' AND a.id_elemento= 2019'
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_planet_ring_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND a.id_actividad= 9'
        query_params += ' AND a.id_elemento= 2020'
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_star_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND a.id_actividad= 9'
        query_params += ' AND a.id_elemento= 2021'
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_supernova_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND a.id_actividad= 9'
        query_params += ' AND a.id_elemento= 2022'
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_nebulosa_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND a.id_actividad= 9'
        query_params += ' AND a.id_elemento= 2023'
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_galaxy_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND a.id_actividad= 9'
        query_params += ' AND a.id_elemento= 2024'
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_aceptar_creacion_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
        query_params += ' AND (a.id_elemento= 2018 OR a.id_elemento= 2019 OR a.id_elemento= 2020 OR a.id_elemento= 2021 OR a.id_elemento= 2022 OR a.id_elemento= 2023 OR a.id_elemento= 2024)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_volver_creacion_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2014'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_ingresar_creacion_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += ' AND b.colegio_id = ' + request.GET.get('school') + ' AND a.id_elemento= 2028'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

#LABERINTO
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
    #print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base
def get_aceptar_laberinto_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " +  request.GET.get('school')+' AND a.id_elemento= 2142'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_volver_laberinto_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2001'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_ingresar_laberinto_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += ' AND b.colegio_id = ' + request.GET.get('school') + ' AND a.id_elemento= 2033'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base
def get_correctas_alternativas_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_actividad = 11 AND (a.id_elemento=2037 OR a.id_elemento=2038 OR a.id_elemento=2039 OR a.id_elemento=2040) AND a.correcta = 1'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base
def get_incorrectas_alternativas_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_actividad = 11 AND (a.id_elemento=2037 OR a.id_elemento=2038 OR a.id_elemento=2039 OR a.id_elemento=2040) AND a.correcta = 0'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_aceptar_alternativas_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2131'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_volver_alternativas_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2035'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_ingresar_alternativas_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += ' AND b.colegio_id = ' + request.GET.get('school') + ' AND a.id_elemento= 2029'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base
#BUSCA
def get_correctas_busca_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_actividad=12 AND a.correcta=1'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base
def get_incorrectas_busca_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_actividad=12 AND a.correcta=0'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_aceptar_busca_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2140'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_volver_busca_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2054'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_ingresar_busca_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += ' AND b.colegio_id = ' + request.GET.get('school') + ' AND a.id_elemento= 2030'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base
def get_aceptar_cuida_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2141'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_volver_cuida_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2108'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_ingresar_cuida_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += ' AND b.colegio_id = ' + request.GET.get('school') + ' AND a.id_elemento= 2032'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base
#PUZZLE
def get_aceptar_puzzle_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2078'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_volver_puzzle_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2123'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_ingresar_puzzle_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += ' AND b.colegio_id = ' + request.GET.get('school') + ' AND a.id_elemento= 2031'
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
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base
    
#FIN QUERY PLUS SPACE------------------------