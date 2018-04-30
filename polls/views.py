# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.template import RequestContext, loader
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from twython import Twython  
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import re
def index(request):
	# consumer_key = "694VnNmdaQWvMqyb2qA7UjLaL"
	# consumer_secret = "CfTL1wnftIavKQZPa0K9e26oKAHteIheUUQz8EeMeTqiAvrXvw"
	# access_token  ="974318757815472130-Flm3bmXS6jP0imR6NggglcYN54x7Pth"
	# access_token_secret  ='xXDaNdnU6qYY2EoR5QIm392ICBDnBPnSh9P6UlFO4EG1J'
	# api = Twython(app_key=consumer_key, app_secret=consumer_secret, oauth_token=access_token, oauth_token_secret=access_token_secret)
	# data = api.get_followers_list(screen_name='joanribo')

	# latest_question_list = data['users']
	
	latest_question_list = ""
	#Template 
	template = loader.get_template('polls/index.html')
	context = {'latest_question_list': latest_question_list}
	return HttpResponse(template.render(context))

@csrf_exempt
def panelControl(request):
	if request.method == 'POST':
		if request.POST.get('name', False):
			name = request.POST['name']
			consumer_key = "694VnNmdaQWvMqyb2qA7UjLaL"
			consumer_secret = "CfTL1wnftIavKQZPa0K9e26oKAHteIheUUQz8EeMeTqiAvrXvw"
			access_token  ="974318757815472130-Flm3bmXS6jP0imR6NggglcYN54x7Pth"
			access_token_secret  ='xXDaNdnU6qYY2EoR5QIm392ICBDnBPnSh9P6UlFO4EG1J'
			api = Twython(app_key=consumer_key, app_secret=consumer_secret, oauth_token=access_token, oauth_token_secret=access_token_secret)
			
			#QUE EL NOMBRE NO TENGA @
			removeAt = re.search('\w+', name)
			name = removeAt.group(0)
			data = api.get_followers_list(screen_name=name)
			usuarios = {}
			for usuario in data['users']:
				perfilFalso = 0

				#Nombre de usuario
				print usuario['screen_name']

				#ID USUAIRO
				# print usuario['id']

				#IMAGEN POR DEFECTO
				if 'true' == usuario['default_profile_image']:
					perfilFalso+=1


				#DESCRIPCION
				if "" == usuario['description']:
					perfilFalso+=1


				#Imagen del background
				if 'null' == usuario['profile_background_image_url']:
					perfilFalso+=1


				#Me gustas o favoritos en twitter
				if 0 == usuario['favourites_count'] :
					perfilFalso+=1



				#Esta siguiendo
				if 50 >= usuario['friends_count']:
					perfilFalso+=1

				print usuario['created_at']
				# print datetime.datetime.strptime(usuario['created_at'], "%a %b %d %Y").strftime("%d/%m/%Y")
				#Fecha de cracion de cuenta
				# if usuario['created_at'] :
				# 	perfilFalso++


				#Personas que le siguen
				if 20 > usuario['followers_count'] :
					perfilFalso+=1

				usuarios[usuario['screen_name']] = perfilFalso
			usrFalsos = 0
			usrSospect = 0
			usrAnalized = len(usuarios)
			for key, value in usuarios.iteritems():
				if 4 <= value:
					usrFalsos+=1
				elif 2 <= value:
					usrSospect+=1

			context = {'usrFalsos':usrFalsos, 'usrSospect':usrSospect, 'usrAnalized':usrAnalized}
			template = loader.get_template('polls/dataResult.html')
			return HttpResponse(template.render(context))
	else:
		context = {}
		template = loader.get_template('polls/panelControl.html')
		return HttpResponse(template.render(context))
	

def dataResult(request):
	latest_question_list = ""
	context = {'latest_question_list': latest_question_list}
	template = loader.get_template('polls/dataResult.html')
	return HttpResponse(template.render(context))