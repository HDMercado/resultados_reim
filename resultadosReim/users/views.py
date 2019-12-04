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
        #REIM SELECCIONADO
        reim_num = request.GET.get('reim')
        
        move_element_quantity_response = []
        aceptar_creacion_quantity_response = []
        ingresar_creacion_quantity_response = []
        volver_creacion_quantity_response = []

        if reim_num=="2":

            #Elemento desplazado
            move_element_query = get_move_element_query(request)
            cursor.execute(move_element_query)
            queries.append({"name": 'Desplazado query', "query": move_element_query})
            move_element_quantity = cursor.fetchall()
            for row in move_element_quantity:
                move_element_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
            
            #Volver creacion
            volver_creacion_query = get_volver_creacion_query(request)
            cursor.execute(volver_creacion_query)
            queries.append({"name": 'volver creacion query', "query": volver_creacion_query})
            volver_creacion_quantity = cursor.fetchall()
            for row in volver_creacion_quantity:
                volver_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
            #aceptar creacion
            aceptar_creacion_query = get_aceptar_creacion_query(request)
            cursor.execute(aceptar_creacion_query)
            queries.append({"name": 'aceptar creacion query', "query": aceptar_creacion_query})
            aceptar_creacion_quantity = cursor.fetchall()
            for row in aceptar_creacion_quantity:
                aceptar_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
            
            #Ingresar creacion
            ingresar_creacion_query = get_ingresar_creacion_query(request)
            cursor.execute(ingresar_creacion_query)
            queries.append({"name": 'ingresar creacion query', "query": ingresar_creacion_query})
            ingresar_creacion_quantity = cursor.fetchall()
            for row in ingresar_creacion_quantity:
                ingresar_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
            
        #Clean Ocean
        colision_quantity_response = []
        corrects_quantity_response = []
        incorrects_quantity_response = []
        jumps_quantity_response = []

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
            print ("corrects quantity" , corrects_quantity)
            for row in corrects_quantity:
                corrects_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            incorrects_query = get_incorrects_co(request)
            cursor.execute(incorrects_query)
            queries.append({"name": 'Incorrects query', "query": incorrects_query})
            incorrects_quantity = cursor.fetchall()
            print ("incorrects quantity" , incorrects_quantity)
            for row in incorrects_quantity:
                incorrects_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

            jumps_query = get_jumps_co(request)
            cursor.execute(jumps_query)
            queries.append({"name": 'Jumps query', "query": jumps_query})
            jumps_quantity = cursor.fetchall()
            print ("jumps quantity" , jumps_quantity)
            for row in jumps_quantity:
                jumps_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
    
        #Cantidad de Sesiones
        session_query = get_session_query(request)
        cursor.execute(session_query)
        queries.append({"name": 'Session query', "query": session_query})
        sesion_quantity = cursor.fetchall()
        sesion_quantity_response = []
        for row in sesion_quantity:
            sesion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        activate_graphics = activate_course_filter and activate_school_filter and activate_reim_filter
        return render(
            request,
            "users/welcome.html",
            {
                # Show graphics at the init
                'activate_graphics': activate_graphics,
                # Other context var
                'queries': queries,
                'schools': schools_response,
                'reims': reims_response,
                'game_time': game_time_response,
                'courses': courses_response,
                'activities': activities_response,
                'touch_quantity': touch_quantity_response,
                'sesion_quantity': sesion_quantity_response,
                'cant_usuarios':cant_usuarios,
                'activity_num':activity_num,
                'reim_num':reim_num,
                'move_element_quantity':move_element_quantity_response,
                'aceptar_creacion_quantity':aceptar_creacion_quantity_response,
                'volver_creacion_quantity':volver_creacion_quantity_response,
                'ingresar_creacion_quantity':ingresar_creacion_quantity_response,
                'colision_quantity':colision_quantity_response,
                'corrects_quantity':corrects_quantity_response,
                'incorrects_quantity':incorrects_quantity_response,
                'jumps_quantity':jumps_quantity_response,
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