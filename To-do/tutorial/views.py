from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
from dateutil import tz, parser
from tutorial.graph_helper import *
from tutorial.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token

def home(request):
  context = initialize_context(request)
  #print(context)
  return render(request, 'tutorial/home.html', context)

def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context

def sign_in(request):
  # Get the sign-in flow
  flow = get_sign_in_flow()
  # Save the expected flow so we can use it in the callback
  try:
    request.session['auth_flow'] = flow
  except Exception as e:
    print(e)
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(flow['auth_uri'])

def callback(request):
  # Make the token request
  result = get_token_from_code(request)

  #Get the user's profile
  user = get_user(result['access_token'])

  # Store user
  store_user(request, user)
  return HttpResponseRedirect(reverse('home'))

def crear_csv(request):
  context = initialize_context(request)
  user = context['user']

  if request.method == 'POST':
    #print(request.POST)
    # Create the event
    token = get_token(request)

    crear = create_event(
      token,
      request.POST['carpeta'],
      request.POST['lista'])
    if len(crear['value']) == 0:
      return render(request, 'tutorial/error1.html')
    else:
      id_lista = crear['value'][0]['id']
      nombre = crear['value'][0]['displayName']
    print(request.POST)
    if request.POST['cantidad'] != '':
      cantidad_i = int(request.POST['cantidad'])
    else:
      cantidad_i = 20
    listas = obtener_contenido_lista(token, id_lista, cantidad_i)
    nombre_n = ""
    for i in range(len(nombre)):
      if nombre[i] == '/':
        nombre_n += '-'
      else:
        nombre_n += nombre[i]
    nombre = nombre_n
    with open(f"../csv/{nombre}.csv","w") as csv:
      for nombre_lista in listas['value']:
        nombre_lista = nombre_lista['title'].split('/')
        csv.write(f"{'/'.join(nombre_lista[:2])};{'/'.join(nombre_lista[2:])}\n")
    # Redirect back to calendar view
    return render(request, 'tutorial/success.html',{'nombre':f'{nombre}'})
  else:
    # Render the form
    return render(request, 'tutorial/crear_csv.html', context)

def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))
