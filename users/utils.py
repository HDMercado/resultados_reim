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

#INICIO DIA MUNDIAL

### GRAN GRAFICO ###

#TRAER NIÑOS
def get_alumnos_and_id(request):
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
    return start_base + final_base



#LABERINTO POR NIÑO
def get_laberinto_porniño(request, id_niño):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    query_params += ' AND a.id_user=' + str(id_niño) 

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS ocurrecias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND (a.id_elemento=4064 or a.id_elemento=4074 or a.id_elemento=4084 or a.id_elemento=4065 or a.id_elemento=4075 or a.id_elemento=4085) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base

#ABEJAS POR NIÑO
def get_abejas_porniño(request, id_niño):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    query_params += ' AND a.id_user=' + str(id_niño) 

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS ocurrecias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND (a.id_elemento=4154 or a.id_elemento = 4155) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base

#LUCES POR NIÑO
def get_luces_porniño(request, id_niño):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    query_params += ' AND a.id_user=' + str(id_niño) 

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS ocurrecias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND (a.id_elemento=4093 or a.id_elemento = 4095 or a.id_elemento = 4097) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base

#OCEANO RIO POR NIÑO
def get_oceanorio_porniño(request, id_niño):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    query_params += ' AND a.id_user=' + str(id_niño) 

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS ocurrecias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND (a.id_elemento=4099 or a.id_elemento = 4109) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base

#Correcta_Incorrecta Dia mundial
def get_ganar_perder_DM_Quest(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=4162,1,NULL)) correcta, count(if(a.id_elemento=4163,1,NULL)) incorrecta FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base


###JUEGO LABERINTO###

#Ganar Perder
def get_ganar_perder_lab(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=4157,1,NULL)) fruta, count(if(a.id_elemento=4158,1,NULL)) chatarra FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base

#Muro vs Hoyo
def get_colision_muro_hoyo(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=4064 or a.id_elemento=4074 or a.id_elemento=4084,1,NULL)) muro, count(if(a.id_elemento=4065 or a.id_elemento=4075 or a.id_elemento=4085,1,NULL)) hoyo FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'
    return start_base + final_base

#Colisiones en el tiempo
def get_colisiones_analitica_DM(request):

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
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND (a.id_elemento=4064 OR a.id_elemento=4065 OR a.id_elemento=4074 OR id_elemento=4075 OR id_elemento=4084 OR id_elemento=4085 OR id_elemento=4157 OR id_elemento=4158) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base

#tipo de basura    
def get_tipo_basura(request):
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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if((a.id_elemento=4100 or a.id_elemento=4114),1,NULL)) bolsa, count(if((a.id_elemento=4101 or a.id_elemento=4115),1,NULL)) botella, count(if((a.id_elemento=4102 or a.id_elemento=4116),1,NULL)) mancha, count(if((a.id_elemento=4103 or a.id_elemento=4117),1,NULL)) red, count(if((a.id_elemento=4104 or a.id_elemento=4118),1,NULL)) zapato FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'
    return start_base + final_base

#animales por nivel
def get_animales_nivel(request):
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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if((a.id_elemento=4105 or a.id_elemento=4106 or a.id_elemento=4107 or a.id_elemento=4108),1,NULL)) animalesoceano, count(if((a.id_elemento=4109 or a.id_elemento=4110 or a.id_elemento=4111 or a.id_elemento=4112 or a.id_elemento=4113),1,NULL)) animalesrio, count(if((a.id_elemento=4100 or a.id_elemento=4101 or a.id_elemento=4102 or a.id_elemento=4103 or a.id_elemento=4104),1,NULL)) basuraoceano, count(if((a.id_elemento=4114 or a.id_elemento=4115 or a.id_elemento=4116 or a.id_elemento=4117 or a.id_elemento=4118),1,NULL)) basurario FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

#touch y luces correctas
def get_touches_luces(request):
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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if((a.id_elemento=4093 or a.id_elemento=4095 or a.id_elemento=4097),1,NULL)) touches, count(if((a.id_elemento=4094 or a.id_elemento=4065 or a.id_elemento=4098),1,NULL)) lucescorrectas FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

#llega a la miel, cae o choca
def get_miel_cae_choca(request):
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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if((a.id_elemento=4153),1,NULL)) colisionpanal, count(if((a.id_elemento=4154),1,NULL)) colisionsuelo, count(if((a.id_elemento=4155),1,NULL)) colisionosoavispa FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

#animales salvados

def get_animales_salvados(request):
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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if((a.id_elemento=4034),1,NULL)) ballena, count(if((a.id_elemento=4035),1,NULL)) oso, count(if((a.id_elemento=4036),1,NULL)) pinguino, count(if((a.id_elemento=4037),1,NULL)) pepino, count(if((a.id_elemento=4038),1,NULL)) pajaro, count(if((a.id_elemento=4039),1,NULL)) foca, count(if((a.id_elemento=4041),1,NULL)) tigre, count(if((a.id_elemento=4042),1,NULL)) cocodrilo, count(if((a.id_elemento=4043),1,NULL)) mono, count(if((a.id_elemento=4044),1,NULL)) serpiente, count(if((a.id_elemento=4045),1,NULL)) Perezoso, count(if((a.id_elemento=4046 or a.id_elemento=4051),1,NULL)) rana, count(if((a.id_elemento=4048),1,NULL)) lagartija, count(if((a.id_elemento=4049 or a.id_elemento=4050 or a.id_elemento=4056),1,NULL)) lemur, count(if((a.id_elemento=4052),1,NULL)) camaleon, count(if((a.id_elemento=4053),1,NULL)) tortuga, count(if((a.id_elemento=4054),1,NULL)) leon, count(if((a.id_elemento=4055),1,NULL)) fosa FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

#animales salvados por nivel

def get_animales_salvados_pornivel(request):
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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if((a.id_elemento=4034 or a.id_elemento=4035 or a.id_elemento=4036 or a.id_elemento=4037 or a.id_elemento=4038 or a.id_elemento=4039),1, NULL)) animalesantartica, count(if((a.id_elemento=4041 or a.id_elemento=4042 or a.id_elemento=4043 or a.id_elemento=4044 or a.id_elemento=4045 or a.id_elemento=4046),1,NULL)) animalesselva, count(if((a.id_elemento=4048 or a.id_elemento=4049 or a.id_elemento=4050 or a.id_elemento=4051 or a.id_elemento=4052 or a.id_elemento=4053 or a.id_elemento=4054 or a.id_elemento=4055 or a.id_elemento=4056),1,NULL)) animalesmadagascar FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

#instruccion seguida vs instruccion perdida

def get_correcta_incorrecta_arbol(request):
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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if((a.id_elemento=4160),1, NULL)) perdida, count(if((a.id_elemento=4161),1, NULL)) atino FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base
  
  #Cuantas veces hizo crecer el arbol

def get_crecimiento_arbol(request):

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
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND (a.id_elemento=4159) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base

#FIN QUERYS DÍA MUNDIAL

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

def get_tiempoactDM(request):
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

    start_base = 'SELECT a.actividad_id, b.nombre, round((sum(timestampdiff(minute, inicio, final))/30)) as tiempo FROM tiempoxactividad a, actividad b, pertenece e where'
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
    print(query_params)

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

#INICIO REIM ID = 77, NOMBRE = BUSCANDO EL TESORO PERDIDO

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

#FIN REIM ID = 77, NOMBRE = BUSCANDO EL TESORO PERDIDO
#####BEGIN BUILD YOUR CITY#####
##GENERAL QUERYS:
def get_number_of_sessions(request):
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

def get_playtime(request):
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

    start_base = "SELECT u.id, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre_alumno, IF (ROUND((SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))))/60<1, 1,ROUND(SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))/60)) as minutos_juego, co.nombre as Colegio, concat(n.nombre, c.nombre) as Curso FROM asigna_reim_alumno a, usuario u, pertenece p , nivel n , curso c, colegio co WHERE" + date
    final_base = ' n.id=p.nivel_id and p.curso_id = c.id and  a.usuario_id = u.id and p.usuario_id=u.id and co.id = p.colegio_id AND p.colegio_id IN (SELECT colegio_id FROM pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND p.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

    return start_base + final_base

def get_touch_count(request):
    
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
    print(query_params)

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_activities_played_counter(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
        
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT a.id_elemento as idElemento, count(1) as counter FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + ' AND a.id_elemento IN (27101,27102,27103)' + query_params + ' GROUP BY a.id_elemento;'

    return start_base + final_base

##CONSTRUCTION MAP:

def get_built_elements_counter_per_category(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, COUNT(if(a.id_elemento IN (27104, 27105, 27106, 27107) ,1,NULL)) CantidadEdificios, COUNT(if(a.id_elemento IN (27108, 27109, 27110, 27111) ,1,NULL)) CantidadAdornos, COUNT(if(a.id_elemento IN (27112, 27113, 27114, 27115) ,1,NULL)) CantidadAutomoviles FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.id'
    
    return start_base + final_base

def get_built_elements_counter(request):

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

    start_base = ' SELECT a.id_elemento, COUNT(1) counter FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27104,27105,27106,27107,27108,27109,27110,27111,27112,27113,27114,27115)' + ' GROUP BY a.id_elemento ORDER BY a.id_elemento'
    
    return start_base + final_base

##CINEMA:
def getNumberOfEntrances(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  Count(id_elemento) as NumberOfEntrances FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27243) ' + ' GROUP BY u.id'
    
    return start_base + final_base

def getCinema_CompleteVsIncomplete(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Completes, COUNT(if(a.correcta = 0 ,1,NULL)) AS Incompletes FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento = 27243 ' + ' GROUP BY u.id'
    
    return start_base + final_base

def getCinema_SuccessVsFailure(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27201, 27202, 27203, 27204, 27205, 27206, 27207, 27208, 27209, 27210, 27211, 27212, 27213, 27214, 27215, 27216, 27217, 27218, 27219, 27220, 27221, 27222, 27223, 27224, 27225, 27226, 27227, 27228, 27229, 27230, 27231, 27232, 27233, 27234, 27235, 27236, 27237, 27238, 27239, 27240, 27241, 27242) ' + ' GROUP BY u.id'
    
    return start_base + final_base

def getCinema_SuccessVsFailureGeneral(request):
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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27201, 27202, 27203, 27204, 27205, 27206, 27207, 27208, 27209, 27210, 27211, 27212, 27213, 27214, 27215, 27216, 27217, 27218, 27219, 27220, 27221, 27222, 27223, 27224, 27225, 27226, 27227, 27228, 27229, 27230, 27231, 27232, 27233, 27234, 27235, 27236, 27237, 27238, 27239, 27240, 27241, 27242) ' 
    
    return start_base + final_base

def getCinema_SuccessPercentageInTime(request):

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
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS Fecha, COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND a.id_elemento IN (27201, 27202, 27203, 27204, 27205, 27206, 27207, 27208, 27209, 27210, 27211, 27212, 27213, 27214, 27215, 27216, 27217, 27218, 27219, 27220, 27221, 27222, 27223, 27224, 27225, 27226, 27227, 27228, 27229, 27230, 27231, 27232, 27233, 27234, 27235, 27236, 27237, 27238, 27239, 27240, 27241, 27242) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
		
    
    return start_base + final_base

def getCinema_SuccessVsFailureGeneral(request):
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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27201, 27202, 27203, 27204, 27205, 27206, 27207, 27208, 27209, 27210, 27211, 27212, 27213, 27214, 27215, 27216, 27217, 27218, 27219, 27220, 27221, 27222, 27223, 27224, 27225, 27226, 27227, 27228, 27229, 27230, 27231, 27232, 27233, 27234, 27235, 27236, 27237, 27238, 27239, 27240, 27241, 27242) ' 
    
    return start_base + final_base


def getCinema_SuccessVsFailure_ParticularSeats(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, e.nombre as nombreElemento, COUNT(if(a.correcta = 1 ,1, NULL)) AS Success, COUNT(if(a.correcta = 0 ,1, NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b, elemento e  WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.id_elemento = e.id' + query_params + ' AND a.id_elemento IN (27201, 27202, 27203, 27204, 27205, 27206, 27207, 27208, 27209, 27210, 27211, 27212, 27213, 27214, 27215, 27216, 27217, 27218, 27219, 27220, 27221, 27222, 27223, 27224, 27225, 27226, 27227, 27228, 27229, 27230, 27231, 27232, 27233, 27234, 27235, 27236, 27237, 27238, 27239, 27240, 27241, 27242) ' + ' GROUP BY u.id, a.id_elemento'
    
    return start_base + final_base

##SCHOOL:
def getSchoolNumberOfEntrances(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  Count(id_elemento) as NumberOfEntrances FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27305) ' + ' GROUP BY u.id'
    
    return start_base + final_base

def getSchool_CompleteVsIncomplete(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Completes, COUNT(if(a.correcta = 0 ,1,NULL)) AS Incompletes FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento = 27305 ' + ' GROUP BY u.id'
    
    return start_base + final_base

def getSchool_SuccessVsFailure(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27301, 27302, 27303, 27304) ' + ' GROUP BY u.id'
    
    return start_base + final_base

def getSchool_SuccessVsFailureGeneral(request):
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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27301, 27302, 27303, 27304) '
    
    return start_base + final_base

def getSchool_SuccessPercentageInTime(request):

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
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS Fecha, COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND a.id_elemento IN (27301, 27302, 27303, 27304) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base

def getSchool_SuccessVsFailureGeneral(request):
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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27301, 27302, 27303, 27304) '
    
    return start_base + final_base


def getSchool_SuccessVsFailure_ParticularSeats(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, e.nombre as nombreElemento, COUNT(if(a.correcta = 1 ,1, NULL)) AS Success, COUNT(if(a.correcta = 0 ,1, NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b, elemento e  WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.id_elemento = e.id' + query_params + ' AND a.id_elemento IN (27301, 27302, 27303, 27304) ' + ' GROUP BY u.id, a.id_elemento'
    
    return start_base + final_base

##TAXI:
def getTaxiNumberOfEntrances(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  Count(id_elemento) as NumberOfEntrances FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27409) ' + ' GROUP BY u.id'
    
    return start_base + final_base

def getTaxi_CompleteVsIncomplete(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Completes, COUNT(if(a.correcta = 0 ,1,NULL)) AS Incompletes FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento = 27409 ' + ' GROUP BY u.id'
    
    return start_base + final_base

def getTaxi_SuccessVsFailure(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27401, 27402, 27403, 27404, 27405, 27406, 27407, 27408) ' + ' GROUP BY u.id'
    
    return start_base + final_base

def getTaxi_SuccessVsFailureGeneral(request):
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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27401, 27402, 27403, 27404, 27405, 27406, 27407, 27408) '
    
    return start_base + final_base

def getTaxi_SuccessPercentageInTime(request):

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
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS Fecha, COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND a.id_elemento IN (27401, 27402, 27403, 27404, 27405, 27406, 27407, 27408) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base

def getTaxi_SuccessVsFailureGeneral(request):
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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,  COUNT(if(a.correcta = 1 ,1,NULL)) AS Success, COUNT(if(a.correcta = 0 ,1,NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.id_elemento IN (27401, 27402, 27403, 27404, 27405, 27406, 27407, 27408) ' 
    
    return start_base + final_base


def getTaxi_SuccessVsFailure_ParticularSeats(request):

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

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, e.nombre as nombreElemento, COUNT(if(a.correcta = 1 ,1, NULL)) AS Success, COUNT(if(a.correcta = 0 ,1, NULL)) AS Failure FROM alumno_respuesta_actividad a, usuario u, pertenece b, elemento e  WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.id_elemento = e.id' + query_params + ' AND a.id_elemento IN (27401, 27402, 27403, 27404, 27405, 27406, 27407, 27408) ' + ' GROUP BY u.id, a.id_elemento'
    
    return start_base + final_base


######END BUILD YOUR CITY######

######START RECICLANDO CONSTRUYO######
def get_porcentaje_llave(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, COALESCE(round(count((if(a.id_elemento=2128,1,null)))/count((if (a.id_elemento=2031,1,null)))),0) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    hi = "  SELECT  CONCAT(usuario.nombres,  " + "         ' ', " + "         usuario.apellido_paterno, " + "         ' ', " + "         usuario.apellido_materno) AS nombre, " + " round(COUNT( alumno_respuesta_actividad.correcta) * 100 / (SELECT  " + "         COUNT(alumno_respuesta_actividad.correcta) AS s " + "     FROM " + "         alumno_respuesta_actividad " + "     WHERE " + "         (correcta = 0 OR correcta = 1) AND alumno_respuesta_actividad.id_elemento = 290013 " + query_params2 + "             ), 0) AS `Porcentaje`, " + "             pertenece.colegio_id, " + "             pertenece.curso_id " + " FROM " + "     usuario  " + " INNER JOIN alumno_respuesta_actividad " + " ON usuario.id = alumno_respuesta_actividad.id_user " + " INNER JOIN pertenece " + " ON pertenece.usuario_id = alumno_respuesta_actividad.id_user " + " WHERE " + " 		correcta = 1 AND alumno_respuesta_actividad.id_elemento = 290013 " + query_params
    return hi


def get_promedio_intentos(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT CONCAT(usuario.nombres, ' ',usuario.apellido_paterno, ' ',usuario.apellido_materno) AS nombre, ROUND(COUNT(alumno_respuesta_actividad.correcta) / (SELECT COUNT(alumno_respuesta_actividad.correcta) AS s FROM alumno_respuesta_actividad WHERE (correcta = 1) AND (alumno_respuesta_actividad.id_elemento = 290013 or alumno_respuesta_actividad.id_elemento = 290014 or alumno_respuesta_actividad.id_elemento = 290015 or alumno_respuesta_actividad.id_elemento = 290016)" + query_params2 + " ), 0) AS `Promedio movimientos por intento satisfactorio`, pertenece.colegio_id, pertenece.curso_id FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user WHERE correcta = 2 AND (alumno_respuesta_actividad.id_elemento = 290013 or alumno_respuesta_actividad.id_elemento = 290014 or alumno_respuesta_actividad.id_elemento = 290015 or alumno_respuesta_actividad.id_elemento = 290016)" + query_params
    #print(hi)
    return hi


def get_promedio_intentos_totales(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT CONCAT(usuario.nombres, ' ',usuario.apellido_paterno, ' ',usuario.apellido_materno) AS nombre, ROUND(COUNT(alumno_respuesta_actividad.correcta) / (SELECT COUNT(alumno_respuesta_actividad.correcta) AS s FROM alumno_respuesta_actividad WHERE (correcta = 1 OR correcta = 0) AND (alumno_respuesta_actividad.id_elemento = 290013 OR alumno_respuesta_actividad.id_elemento = 290014 OR alumno_respuesta_actividad.id_elemento = 290015 OR alumno_respuesta_actividad.id_elemento = 290016)" + query_params2 + " ), 0) AS `Promedio movimientos por intento satisfactorio`, pertenece.colegio_id, pertenece.curso_id FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user WHERE correcta = 2 AND (alumno_respuesta_actividad.id_elemento = 290013 OR alumno_respuesta_actividad.id_elemento = 290014 OR alumno_respuesta_actividad.id_elemento = 290015 OR alumno_respuesta_actividad.id_elemento = 290016)" + query_params
    #print(hi)
    return hi


def get_elementos_reciclados_usuario(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT CONCAT(usuario.nombres, ' ',usuario.apellido_paterno, ' ',usuario.apellido_materno) AS nombre, count(id_elemento), elemento.nombre, pertenece.colegio_id, pertenece.curso_id FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user INNER JOIN elemento ON alumno_respuesta_actividad.id_elemento = elemento.id WHERE correcta = 1" + query_params + " GROUP BY elemento.id"
    #print(hi)
    return hi

def get_elementos_reciclados_incorrecto_usuario(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT CONCAT(usuario.nombres, ' ',usuario.apellido_paterno, ' ',usuario.apellido_materno) AS nombre, count(id_elemento), elemento.nombre, pertenece.colegio_id, pertenece.curso_id FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user INNER JOIN elemento ON alumno_respuesta_actividad.id_elemento = elemento.id WHERE correcta = 0" + query_params + " GROUP BY elemento.id"
    #print(hi)
    return hi

def get_Respuestas_Usuario_VencerAlConstructor(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT elemento.id, alumno_respuesta_actividad.fila, COUNT(elemento.id) AS cantidad, SUM(alumno_respuesta_actividad.correcta = 0) AS incorrectas, SUM(alumno_respuesta_actividad.correcta = 1) AS Correctas FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user INNER JOIN elemento ON alumno_respuesta_actividad.id_elemento = elemento.id WHERE ( alumno_respuesta_actividad.fila = 1000 OR  alumno_respuesta_actividad.fila = 2000)" + query_params + " GROUP BY alumno_respuesta_actividad.fila"
    #print(hi)
    return hi

def get_ElementosRecicladosCorrectamente_Tipo(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT elemento.id, alumno_respuesta_actividad.columna, count(elemento.id) as cantidad FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user INNER JOIN elemento ON alumno_respuesta_actividad.id_elemento = elemento.id WHERE alumno_respuesta_actividad.correcta = 0" + query_params + " GROUP BY alumno_respuesta_actividad.columna"
    #print(hi)
    return hi

def get_ElementosRecicladosIncorrectamente_Tipo(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT elemento.id, alumno_respuesta_actividad.columna, count(elemento.id) as cantidad FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user INNER JOIN elemento ON alumno_respuesta_actividad.id_elemento = elemento.id WHERE alumno_respuesta_actividad.correcta = 1" + query_params + " GROUP BY alumno_respuesta_actividad.columna"
    #print(hi)
    return hi

def get_llave_Tipo(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT elemento.nombre, count(alumno_respuesta_actividad.id_elemento), sum(alumno_respuesta_actividad.correcta = 0) AS incorrectas, sum(alumno_respuesta_actividad.correcta = 1) AS Correctas FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user INNER JOIN elemento ON alumno_respuesta_actividad.id_elemento = elemento.id WHERE 1 = 1 AND (alumno_respuesta_actividad.id_elemento = 290014 or alumno_respuesta_actividad.id_elemento = 290015 or alumno_respuesta_actividad.id_elemento = 290016) AND alumno_respuesta_actividad.correcta != 2" + query_params + " GROUP BY alumno_respuesta_actividad.id_elemento"
    print(hi)
    return hi

def get_Respuestas_General_VencerAlConstructor(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT CONCAT(usuario.nombres,' ',usuario.apellido_paterno,' ',usuario.apellido_materno) AS nombre,pertenece.colegio_id,pertenece.curso_id,alumno_respuesta_actividad.correcta,count(alumno_respuesta_actividad.correcta) as Totales,SUM(alumno_respuesta_actividad.correcta = 0) AS incorrectas,SUM(alumno_respuesta_actividad.correcta = 1) AS Correctas FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user INNER JOIN elemento ON alumno_respuesta_actividad.id_elemento = elemento.id WHERE 1=1" + query_params + " group by usuario_id"
    #print(hi)
    return hi

def get_Historial_Respuestas(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT CONCAT(usuario.nombres,' ',usuario.apellido_paterno,' ',usuario.apellido_materno) AS nombre,pertenece.colegio_id,pertenece.curso_id,alumno_respuesta_actividad.correcta,COUNT(alumno_respuesta_actividad.correcta) AS Totales,SUM(alumno_respuesta_actividad.correcta = 0) AS incorrectas,SUM(alumno_respuesta_actividad.correcta = 1) AS Correctas,DATE(datetime_touch) as Fecha FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user INNER JOIN elemento ON alumno_respuesta_actividad.id_elemento = elemento.id WHERE 1=1" + query_params + " GROUP BY DAY(datetime_touch) ORDER BY datetime_touch ASC"
    #print(hi)
    return hi

def get_Historial_movimientos(request):
    query_params = ''
    date = ''
    query_params2 = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND pertenece.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND pertenece.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND alumno_respuesta_actividad.id_actividad=' + request.GET.get('activity')

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params2 = ' AND alumno_respuesta_actividad.id_reim=' + request.GET.get('reim')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params2 += " AND alumno_respuesta_actividad.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params2 += ' AND alumno_respuesta_actividad.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (
            request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    hi = "SELECT CONCAT(usuario.nombres,' ',usuario.apellido_paterno,' ',usuario.apellido_materno) AS nombre,pertenece.colegio_id,pertenece.curso_id,alumno_respuesta_actividad.correcta,COUNT(alumno_respuesta_actividad.correcta) AS Totales,SUM(alumno_respuesta_actividad.correcta = 0) AS incorrectas,SUM(alumno_respuesta_actividad.correcta = 1) AS Correctas,DATE(datetime_touch) as Fecha FROM usuario INNER JOIN alumno_respuesta_actividad ON usuario.id = alumno_respuesta_actividad.id_user INNER JOIN pertenece ON pertenece.usuario_id = alumno_respuesta_actividad.id_user INNER JOIN elemento ON alumno_respuesta_actividad.id_elemento = elemento.id WHERE 1=1 AND alumno_respuesta_actividad.correcta != 2 AND (alumno_respuesta_actividad.id_elemento = 290013 OR alumno_respuesta_actividad.id_elemento = 290014 OR alumno_respuesta_actividad.id_elemento = 290015 OR alumno_respuesta_actividad.id_elemento = 290016) " + query_params + " GROUP BY DAY(datetime_touch) ORDER BY datetime_touch ASC"
    #print(hi)
    return hi


###################Inicio Reciclando cuido el Océano#####################

def get_touch_all_act206(request):
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
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and correcta=1 and (id_elemento=290400 or (id_elemento>=290400 and id_elemento<=290401) or (id_elemento>=290002 and id_elemento<=290004)) group by id_elemento;'
    return start_base + final_base
#Timer
def get_time_act_RCO(request):
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
#Correctas Incorrectas
def get_corrects_incorrects_RCO(request):

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
def get_corrects_RCO(request):

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
#Incorrectas
def get_incorrects_RCO(request):

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
#Simetrix
def get_completa_incompleta_RCO(request):

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
#Agrupados
def get_analytics1_co_act_3(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
     
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=290038,1,NULL)) Actividad1, count(if(a.id_elemento=290039,1,NULL)) Actividad2, count(if(a.id_elemento=290040,1,NULL)) Actividad3, count(if(a.id_elemento=290041,1,NULL)) Actvidad4, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b where' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'
    return start_base + final_base
#Actrividad mas jugada
def get_analytics1_1_co_act_3(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
     
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=290036,1,NULL)) Actividad1, count(if(a.id_elemento=290034,1,NULL)) Actividad2, count(if(a.id_elemento=290037,1,NULL)) Actividad3, count(if(a.id_elemento=290035,1,NULL)) Actvidad4, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b where' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'
    return start_base + final_base

#Agrupados
def get_posicionamiento_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=290036,1,NULL)) a_metal, count(if(a.id_elemento=290038,1,NULL)) desa_metal, count(if(a.id_elemento=290034,1,NULL)) a_carton , count(if(a.id_elemento=290039,1,NULL)) desa_carton, count(if(a.id_elemento=290037,1,NULL)) a_plastico, count(if(a.id_elemento=290040,1,NULL)) desa_plastico, count(if(a.id_elemento=290035,1,NULL)) a_vidrio, count(if(a.id_elemento=290041,1,NULL)) desa_vidrio FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta = 1 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base

#Desafios OA
def get_OA_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300015,25,NULL)) bn_total, count(if(a.id_elemento=300016,25,NULL)) ml_total, count(if(a.id_elemento=300015,26,NULL)) bn_CN05OAAC , count(if(a.id_elemento=300016,26,NULL)) ml_CN05OAAC, count(if(a.id_elemento=300015,27,NULL)) bn_MA04OA17, count(if(a.id_elemento=300016,27,NULL)) ml_MA04OA17, count(if(a.id_elemento=300015,28,NULL)) bn_MA04OA18, count(if(a.id_elemento=300016,28,NULL)) ml_MA04OA18, count(if(a.id_elemento=300015,29,NULL)) bn_MA04OAH, count(if(a.id_elemento=300016,29,NULL)) ml_MA04OAH FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta < 30 and a.correcta > 24 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
#Desafios OA
def get_OA2_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300015,26,NULL)) bn_CN05OAAC FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=26 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
#Desafios OA 
def get_OA2_2_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300016,26,NULL)) ml_CN05OAAC FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=26 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
#Desafios OA
def get_OA3_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300015,27,NULL)) bn_MA04OA17 FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=27 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
#Desafios OA
def get_OA3_2_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300016,27,NULL)) ml_MA04OA17 FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=27 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
#Desafios OA
def get_OA4_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300015,28,NULL)) bn_MA04OA18 FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=28 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
#Desafios OA
def get_OA4_2_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300016,28,NULL)) ml_MA04OA18 FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=28 ' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base
# Colaborativa 
def get_victorias_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300006,1,NULL)) victorias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=1 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
# Colaborativa
def get_derrotas_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300007,0,NULL)) derrotas FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=0 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
# Colaborativa movumientos
def get_mov_multi_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300017,1,NULL)) movimientos FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=1 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
# Colaborativa
def get_OA5_2_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300016,29,NULL)) ml_MA04OAHA FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=29 ' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base
#Desafios OA
def get_OA5_Desafios_RCO(request):

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
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=300015,29,NULL)) bn_MA04OAHA FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta=29 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base
#Desafios OA
def get_touch_all_OA1Bien(request):
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
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and correcta=26 and id_elemento=300015 group by id_elemento;'
    return start_base + final_base


def get_elementos_alu_RCO(request):

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
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND (a.id_elemento=290034 OR a.id_elemento=290036 OR a.id_elemento=290037 OR a.id_elemento=290035 OR a.id_elemento=290434 OR a.id_elemento=290435 OR a.id_elemento=290436 OR a.id_elemento=290437) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base

###################Fin Reciclando cuido el océano#####################
###### BEGIN REIM 202 PROTECT YOUR LAND


##GENERAL QUERYS:
def get_number_of_sessionsPYL(request):
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


def get_playtimePYL(request):
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

    start_base = "SELECT u.id, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre_alumno, IF (ROUND((SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))))/60<1, 1,ROUND(SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))/60)) as minutos_juego, co.nombre as Colegio, concat(n.nombre, c.nombre) as Curso FROM asigna_reim_alumno a, usuario u, pertenece p , nivel n , curso c, colegio co WHERE" + date
    final_base = ' n.id=p.nivel_id and p.curso_id = c.id and  a.usuario_id = u.id and p.usuario_id=u.id and co.id = p.colegio_id AND p.colegio_id IN (SELECT colegio_id FROM pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND p.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

    return start_base + final_base


def get_touch_countPYL(request):
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
    print(query_params)

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base


def get_activities_played_counterPYL(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT a.id_elemento as idElemento, count(1) as counter FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + ' AND a.id_elemento IN (280000,280001,280002, 280004)' + query_params + ' GROUP BY a.id_elemento;'

    return start_base + final_base

##ACTIVIDAD FOOTPRINTS:

def get_corrects_PYL(request):

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

def get_correctsxsession_PYL(request):

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
    start_base = 'SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS ocurrecias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user AND (a.id_elemento=280201) ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    return start_base + final_base

def PYL_getTimer(request):
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = '  SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(max(a.fila)) as Maximo, concat(min(a.fila)) as Minimo FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user AND a.id_elemento = 280215 ' + query_params + ' GROUP BY u.id;'

    return start_base + final_base


##ACTIVIDAD DRAW SOLUTIONS:

def get_activities_colorPYL(request):
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT a.id_elemento as idElemento, count(1) as counter FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + ' AND a.id_elemento IN (280100,280101,280102, 280103, 280104)' + query_params + ' GROUP BY a.id_elemento;'

    return start_base + final_base

def get_ElemVisual_PYL(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=280106,1,NULL)) Intensidad, count(if(a.id_elemento=280107,1,NULL)) Grosor, count(if(a.id_elemento=280105,1,NULL)) Borrar FROM alumno_respuesta_actividad a, usuario u, pertenece b  WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user ' + query_params +  ' GROUP BY u.id;'

    return start_base + final_base

###### GALLERY

def PYL_Get_Emociones(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=280216,1,NULL)) Sorprendido, count(if(a.id_elemento=280217,1,NULL)) Triste, count(if(a.id_elemento=280218,1,NULL)) Encanta, count(if(a.id_elemento=280219,1,NULL)) Feliz FROM alumno_respuesta_actividad a, usuario u, pertenece b  WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY u.id;'

    return start_base + final_base



##ACTIVIDAD BUILD YOUR LAND

def PYL_Get_Answer(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT a.id_elemento, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(correcta=1,1,NULL)) Correctas, count(if(correcta=0,1,NULL)) Incorrectas,i.Pregunta FROM alumno_respuesta_actividad a, usuario u, pertenece b, item i WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user and a.id_elemento = i.IdItem ' + query_params + ' GROUP BY a.id_elemento;'

    return start_base + final_base

def PYL_Get_AnswerxOA(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = ' SELECT count(if(correcta=1,1,NULL)) Correctas, count(if(correcta=0,1,NULL)) Incorrectas, i.objetivo_aprendizaje_id, o.nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b, item i, objetivo_aprendizaje o WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user and a.id_elemento = i.IdItem and i.objetivo_aprendizaje_id = o.id ' + query_params + ' GROUP BY o.id;'

    return start_base + final_base

def PYL_Get_AnswerxOA(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = ' SELECT count(if(correcta=1,1,NULL)) Correctas, count(if(correcta=0,1,NULL)) Incorrectas, i.objetivo_aprendizaje_id, o.nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b, item i, objetivo_aprendizaje o WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user and a.id_elemento = i.IdItem and i.objetivo_aprendizaje_id = o.id ' + query_params + ' GROUP BY o.id;'

    return start_base + final_base

#INICIO QUERYS Toy's Colection---------------

def get_cantidad_sesiones_por_curso(request):

    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, COALESCE(round(count((if(a.id_elemento=2128,1,null)))/count((if (a.id_elemento=2031,1,null)))),0) AS CantidadTouch, b.colegio_id, b.curso_id '
    start_base += ' FROM asigna_reim_alumno a'
    start_base += ' INNER JOIN usuario u on (u.id=a.usuario_id)' 
    start_base += ' INNER JOIN pertenece b on (b.usuario_id = a.usuario_id)'
    start_base += ' WHERE ' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base  

#Sesiones del curso
def get_sesiones(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)

    start_base = 'SELECT "Sesiones Totales" as nombre, count(a.usuario_id) AS Cantidad FROM asigna_reim_alumno a INNER JOIN usuario u on (u.id=a.usuario_id) INNER JOIN pertenece b on (b.usuario_id = a.usuario_id) WHERE ' + date
    final_base = ' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY b.colegio_id'
    return start_base + final_base

#Tiempo del curso
def get_tiempo_total(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)

    start_base = 'SELECT  "Tiempo Total" as nombre, round(sum(TO_SECONDS(datetime_termino)-TO_SECONDS(datetime_inicio))/60,0) as Tiempo FROM asigna_reim_alumno a INNER JOIN usuario u on (u.id=a.usuario_id) INNER JOIN pertenece b on (b.usuario_id = a.usuario_id) WHERE ' + date
    final_base = ' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY b.colegio_id'
    return start_base + final_base

#Tiempo Promedio del curso
def get_tiempo_promedio(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, round((sum(TO_SECONDS(datetime_termino)-TO_SECONDS(datetime_inicio))/60)/count(a.usuario_id),0) as Tiempo_promedio'
    start_base += ' FROM asigna_reim_alumno a'
    start_base += ' INNER JOIN usuario u on (u.id=a.usuario_id)' 
    start_base += ' INNER JOIN pertenece b on (b.usuario_id = a.usuario_id)'
    start_base += ' WHERE ' + date
    final_base = ' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")' 
    final_base += ' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

    return start_base + final_base

#Solicitudes Realizadas
def get_solicitudes(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)

    sql ='SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(datetime_touch) as Solicitudes'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN elemento e on (e.id=are.id_elemento)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' AND id_actividad=9041'
    sql +=' AND are.id_elemento in (290050)'  + query_params
    sql +=' GROUP BY u.id;'

    return sql

def get_colaboraciones(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)

    sql ='SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(datetime_touch) as Solicitudes'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN elemento e on (e.id=are.id_elemento)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' AND id_actividad=9041'
    sql +=' AND id_elemento in (290615)'  + query_params
    sql +=' GROUP BY u.id;'

    return sql


def get_colaboraciones_rec(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)

    sql ='SELECT usuariorecibe_id, concat(usu.nombres ," ", usu.apellido_paterno ," ", usu.apellido_materno) as nombre, count(1)'
    sql +=' FROM transaccion_reim t'
    sql +=' INNER JOIN usuario usu on (usu.id=t.usuariorecibe_id)'
    sql +=' WHERE session_id in ('
    sql +=' SELECT distinct(sesion_id)'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN detalle_elemento d on (d.id_elemento=are.id_elemento)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_Actividad=9041'
    sql +=' and are.id_elemento in(290615)'  + query_params + ')'
    sql +=' AND t.elemento_id in (290614)'
    sql +=' group by usuariorecibe_id;'

    return sql


#Preferencias de búsqueda
def get_Lugar_Buscado(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    date = get_date_param(request)
    date=''
    #start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, round((sum(TO_SECONDS(datetime_termino)-TO_SECONDS(datetime_inicio))/60)/count(a.usuario_id),0) as Tiempo_promedio FROM asigna_reim_alumno a INNER JOIN usuario u on (u.id=a.usuario_id) INNER JOIN pertenece b on (b.usuario_id = a.usuario_id) WHERE ' + date
    #final_base = ' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' 
    sql ='SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, round(sum(if(id_elemento=290164,1,0))*100/Count(id_elemento),0) as Casa, round(sum(if(id_elemento=290165,1,0))*100/Count(id_elemento),0) as Parque, round(sum(if(id_elemento=290166,1,0))*100/Count(id_elemento),0) as Colegio'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN elemento e on (e.id=are.id_elemento)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' AND id_actividad=9040'
    sql +=' AND id_elemento in (290164, 290165, 290166)'  + query_params
    sql +=' GROUP BY u.id;'

    return sql

#Preferencias de búsqueda
def get_Habitacion_Buscado1(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in(9028,9029,9030)'
    date = get_date_param(request)
    date=''
    #start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, round((sum(TO_SECONDS(datetime_termino)-TO_SECONDS(datetime_inicio))/60)/count(a.usuario_id),0) as Tiempo_promedio FROM asigna_reim_alumno a INNER JOIN usuario u on (u.id=a.usuario_id) INNER JOIN pertenece b on (b.usuario_id = a.usuario_id) WHERE ' + date
    #final_base = ' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' 
    sql ='SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,' 
    sql +=' round(sum(if(id_elemento=290167,1,0))*100/Count(id_elemento),0) as Dormitorio,'
    sql +=' round(sum(if(id_elemento=290168,1,0))*100/Count(id_elemento),0) as Cocina,'
    sql +=' round(sum(if(id_elemento=290169,1,0))*100/Count(id_elemento),0) as Baño,'
    sql +=' round(sum(if(id_elemento=290170,1,0))*100/Count(id_elemento),0) as Living,'
    sql +=' round(sum(if(id_elemento=290171,1,0))*100/Count(id_elemento),0) as Comedor'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN elemento e on (e.id=are.id_elemento)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' AND id_elemento in (290167, 290168, 290169, 290170, 290171, 290172, 290173, 290174)'  + query_params
    sql +=' GROUP BY u.id;'

    return sql

def get_Habitacion_Buscado2(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in(9028,9029,9030)'
    date = get_date_param(request)
    date=''
    #start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, round((sum(TO_SECONDS(datetime_termino)-TO_SECONDS(datetime_inicio))/60)/count(a.usuario_id),0) as Tiempo_promedio FROM asigna_reim_alumno a INNER JOIN usuario u on (u.id=a.usuario_id) INNER JOIN pertenece b on (b.usuario_id = a.usuario_id) WHERE ' + date
    #final_base = ' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' 
    sql ='SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,' 
    sql +=' round(sum(if(id_elemento=290172,1,0))*100/Count(id_elemento),0) as Pasillo'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN elemento e on (e.id=are.id_elemento)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' AND id_elemento in (290167, 290168, 290169, 290170, 290171, 290172, 290173, 290174)'  + query_params
    sql +=' GROUP BY u.id;'

    return sql

def get_Habitacion_Buscado3(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in(9028,9029,9030)'
    date = get_date_param(request)
    date=''
    #start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, round((sum(TO_SECONDS(datetime_termino)-TO_SECONDS(datetime_inicio))/60)/count(a.usuario_id),0) as Tiempo_promedio FROM asigna_reim_alumno a INNER JOIN usuario u on (u.id=a.usuario_id) INNER JOIN pertenece b on (b.usuario_id = a.usuario_id) WHERE ' + date
    #final_base = ' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' 
    sql ='SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,' 
    sql +=' round(sum(if(id_elemento=290173,1,0))*100/Count(id_elemento),0) as Sala_de_Clases,'
    sql +=' round(sum(if(id_elemento=290174,1,0))*100/Count(id_elemento),0) as Parque'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN elemento e on (e.id=are.id_elemento)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' AND id_elemento in (290167, 290168, 290169, 290170, 290171, 290172, 290173, 290174)'  + query_params
    sql +=' GROUP BY u.id;'

    return sql

def get_desafios(request):

    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in (9016,9017,9018,9019)'
    date = get_date_param(request)
    date=''

    sql='SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre,if(id_Actividad=9016,"Colores",if(id_Actividad=9017,"Formas",if(id_Actividad=9018,"Vocales",if(id_Actividad=9019,"Números","Otra")))) as actividad, sum(if(id_elemento=290048,1,0))as no_realizado, sum(if(id_elemento=290048,0,if(correcta=1,1,0))) as correctas,sum(if(id_elemento=290048,0,if(correcta=0,1,0))) as incorrectas'
    sql +=' FROM asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=a.usuario_id)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = a.usuario_id)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and id_elemento not in(290045)' + query_params
    sql +=' Group by id_actividad;'
    return sql

def get_desafios_porcentual(request):

    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in (9016,9017,9018,9019)'

    date = get_date_param(request)
    date=''

    sql='SELECT date(datetime_touch), round(sum(if(correcta=1,1,0))*100/count(correcta),0) as corectas'
    sql +=' FROM asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=a.usuario_id)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = a.usuario_id)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_elemento not in(290048,290045,290046)' + query_params
    sql +=' group by date(datetime_touch)'
    sql +=' order by date(datetime_touch) asc;'
    return sql

def get_no_desafios(request):

    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in (9016,9017,9018,9019)'
    date = get_date_param(request)
    date=''

    sql='SELECT if(id_Actividad=9016,"Colores",if(id_Actividad=9017,"Formas",if(id_Actividad=9018,"Vocales",if(id_Actividad=9019,"Números","Otra")))),'
    sql +=' sum(if(id_elemento=290048,1,0))/count(id_elemento) as no_realizado'
    sql +=' FROM asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=a.usuario_id)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = a.usuario_id)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and id_elemento not in(290045)' + query_params
    sql +=' Group by id_actividad;'
    return sql

def get_colores(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)
    date=''

    sql='SELECT distinct(are.id_elemento),SUBSTRING(descripcion,INSTR(descripcion, " ")) as descripcion,'
    sql +=' sum(if(correcta=1,1,0)) as corectas,sum(if(correcta=0,1,0)) as incorectas'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN detalle_elemento d on (d.id_elemento=are.id_elemento)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_Actividad=9016'
    sql +=' and are.id_elemento not in(290048,290045,290046)' + query_params
    sql +=' group by SUBSTRING(descripcion,INSTR(descripcion, " "))' 
    return sql

    
def get_formas(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)
    date=''

    sql='SELECT distinct(are.id_elemento),MID(descripcion,1,INSTR(descripcion, " ")) as descripcion,'
    sql +=' sum(if(correcta=1,1,0)) as corectas,sum(if(correcta=0,1,0)) as incorectas'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN detalle_elemento d on (d.id_elemento=are.id_elemento)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_Actividad=9017'
    sql +=' and are.id_elemento not in(290048,290045,290046)' + query_params
    sql +=' group by Mid(descripcion,1,INSTR(descripcion, " "))' 
    return sql

def get_vocales(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)
    date=''

    sql='SELECT distinct(are.id_elemento),descripcion,'
    sql +=' sum(if(correcta=1,1,0)) as corectas,sum(if(correcta=0,1,0)) as incorectas'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN detalle_elemento d on (d.id_elemento=are.id_elemento)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_Actividad=9018'
    sql +=' and are.id_elemento not in(290048,290045,290046)' + query_params
    sql +=' group by descripcion' 
    return sql

def get_numeros(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')

    date = get_date_param(request)
    date=''

    sql='SELECT distinct(are.id_elemento),descripcion,'
    sql +=' sum(if(correcta=1,1,0)) as corectas,sum(if(correcta=0,1,0)) as incorectas'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN detalle_elemento d on (d.id_elemento=are.id_elemento)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_Actividad=9019'
    sql +=' and are.id_elemento not in(290048,290045,290046)' + query_params
    sql +=' group by descripcion' 
    return sql

def get_ordenar(request):

    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in (9020,9021,9022,9023,9024,9025,9026,9027)'

    date = get_date_param(request)
    date=''

    sql='SELECT date(datetime_touch), round(sum(if(correcta=1,1,0))*100/count(correcta),0) as corectas'
    sql +=' FROM asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=a.usuario_id)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = a.usuario_id)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_elemento in(300211,300212,300210)' + query_params
    sql +=' group by date(datetime_touch)'
    sql +=' order by date(datetime_touch) asc;'
    return sql

def get_ordenar_resultados(request):

    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in (9020,9021,9022,9023,9024,9025,9026,9027)'

    date = get_date_param(request)
    date=''

    sql='SELECT distinct(are.id_elemento),descripcion, sum(if(correcta=1,1,0)) as corectas,sum(if(correcta=0,1,0)) as incorectas'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN detalle_elemento d on (d.id_elemento=are.id_elemento)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_elemento in(300211,300212,300210)' + query_params
    sql +=' group by descripcion order by descripcion asc;'
    return sql


def get_buscar(request):

    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in (9031,9032,9033,9034,9035,9036,9037,9038)'

    date = get_date_param(request)
    date=''

    sql='SELECT date(datetime_touch), round(sum(if(correcta=1,1,0))*100/count(correcta),0) as corectas'
    sql +=' FROM asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=a.usuario_id)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = a.usuario_id)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_elemento  between 290084 and 290163 ' + query_params
    sql +=' group by date(datetime_touch)'
    sql +=' order by date(datetime_touch) asc;'
    return sql

def get_buscar_resultados(request):

    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in (9031,9032,9033,9034,9035,9036,9037,9038)'

    date = get_date_param(request)
    date=''

    sql='SELECT distinct(are.id_elemento),descripcion, sum(if(correcta=1,1,0)) as corectas,sum(if(correcta=0,1,0)) as incorectas'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN detalle_elemento d on (d.id_elemento=are.id_elemento)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_elemento between 290084 and 290163 ' + query_params
    sql +=' group by descripcion order by descripcion asc;'
    return sql

def get_donaciones(request):

    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND id_actividad=' + request.GET.get('activity')
    else:
        query_params += ' AND id_actividad in (9015)'

    date = get_date_param(request)
    date=''

    sql='SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(correcta) as cantidad'
    sql +=' FROM  asigna_reim_alumno a'
    sql +=' INNER JOIN alumno_respuesta_actividad are on(are.id_user=a.usuario_id and id_per=periodo_id and id_reim=reim_id and datetime_touch between datetime_inicio and datetime_termino)'
    sql +=' INNER JOIN detalle_elemento d on (d.id_elemento=are.id_elemento)'
    sql +=' INNER JOIN actividad act on (act.id=id_actividad)'
    sql +=' INNER JOIN usuario u on (u.id=are.id_user)'
    sql +=' INNER JOIN pertenece b on (b.usuario_id = are.id_user)'
    sql +=' WHERE '  + date
    sql +=' b.colegio_id IN (SELECT colegio_id from pertenece p INNER JOIN usuario u1 ON (p.usuario_id = u1.id) WHERE username="' + request.user.username + '")'
    sql +=' AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))'
    sql +=' and are.id_elemento not in (290048,290046,290045) ' + query_params
    sql +=' group by u.id order by u.id asc;'
    return sql
#FIN Query TOY'S COLECTION
