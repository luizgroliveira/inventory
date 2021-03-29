#!/bin/env python
import os
import sys
import json
import urllib3
import requests
import argparse

urllib3.disable_warnings()

url = os.getenv("URL_PORTAL_IIF","https://infradevops-api.apl.caixa/api.php")
url = "http://infradevops-api-des.nprd2.caixa/api.php"

var_ambiente = os.getenv("SISTEMAAMBIENTE",os.getenv("SISTEMA_AMBIENTE",""))

var_sistema = os.getenv("SISTEMANOME",os.getenv("SISTEMA_NOME",""))

var_site = os.getenv("SITE","")

todos = False
##

dynamic_inventory = {}

def consultaPortal(url_portal,payload):
  try:
    request = requests.get(url_portal, params=payload, verify=False)
    request.raise_for_status()
    if 'info' in request.json():
      return 'vazio'

    return request.json()['dados']

  except requests.exceptions.HTTPError as http_error:
    print("HTTP Error:", http_error)
  except requests.exceptions.ConnectionError as con_error:
    print("Erro de conexao:",con_error)
  except requests.exceptions.Timeout as time_error:
    print("Conexao expirada", time_error)
  except requests.exceptions.RequestException as error:
    print("Erro:",error)
  except Exception as e:
    print ("Error:", e.args[0])
    sys.exit(1)

def cria_inventario(lista_membros):
  """ Gera lista de hosts e grupos """

  dynamic_inventory['_meta'] = {'hostvars':{}}
  dynamic_inventory[ambiente] = {'children':[], 'vars': {}}
  dynamic_inventory[ambiente]['children'].append('local')

  #import ipdb
  #ipdb.set_trace()

  global site
  try:
   if site:
     pass
  #except UnboundLocalError:
  except:
    if ambiente.lower() == 'prd':
      site = 'ctc_npcn'
    else:
      site = 'ctc_nprd'
  else:
    pass

  #print(json.dumps(lista_membros,indent=2))
  if lista_membros == 'vazio':

    #dynamic_inventory[site] = {'hosts':[], 'vars':{}}
    #dynamic_inventory[site] = {'children':[], 'vars': {}}
    #dynamic_inventory[site]['children'].append(membro['produto'])
    #pass
    dynamic_inventory[site] = {'hosts':[], 'vars':{}}
    dynamic_inventory[site] = {'children':[], 'vars': {}}
    #dynamic_inventory[site]['children'].append(membro['produto'])

    #print(site)
    if site not in dynamic_inventory[ambiente]['children']:
      dynamic_inventory[ambiente]['children'].append(site)

  else:

    for membro in lista_membros:
      #import ipdb; ipdb.set_trace()
      if membro['produto'] not in dynamic_inventory[ambiente]['children']:
        dynamic_inventory[ambiente]['children'].append(membro['produto'])

      if var_site != '':
      #if len(var_site) > 0:

        if membro['site'] == var_site:

          if membro["status"].lower() != 'ativado' and todos == False:
            continue

          if membro['plataforma'].lower() != 'vm' and todos == False:
            continue

          if membro['site'] == None:
            if membro['ambiente'].lower() == 'prd':
              site = 'ctc_npcn'
            else:
              site = 'ctc_nprd'
          else:
            site = membro['site']

          #if membro['site'] == None and todos == False:
          #  continue

          if membro['produto'].lower() not in dynamic_inventory:
            dynamic_inventory[membro['produto']] = {'hosts':[], 'vars':{}}

          dynamic_inventory[membro['produto']]['hosts'].append(membro['servidores_json'][0]['nome'])
          dynamic_inventory['local'] = {'hosts':['127.0.0.1'], 'vars':{'ansible_connection':'local'}}

          dynamic_inventory[site] = {'hosts':[], 'vars':{}}
          dynamic_inventory[site] = {'children':[], 'vars': {}}
          dynamic_inventory[site]['children'].append(membro['produto'])

          if site not in dynamic_inventory[ambiente]['children']:
            dynamic_inventory[ambiente]['children'].append(site)
      else:
        if membro["status"].lower() != 'ativado' and todos == False:
          continue

        if membro['plataforma'].lower() != 'vm' and todos == False:
          continue


        if membro['site'] == None:
          if membro['ambiente'].lower() == 'prd':
            site = 'ctc_npcn'
          else:
            site = 'ctc_nprd'
        else:
          site = membro['site']

        if membro['produto'].lower() not in dynamic_inventory:
          dynamic_inventory[membro['produto']] = {'hosts':[], 'vars':{}}

        dynamic_inventory[membro['produto']]['hosts'].append(membro['servidores_json'][0]['nome'])
        dynamic_inventory['local'] = {'hosts':['127.0.0.1'], 'vars':{'ansible_connection':'local'}}

        dynamic_inventory[site] = {'hosts':[], 'vars':{}}
        dynamic_inventory[site] = {'children':[], 'vars': {}}
        dynamic_inventory[site]['children'].append(membro['produto'])

        if site not in dynamic_inventory[ambiente]['children']:
          dynamic_inventory[ambiente]['children'].append(site)
      if membro['produto'] not in dynamic_inventory[site]['children']:
        dynamic_inventory[site]['children'].append(membro['produto'])




#    for membro in lista_membros:
#
#      if membro["status"].lower() != 'ativado' and todos == False:
#        continue
#
#      if membro['plataforma'].lower() != 'vm' and todos == False:
#        continue
#
#
#      if membro['site'] == None:
#        if membro['ambiente'].lower() == 'prd':
#          site = 'ctc_npcn'
#        else:
#          site = 'ctc_nprd'
#      else:
#        site = membro['site']
#
#      if membro['produto'].lower() not in dynamic_inventory:
#        dynamic_inventory[membro['produto']] = {'hosts':[], 'vars':{}}
#
#      dynamic_inventory[membro['produto']]['hosts'].append(membro['servidores_json'][0]['nome'])
#      dynamic_inventory['local'] = {'hosts':['127.0.0.1'], 'vars':{'ansible_connection':'local'}}
#
#      dynamic_inventory[site] = {'hosts':[], 'vars':{}}
#      dynamic_inventory[site] = {'children':[], 'vars': {}}
#      dynamic_inventory[site]['children'].append(membro['produto'])
#
#    dynamic_inventory[ambiente]['children'].append(site)








def filtra_host(lista, var_site):
   list_site = [None, 'ctc_nprd', 'ctc_npcn', 'dtc_npcn', 'ctc_canais', 'dtc_canais']
   print("LIST: {}".format(list_site))
   print("VATSITE: {}".format(var_site))
   if var_site != '':
     if var_site in list_site:
       if host['site'] == var_site:

         for host in lista_membros:

           if host["status"] != 'ativado' and todos == False:
             continue

           if host['plataforma'].lower() != 'vm' and todos == False:
             continue

           # Constroi hostvars
           nome = host['servidores_json'][0]['nome']
           ip = host['servidores_json'][0]['ip']

           dynamic_inventory['_meta']['hostvars'][nome] = {}
           dynamic_inventory['_meta']['hostvars'][nome].update({'ansible_host': ip})
           for key, value in host.items():
             if key == 'servidores_json':
               continue
             dynamic_inventory['_meta']['hostvars'][nome].update({key: value})
     else:
       os.exit(2)
       print("'site' nao eh valido. Segus os campos validos: {}".format(list_site))
   else:
    for host in lista_membros:

      if host["status"] != 'ativado' and todos == False:
        continue

      if host['plataforma'].lower() != 'vm' and todos == False:
        continue

      # Constroi hostvars
      nome = host['servidores_json'][0]['nome']
      ip = host['servidores_json'][0]['ip']

      dynamic_inventory['_meta']['hostvars'][nome] = {}
      dynamic_inventory['_meta']['hostvars'][nome].update({'ansible_host': ip})
      for key, value in host.items():
        if key == 'servidores_json':
          continue
        dynamic_inventory['_meta']['hostvars'][nome].update({key: value})





def hosts_info():
  """ Gera info do hostsvars """
  #print("SITE: {}".format(site))
  #list_site = [None, 'ctc_nprd', 'ctc_npcn', 'dtc_npcn', 'ctc_canais', 'dtc_canais', 'ctc_canais_pix', 'dtc_canais_pix']
  #list_site = [None, 'ctc_nprd', 'ctc_npcn', 'dtc_npcn', 'ctc_canais', 'dtc_canais', 'ctc_canais_pix', 'dtc_canais_pix']
  list_site = [None, 'ctc_nprd', 'ctc_npcn', 'dtc_npcn', 'ctc_canais_pix', 'dtc_canais_pix']

  #if 'site' not in globals():
  #  if site not in list_site:
  #     print("'site' nao eh valido. Segue a lista de site: {}".format(", ".join(list_site[1:])))
  #     sys.exit(1)
  #  lista_servidores = (('acao','listarServidoresCadastrados'),('sistema',sistema),('ambiente',ambiente),('site',site))
  #else:
  #  lista_servidores = (('acao','listarServidoresCadastrados'),('sistema',sistema),('ambiente',ambiente))

  try:
    # Verifica se foi passado o site
    if site:
      if site not in list_site:
        print("'site' nao eh valido. Segue a lista de site: {}".format(", ".join(list_site[1:])))
        sys.exit(1)
      lista_servidores = (('acao','listarServidoresCadastrados'),('sistema',sistema),('ambiente',ambiente),('site',site))
  except NameError:
    lista_servidores = (('acao','listarServidoresCadastrados'),('sistema',sistema),('ambiente',ambiente))


  #lista_servidores = (('acao','listarServidoresCadastrados'),('sistema',sistema),('ambiente',ambiente))
  #lista_servidores = (('acao','listarServidoresCadastrados'),('sistema',sistema),('ambiente',ambiente),('site',site))
  lista_membros = consultaPortal(url,lista_servidores)
  cria_inventario(lista_membros)

  if lista_membros == 'vazio':
    pass

  else:
    #filtra_host(lista_membros,var_site)
    for host in lista_membros:
      if var_site != '':
        if var_site not in list_site:
           print("'site' nao eh valido. Segue a lista de site: {}".format(", ".join(list_site[1:])))
           sys.exit(1)
             #
        if host['site'] == var_site:
          for host in lista_membros:

            if host["status"] != 'ativado' and todos == False:
              continue

            if host['plataforma'].lower() != 'vm' and todos == False:
              continue

            # Constroi hostvars
            nome = host['servidores_json'][0]['nome']
            ip = host['servidores_json'][0]['ip']

            dynamic_inventory['_meta']['hostvars'][nome] = {}
            dynamic_inventory['_meta']['hostvars'][nome].update({'ansible_host': ip})
            for key, value in host.items():
              if key == 'servidores_json':
                continue
              dynamic_inventory['_meta']['hostvars'][nome].update({key: value})
      else:
        for host in lista_membros:

          if host["status"] != 'ativado' and todos == False:
            continue

          if host['plataforma'].lower() != 'vm' and todos == False:
            continue

          # Constroi hostvars
          nome = host['servidores_json'][0]['nome']
          ip = host['servidores_json'][0]['ip']

          dynamic_inventory['_meta']['hostvars'][nome] = {}
          dynamic_inventory['_meta']['hostvars'][nome].update({'ansible_host': ip})
          for key, value in host.items():
            if key == 'servidores_json':
              continue
            dynamic_inventory['_meta']['hostvars'][nome].update({key: value})

#    for host in lista_membros:
#
#      if host["status"] != 'ativado' and todos == False:
#        continue
#
#      if host['plataforma'].lower() != 'vm' and todos == False:
#        continue
#
#      # Constroi hostvars
#      nome = host['servidores_json'][0]['nome']
#      ip = host['servidores_json'][0]['ip']
#
#      dynamic_inventory['_meta']['hostvars'][nome] = {}
#      dynamic_inventory['_meta']['hostvars'][nome].update({'ansible_host': ip})
#      for key, value in host.items():
#        if key == 'servidores_json':
#          continue
#        dynamic_inventory['_meta']['hostvars'][nome].update({key: value})





def lista_inventario():
  """ Lista o inventario """
  hosts_info()
  inventario = json.dumps(dynamic_inventory, indent = 4, sort_keys = True)
  print(inventario)
  return inventario

def lista_host(hosts):
  """ Traz informacoes do host """
  hosts_info()
  for host in hosts:
    try:
      inventario = json.dumps(dynamic_inventory['_meta']['hostvars'][host], indent = 4, sort_keys = True)
      print(inventario)
    except KeyError as e:
      print(host + ': servidor inexistente')


my_args = argparse.ArgumentParser(description="Ansible Inventory Caixa")
my_args.add_argument('--list', action='store_true' , help="Lista")
my_args.add_argument('--host', nargs='+', metavar='HOSTNAME', help="Lista os hosts do ambiente")
my_args.add_argument('-s','--sistema', nargs='?', help="'Sistema' pesquisado. Utilize a '--sistema', '-a' ou a variavel de ambiente 'SISTEMANOME'")
my_args.add_argument('-a','--ambiente', nargs='?', help="'Ambiente' pesquisado. Utilize a '--ambiente', '-a' ou a variavel de ambiente 'SISTEMAAMBIENTE'")
my_args.add_argument('--site', nargs='?',default='', help="Pesqusa em um site especifico")
#my_args.add_argument('-p','--produto', nargs='?',default='', help="Pesqusa por um produto especifico")
my_args.add_argument('--all', action='store_true', help="Utilizado com '--list'; mostra todos os cadastros do Sistema e do Ambiente especificado (ex.: container, android, etc).")
my_args.add_argument('--version', action='version', version='%(prog)s 0.1')


args = my_args.parse_args()
#var_site = args.site.lower()

if args.all:
  todos = True

if var_site:
  site = var_site.lower()
elif args.site:
  site = args.site.lower()
#else:
#  print("'site' obrigatorio. Utilize a '--site' ou a variavel de ambiente 'SITE'")
#  sys.exit(2)

if var_sistema:
  sistema = var_sistema.lower()
elif args.sistema:
  sistema = args.sistema.lower()
else:
  print("'Sistema' obrigatorio. Utilize a '--sistema', '-a' ou a variavel de ambiente 'SISTEMANOME'")
  sys.exit(2)

if var_ambiente:
  ambiente = var_ambiente.lower()
elif args.ambiente:
  ambiente = args.ambiente.lower()
else:
  print("'Ambiente' obrigatorio. Utilize a '--ambiente', '-a' ou a variavel de ambiente 'SISTEMAAMBIENTE' ")
  sys.exit(2)


if args.list:
  lista_inventario()

if args.host:
  lista_host(args.host)
