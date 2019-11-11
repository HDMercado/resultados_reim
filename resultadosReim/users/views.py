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
        
        #Planet
        planet_query = get_planet_query(request)
        queries.append({"name": 'Planet query', "query": planet_query})
        cursor.execute(planet_query)
        planet_quantity = cursor.fetchall()
        planet_quantity_response = []
        for row in planet_quantity:
            planet_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        
        #Planet satelite
        planet_satelite_query = get_planet_satelite_query(request)
        queries.append({"name": 'Planet satelite query', "query": planet_satelite_query})
        cursor.execute(planet_satelite_query)
        planet_satelite_quantity = cursor.fetchall()
        planet_satelite_quantity_response = []
        for row in planet_satelite_quantity:
            planet_satelite_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
    
        #Planet ring
        planet_ring_query = get_planet_ring_query(request)
        queries.append({"name": 'Planet ring query', "query": planet_ring_query})
        cursor.execute(planet_ring_query)
        planet_ring_quantity = cursor.fetchall()
        planet_ring_quantity_response = []
        for row in planet_ring_quantity:
            planet_ring_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #Star
        star_query = get_star_query(request)
        queries.append({"name": 'Star query', "query": star_query})
        cursor.execute(star_query)
        ring_quantity = cursor.fetchall()
        ring_quantity_response = []
        for row in ring_quantity:
            ring_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #Supernova
        supernova_query = get_supernova_query(request)
        queries.append({"name": 'Supernova query', "query": supernova_query})
        cursor.execute(supernova_query)
        supernova_quantity = cursor.fetchall()
        supernova_quantity_response = []
        for row in supernova_quantity:
            supernova_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #Nebulosa
        nebulosa_query = get_nebulosa_query(request)
        queries.append({"name": 'Nebolosa query', "query": nebulosa_query})
        cursor.execute(nebulosa_query)
        nebulosa_quantity = cursor.fetchall()
        nebulosa_quantity_response = []
        for row in nebulosa_quantity:
            nebulosa_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #Galaxy
        galaxy_query = get_galaxy_query(request)
        queries.append({"name": 'Galaxy query', "query": galaxy_query})
        cursor.execute(galaxy_query)
        galaxy_quantity = cursor.fetchall()
        galaxy_quantity_response = []
        for row in galaxy_quantity:
            galaxy_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #Ingreso creacion
        ingreso_creacion_query = get_ingreso_creacion_query(request)
        queries.append({"name": 'ingreso creacion query', "query": ingreso_creacion_query})
        cursor.execute(ingreso_creacion_query)
        ingreso_creacion_quantity = cursor.fetchall()
        ingreso_creacion_quantity_response = []
        for row in ingreso_creacion_quantity:
            ingreso_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })
        
        #Volver creacion
        volver_creacion_query = get_volver_creacion_query(request)
        queries.append({"name": 'volver creacion query', "query": volver_creacion_query})
        cursor.execute(volver_creacion_query)
        volver_creacion_quantity = cursor.fetchall()
        volver_creacion_quantity_response = []
        for row in volver_creacion_quantity:
            volver_creacion_quantity_response.append({ 'id': row[0], 'name': row[1], 'quantity': row[2] })

        #Cantidad de Usuarios
        cant_usuarios = get_alumnos(request)
        print("largo de graficos")
        print(cant_usuarios)

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