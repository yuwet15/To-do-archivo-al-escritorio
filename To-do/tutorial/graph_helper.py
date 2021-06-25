import requests
import json

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
  # Send GET to /me
  user = requests.get(
    '{0}/me'.format(graph_url),
    headers={
      'Authorization': 'Bearer {0}'.format(token)
    },
    params={
      '$select': 'displayName,mail,mailboxSettings,userPrincipalName'
    })
  # Return the JSON result
  return user.json()

def create_event(token, carpeta, lista):
  # Create an event object
  # https://docs.microsoft.com/graph/api/resources/event?view=graph-rest-1.0


  # Set headers
  headers = {
    'Authorization': 'Bearer {0}'.format(token)
  }

  query_params = {
    '$top': '1',
    '$filter': f"contains(displayName,'{lista}')"
  }

  # Send GET to /me/events
  events = requests.get('{0}/me/todo/lists'.format(graph_url),
    headers=headers,
    params=query_params)

  return events.json()

def obtener_contenido_lista(token, id_lista, cant = 20):
  headers = {
    'Authorization': 'Bearer {0}'.format(token)
  }

  query_params = {
    '$top': f'{cant}'
  }

  events = requests.get(f'{graph_url}/me/todo/lists/{id_lista}/tasks',
    headers=headers,
    params=query_params)
  return events.json()


def get_iana_from_windows(windows_tz_name):
  return windows_tz_name