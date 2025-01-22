import subprocess
import requests
import warnings
warnings.filterwarnings("ignore")
from pyrogram import Client , filters, errors, enums
from pyrogram.types import Message, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery, InputMediaDocument, InputMediaPhoto, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto, InlineQueryResultCachedPhoto
from pyrogram.errors import MessageNotModified, PeerIdInvalid
import asyncio
import tgcrypto
import sqlite3
import shutil
from pathlib import Path
from random import randint
import random
import os
from os.path import exists
from time import time,sleep
from datetime import datetime, timedelta, date
import json
import threading
import string
from config import *
import re
import uuid
from urllib.parse import quote, quote_plus, unquote_plus
from time import sleep, localtime, time
import functools
from dateutil.relativedelta import relativedelta
from fake_useragent import UserAgent
import urllib.parse
from PIL import Image

#global vars
bot = Client("bot",api_id=API_ID, api_hash=API_HASH,bot_token=B_TOKEN)
ADMINS = ["raydel0307"]
seg = 0
TEMPORAL = {}
thumb = "thumb.png"

COMPRAS = {}

#Selenium Config
import sys
from selenium import webdriver
from random import randint
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = GOOGLE_CHROME_BIN
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if not os.path.exists("lectulandia"):
	fh = open("lectulandia.zip","wb")
	resp = requests.get("https://github.com/alexjszamora78/profile/raw/main/lectulandia.zip",stream=True)
	for i in resp.iter_content(1024*1024):
		fh.write(i)
	fh.close()
	subprocess.run(["unzip", "lectulandia.zip"])

#fuctions
def pagar_msg(plan,cuota,usid):
	#Medio Semanal
	m = "💳 Seleccione el método de pago a usar\n\n"
	button1 = InlineKeyboardButton("💳 Tarjeta CUP", f"buy {plan} {cuota} CUP")
	button2 = InlineKeyboardButton("📱 Saldo Móvil", f"buy {plan} {cuota} SM")
	button3 = InlineKeyboardButton("⭕️ Cancelar ⭕️", "None")
	buttons = [[button1],[button2],[button3]]
	reply_markup = InlineKeyboardMarkup(buttons)
	return m,reply_markup

def plans_msg(i,usid):
	m = "💳 Premium Subscription\n\n"	
	if i==1:
		m+= "<code>Al comprar la versión Premium podrá:</code>\n"
		m+= "- __Guardar y Compartir los Libros__\n"
		m+= "- __Buscar, Descargar y Solicitar la cantidad de libros que desee sin limite__\n"
		button1 = InlineKeyboardButton("🤩 Comprar 🤩", f"plans PM")
		button2 = InlineKeyboardButton("⭕️ Cancelar ⭕️", "None")
		buttons = [[button1],[button2]]
		reply_markup = InlineKeyboardMarkup(buttons)
	elif i=="PM":
		m+= "- Elija la cuota de tiempo\n"
		button1 = InlineKeyboardButton("🌀 Semanal", f"pagar Premium Semanal")
		button2 = InlineKeyboardButton("🌀 Quincenal (-10%)", f"pagar Premium Quincenal")
		button3 = InlineKeyboardButton("🌀 Mensual (-25%)", f"pagar Premium Mensual")
		button4 = InlineKeyboardButton("⭕️ Cancelar ⭕️", "None")
		buttons = [[button1],[button2],[button3],[button4]]
		reply_markup = InlineKeyboardMarkup(buttons)
	return m,reply_markup

def generar_token():
	caracteres = string.ascii_letters + string.digits
	token = ''.join(random.choices(caracteres, k=8))
	return token

def get_data():
	conexion = sqlite3.connect('datos.db')
	cursor = conexion.cursor()
	cursor.execute("SELECT * FROM bot")
	resultados = cursor.fetchall()
	conexion.close()
	for row in resultados:
		return json.loads(row[1])

def start_msg():
	button0 = InlineKeyboardButton("💠 Ver Canal 💠", url="https://t.me/ultrashell_downloader")
	button1 = InlineKeyboardButton("📚 Como usar este bot", "how")
	button2 = InlineKeyboardButton("💳 Premium Subscription", "plans 1")
	button3 = InlineKeyboardButton("👥 Invite your friends", "invite")
	buttons = [[button0],[button1],[button2],[button3]]
	reply_markup = InlineKeyboardMarkup(buttons)
	m = (
		"<b>📚👑 ¡Bienvenido al reino de los libros digitales! Cada palabra es un tesoro, cada historia un viaje inolvidable 🌟🌈📱. Explora un océano de narrativas fascinantes y mundos por descubrir. ¡Prepárate para una experiencia mágica de lectura en nuestro reino literario 📚💫 Que el poder de la literatura te guíe y cada página te sorprenda con nuevas aventuras! 📖✨</b>"
	)
	return m,reply_markup

def books_buttons(user_id,i=0):
	usid = str(user_id)
	m = "**Select one | Selecciona uno**"
	if i==1:
		vls = [('Arqueología', 'genero/arqueologia/'), ('Arquitectura', 'genero/arquitectura/'), ('Arte', 'genero/arte/'), ('Astrología', 'genero/astrologia/'), ('Astronomía', 'genero/astronomia/'), ('Autoayuda', 'genero/autoayuda/'), ('Autobiográfico', 'genero/autobiografico/'), ('Aventuras', 'genero/aventuras/'), ('Biografía', 'genero/biografia/'), ('Biología', 'genero/biologia/'), ('Bélico', 'genero/belico/'), ('Ciencia', 'genero/ciencia/'), ('Ciencia ficción', 'genero/ciencia-ficcion/'), ('Ciencias exactas', 'genero/ciencias-exactas/'), ('Ciencias naturales', 'genero/ciencias-naturales/'), ('Ciencias sociales', 'genero/ciencias-sociales/'), ('Cine', 'genero/cine/'), ('Cinematografía', 'genero/cinematografia/'), ('Clásico', 'genero/clasico/'), ('Comunicación', 'genero/comunicacion/'), ('Costumbrista', 'genero/costumbrista/'), ('Crítica', 'genero/critica/'), ('Crítica y teoría literaria', 'genero/critica-y-teoria-literaria/'), ('Crónica', 'genero/cronica/'), ('Crónicas', 'genero/cronicas/'), ('Cuentos', 'genero/cuentos/'), ('Cultura', 'genero/cultura/'), ('Cómic', 'genero/comic/'), ('Deporte', 'genero/deporte/'), ('Deportes', 'genero/deportes/'),('Deportes y juegos', 'genero/deportes-y-juegos/'), ('Diccionarios y enciclopedias', 'genero/diccionarios-y-enciclopedias/'), ('Didáctico', 'genero/didactico/'), ('Distopía', 'genero/distopia/'), ('Divulgación', 'genero/divulgacion/'), ('Divulgación científica', 'genero/divulgacion-cientifica/'), ('Drama', 'genero/drama/'), ('Ecología', 'genero/ecologia/'), ('Economía', 'genero/economia/')]
		buttons = []
		for v in vls:
			buttons.append(InlineKeyboardButton(v[0], f"/view_books 1 2 {v[1]}"))
		buttons.append(InlineKeyboardButton("Siguiente ➡️ ", f"mode books generos {i+1}"))
		buttons.append(InlineKeyboardButton("🚫 Cancelar 🚫", "None"))
		listas = agrupar_en_sublistas(buttons,3)
		reply_markup = InlineKeyboardMarkup(listas)
	elif i==2:
		vls = [('Educación', 'genero/educacion/'), ('Ensayo', 'genero/ensayo/'), ('Erótico', 'genero/erotico/'), ('Esoterismo', 'genero/esoterismo/'), ('Espectáculos', 'genero/espectaculos/'), ('Espionaje', 'genero/espionaje/'), ('Espiritualidad', 'genero/espiritualidad/'), ('Fantasía', 'genero/fantasia/'), ('Fantástico', 'genero/fantastico/'), ('Ficción', 'genero/ficcion/'), ('Filosofía', 'genero/filosofia/'), ('Filosófico', 'genero/filosofico/'), ('Física', 'genero/fisica/'), ('Gastronomía', 'genero/gastronomia/'), ('Geografía', 'genero/geografia/'), ('Guion', 'genero/guion/'), ('Historia', 'genero/historia/'), ('Histórico', 'genero/historico/'), ('Hogar', 'genero/hogar/'), ('Humor', 'genero/humor/'), ('Idiomas', 'genero/idiomas/'), ('Infantil', 'genero/infantil/'), ('Infantil y juvenil', 'genero/infantil-y-juvenil/'), ('Informática', 'genero/informatica/'), ('Interactivo', 'genero/interactivo/'), ('Intriga', 'genero/intriga/'), ('Juvenil', 'genero/juvenil/'), ('Magia', 'genero/magia/'), ('Manuales y cursos', 'genero/manuales-y-cursos/'), ('Matemáticas', 'genero/matematicas/'), ('Medicina', 'genero/medicina/'), ('Medieval', 'genero/medieval/'), ('Memorias', 'genero/memorias/'), ('Misterio', 'genero/misterio/'), ('Mitos', 'genero/mitos/'), ('Música', 'genero/musica/'), ('Nazis', 'genero/nazis/'), ('Negocios', 'genero/negocios/'),('No Ficción', 'genero/no-ficcion/')]
		buttons = []
		for v in vls:
			buttons.append(InlineKeyboardButton(v[0], f"/view_books 1 2 {v[1]}"))
		buttons.append(InlineKeyboardButton("⬅️ Atras", f"mode books generos {i-1}"))
		buttons.append(InlineKeyboardButton("🚫 Cancelar 🚫", "None"))
		buttons.append(InlineKeyboardButton("Siguiente ➡️", f"mode books generos {i+1}"))
		listas = agrupar_en_sublistas(buttons,3)
		reply_markup = InlineKeyboardMarkup(listas)
	elif i==3:
		vls = [('Novela', 'genero/novela/'), ('Novela Negra', 'genero/novela-negra/'), ('Novela del Oeste', 'genero/novela-del-oeste/'), ('Obras completas', 'genero/obras-completas/'), ('Otros', 'genero/otros/'), ('Padres e hijos', 'genero/padres-e-hijos/'), ('Periodismo', 'genero/periodismo/'), ('Pintura', 'genero/pintura/'), ('Poesía', 'genero/poesia/'), ('Policial', 'genero/policial/'), ('Policíaco', 'genero/policiaco/'), ('Política', 'genero/politica/'), ('Psicología', 'genero/psicologia/'), ('Psicológico', 'genero/psicologico/'), ('Publicaciónes periódicas', 'genero/publicaciones-periodicas/'), ('Química', 'genero/quimica/'), ('Realista', 'genero/realista/'), ('Recetas de cocina', 'genero/recetas-de-cocina/'), ('Recopilación', 'genero/recopilacion/'), ('Referencia', 'genero/referencia/'), ('Relato', 'genero/relato/'), ('Religión', 'genero/religion/'), ('Romántico', 'genero/romantico/'), ('Salud y Bienestar', 'genero/salud-y-bienestar/'), ('Sexualidad', 'genero/sexualidad/'), ('Sociología', 'genero/sociologia/'), ('Sátira', 'genero/satira/'), ('Teatro', 'genero/teatro/'), ('Tecnología', 'genero/tecnologia/'), ('Terror', 'genero/terror/'), ('Terrorismo', 'genero/terrorismo/'), ('Thriller', 'genero/thriller/'), ('Ucronía', 'genero/ucronia/'), (' ', ' '), ('Viajes', 'genero/viajes/'), (' ', ' ')]
		buttons = []
		for v in vls:
			buttons.append(InlineKeyboardButton(v[0], f"/view_books 1 2 {v[1]}"))
		buttons.append(InlineKeyboardButton("⬅️ Atras", f"mode books generos {i-1}"))
		buttons.append(InlineKeyboardButton("🚫 Cancelar 🚫", "None"))
		listas = agrupar_en_sublistas(buttons,3)
		reply_markup = InlineKeyboardMarkup(listas)
	return m,reply_markup

def agrupar_en_sublistas(lista, n):
	return [lista[i:i+n] for i in range(0, len(lista), n)]

#async fuctions
async def update_data(dates):
	conexion = sqlite3.connect('datos.db')
	cursor = conexion.cursor()
	data = json.dumps(dates)
	id_actualizar = 1
	cursor.execute("UPDATE bot SET data = ? WHERE id = ?", (data, 1))
	conexion.commit()
	conexion.close()

async def lectulandia_download(url,usid):
	data = get_data()
	if data["users"][usid]["books"]>=5 and data["users"][usid]["plan"]=="Free":
		button1 = InlineKeyboardButton("🤩 Comprar 🤩", f"plans 1")
		buttons = [[button1]]
		reply_markup = InlineKeyboardMarkup(buttons)
		await bot.send_message(int(usid),"⁉️ **Ya alcanzaste el límite** ⁉️",reply_markup=reply_markup)
		return
	ua = UserAgent()
	user_agent = ua.random
	chrome_options.add_argument("user-agent={}".format(user_agent))
	chrome_options.add_argument("user-data-dir=lectulandia")
	path = str(randint(10000,999999))
	os.mkdir(path)
	chrome_options.add_experimental_option("prefs",{"download.default_directory" : path})
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(url)
	u = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'downloadB')))
	url = u.get_attribute("href")
	driver.get(url)
	while True:
		r = os.listdir(path)
		if len(r)!=0:
			if not ".crdownload" in r[0]:
				break
	driver.quit()
	a = os.listdir(path)
	return path+"/"+a[0],path

async def lectulandia_details(url,usid):
	data = get_data()
	if data["users"][usid]["books"]>=5 and data["users"][usid]["plan"]=="Free":
		button1 = InlineKeyboardButton("🤩 Comprar 🤩", f"plans 1")
		buttons = [[button1]]
		reply_markup = InlineKeyboardMarkup(buttons)
		await bot.send_message(int(usid),"⁉️ **Ya alcanzaste el límite** ⁉️",reply_markup=reply_markup)
		return
	ua = UserAgent()
	user_agent = ua.random
	chrome_options.add_argument("user-agent={}".format(user_agent))
	chrome_options.add_argument("user-data-dir=lectulandia")
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(url)
	title = driver.find_element(By.ID, "title").text
	msg = f"📚 {title}\n\n"
	covers = driver.find_element(By.ID, "cover").find_elements(By.XPATH, f'//img')
	for c in covers:
		if c.get_attribute("title")==title:
			cover = c.get_attribute("src")
	genero = driver.find_elements(By.XPATH, '//a[@class="dinSource"]')
	gen = "|"
	for g in genero:
		gen+=f"{g.text}|"
	msg+=gen+"\n"
	sinopsis = driver.find_element(By.ID, "sinopsis").text
	msg+=f"\n<u>Sinopsis</u>:\n{sinopsis}\n"
	books = driver.find_element(By.ID, "downloadContainer").find_elements(By.XPATH, "//a[@target='_blank']")
	epub = books[0].get_attribute("href")
	pdf = books[1].get_attribute("href")
	id1 = str(randint(100000,99999999))
	id2 = str(randint(100000,99999999))
	TEMPORAL[id1] = (epub,title,cover)
	TEMPORAL[id2] = (pdf,title,cover)
	buttons = []
	buttons.append([InlineKeyboardButton("📘 Epub", f"/book_d {id1}"),InlineKeyboardButton("📗 PDF", f"/book_d {id2}")])
	reply_markup = InlineKeyboardMarkup(buttons)
	driver.quit()
	return msg,reply_markup,cover

async def lectulandia_alls(texto,tp,usid):
	try:
		data = get_data()
		if data["users"][usid]["books"]>=5 and data["users"][usid]["plan"]=="Free":
			button1 = InlineKeyboardButton("🤩 Comprar 🤩", f"plans 1")
			buttons = [[button1]]
			reply_markup = InlineKeyboardMarkup(buttons)
			await bot.send_message(int(usid),"⁉️ **Ya alcanzaste el límite** ⁉️",reply_markup=reply_markup)
			return
		ua = UserAgent()
		user_agent = ua.random
		chrome_options.add_argument("user-agent={}".format(user_agent))
		chrome_options.add_argument("user-data-dir=lectulandia")
		driver = webdriver.Chrome(options=chrome_options)
		if tp==0:
			driver.get(f"https://ww3.lectulandia.com/search/{urllib.parse.quote(texto)}")
		elif tp==1:
			driver.get("https://ww3.lectulandia.com/")
		elif tp==2:
			driver.get("https://ww3.lectulandia.com/"+texto)
		bs = driver.find_elements(By.CLASS_NAME, "card")
		results = []
		for b in bs:
			title = b.find_element(By.CLASS_NAME, "cover").get_attribute("title")
			photo_url = b.find_element(By.CLASS_NAME, "cover").get_attribute("src")
			url = b.find_element(By.CLASS_NAME, "card-click-target").get_attribute("href")
			results.append((title,photo_url,url))
			if len(results)==49:
				break
		driver.quit()
		return results
	except Exception as ex:
		await bot.send_message("raydel0307",str(ex))
		try:return lectulandia_alls(texto,tp,usid)
		except:return []

async def send_db():
	mensaje = await bot.get_messages(chat_id=CHANNEL_ID, message_ids=ID_FILE)
	nueva_media = InputMediaDocument("datos.db",caption=str(random.randint(10000,99999)))
	await bot.edit_message_media(chat_id=CHANNEL_ID,message_id=ID_FILE,media=nueva_media)
	print("save_db")

async def check(username,usid):
	data = get_data()
	if not usid in data["users"]:
		date_init = str(datetime.now().date())
		data["users"][usid] = {
			"building":False,
			"date_init":date_init,
			"date_end":None,
			"plan":"Free",
			"forward":True,
			"invite_by":None,
			"token":generar_token(),
			"invited":0,
			"books":0,
		}
		await update_data(data)

#client
@bot.on_message(filters.private)
async def start(client: Client, message: Message):
	async def worker(client: Client, message: Message):
		global thumb
		user_id = message.from_user.id
		otm = message.text
		usid = str(user_id)
		username = message.from_user.username
		data = get_data()
		first_name = message.from_user.first_name
		await check(username,usid)
		data = get_data()
		if not "alls" in data["users"]:
			data["users"]["alls"] = []
		if not os.path.exists("downloads/"):
			os.mkdir("downloads/")
		if not os.path.exists("downloads/"+username):
			os.mkdir("downloads/"+username)
		if not user_id in data["users"]["alls"]:
			data["users"]["alls"].append(user_id)
			await update_data(data)
		if not user_id in data["members"]:
			await message.delete()
			m = "Debes estar unido a este canal para continuar"
			button1 = InlineKeyboardButton("🌀 UNIRME 🌀", url="https://t.me/ultrashell_downloader")
			button2 = InlineKeyboardButton("✅ Verificar", "verificar")
			buttons = [[button1],[button2]]
			reply_markup = InlineKeyboardMarkup(buttons)
			await bot.send_message(user_id,m,reply_markup=reply_markup)
			if message.text:
				v = otm.split(" ")
				if len(v)==2:
					if "start" in v[0]:
						pass
			else:
				return
		if message.photo and data["users"][usid]["building"]==True:
			caption = "#Books #Pago de:\n\n"
			caption+=f"👤 `{user_id}`\n"
			caption+=f"👤 `{username}`\n\n"
			caption+=f"`> {COMPRAS[usid]} <`"
			buttons = []
			buttons.append([InlineKeyboardButton("Done", f"/v {user_id} {COMPRAS[usid]}")])
			reply_markup = InlineKeyboardMarkup(buttons)
			await bot.send_photo(PagosPeticiones,photo=message.photo.file_id,caption=caption,reply_markup=reply_markup)
			data["users"][usid]["building"]=False
			COMPRAS.pop(usid)
			await update_data(data)
			await bot.send_message(user_id,"👤 Su pago esta siento revisado por un administrador, puede demorar de minutos a unas horas\n\n☕️ Por favor, espere ...")
			return
		if otm.startswith("/send_db") and username in ADMINS:
			await send_db()
			await bot.send_message(username,"Done")
		elif otm.startswith("/post") and username in ADMINS:
			users = []
			for us,value in data["users"].items():
				if us!="alls":
					users.append(int(us))
			msg = message.reply_to_message
			v = otm.split("/post ")
			if len(v)==2:
				tc = v[1].split("-")
				if "http" in tc[1]:
					button1 = InlineKeyboardButton(tc[0], url=tc[1])
				elif "!" in tc[1]:
					button1 = InlineKeyboardButton(tc[0], url="https://t.me/ultrashell_bot?start="+tc[1].split("!")[1])
				else:
					button1 = InlineKeyboardButton(tc[0], tc[1])
				buttons = [[button1]]
				reply_markup = InlineKeyboardMarkup(buttons)
			else:
				reply_markup = None

			if msg.text:
				for i in users:
					try:
						if data["users"][str(i)]["plan"]=="Free":
							if reply_markup:await bot.send_message(i,msg.text,reply_markup=reply_markup)
							else:await bot.send_message(i,msg.text)
					except:pass
			elif msg.photo:
				for i in users:
					try:
						if data["users"][str(i)]["plan"]=="Free":
							if reply_markup:await bot.send_photo(i,photo=msg.photo.file_id,caption=msg.caption,reply_markup=reply_markup)
							else:await bot.send_photo(i,photo=msg.photo.file_id,caption=msg.caption)
					except:pass
			elif msg.video:
				for i in users:
					try:
						if data["users"][str(i)]["plan"]=="Free":
							if reply_markup:await bot.send_video(i,video=msg.video.file_id,caption=msg.caption,reply_markup=reply_markup)
							else:await bot.send_video(i,video=msg.video.file_id,caption=msg.caption)
					except:pass
			elif msg.document:
				for i in users:
					try:
						if data["users"][str(i)]["plan"]=="Free":
							if reply_markup:await bot.send_document(i,document=msg.document.file_id,caption=msg.caption,reply_markup=reply_markup)
							else:await bot.send_document(i,document=msg.document.file_id,caption=msg.caption)
					except:pass
			s = await bot.send_message("raydel0307","Done")
			await asyncio.sleep(3)
			await s.delete()
		elif otm.startswith("/users") and username in ADMINS:
			fn = "free-users.txt"
			mn = "medium-users.txt"
			un = "ultra-users.txt"
			f = open(fn,"w")
			m = open(mn,"w")
			u = open(un,"w")
			for usid,value in data["users"].items():
				try:
					if usid!="alls":
						msg = await bot.get_chat(int(usid))
						if data["users"][usid]["plan"]=="Free":
							f.write(f"{usid} @{msg.username} {data['users'][usid]['tokens']}\n")
						elif data["users"][usid]["plan"]=="Medio":
							m.write(f"{usid} @{msg.username} {data['users'][usid]['tokens']} {data['users'][usid]['date_end']}\n")
						elif data["users"][usid]["plan"]=="Ultra":
							u.write(f"{usid} @{msg.username} {data['users'][usid]['tokens']} {data['users'][usid]['date_end']}\n")
				except Exception as ex:
					print(ex)
					pass
			try:
				f.close()
				await bot.send_document("raydel0307",document=fn,caption="Free Users",thumb=thumb)
				os.unlink(fn)
			except:pass
			try:
				m.close()
				await bot.send_document("raydel0307",document=mn,caption="Medium Users",thumb=thumb)
				os.unlink(mn)
			except:pass
			try:
				u.close()
				await bot.send_document("raydel0307",document=un,caption="Ultra Users",thumb=thumb)
				os.unlink(un)
			except:pass
		elif otm.startswith("/books"):
			v = otm.split("/books ")
			m = await bot.send_message(user_id,"[...] Buscando Libros [...]")
			if len(v)==2:
				texto = v[1]
				results = await lectulandia_alls(texto,0,usid)
				buttons = []
				if len(results)!=0:
					for title,photo_url,url in results:
						ids = str(randint(10000,999999))
						TEMPORAL[ids] = url
						button1 = InlineKeyboardButton(title, f"/view_books 0 {ids}")
						buttons.append([button1])
						if len(buttons)>=20:
							break
					reply_markup = InlineKeyboardMarkup(buttons)
					await m.edit(f"🔎 Encontrados [{len(results)}]\n📚 {texto}",reply_markup=reply_markup)
			else:
				button0 = InlineKeyboardButton("Géneros","/view_books 1 generos")
				button1 = InlineKeyboardButton("Novedades", "/view_books 1 1 .")
				button2 = InlineKeyboardButton("Los más leídos de la semana", "/view_books 1 2 compartidos-semana/")
				button3 = InlineKeyboardButton("Los más leídos del mes", "/view_books 1 2 compartidos-mes/")
				button4 = InlineKeyboardButton("Los más comentados", "/view_books 1 2 mas-comentados/")
				buttons = [[button0,button1],[button2],[button3],[button4]]
				buttons.append([InlineKeyboardButton("🚫 Cancelar 🚫", "None")])
				reply_markup = InlineKeyboardMarkup(buttons)
				await m.edit("Seleccione uno",reply_markup=reply_markup)
		elif otm.startswith("/start"):
			await message.delete()
			v = otm.split(" ")
			if len(v)==2:
				try:
					id = v[1]
					if not data["users"][usid]["invite_by"]:
						for uid, udata in data["users"].items():
							if uid!=usid:
								if "token" in udata and udata["token"] == id:
									data["users"][usid]["invite_by"]=uid
									data["users"][uid]["invited"]+=1
									await update_data(data)
									await bot.send_message(int(uid),"+1 Un nuevo usuario a usado su link de referencia")
									break
					else:
						await bot.send_message(username,"🌐 Ya usted pertenece a nuestro servicio")
				except Exception as ex:
					print(ex)
					pass
			m,reply_markup = start_msg()
			m+=f"\n\n<b>Plan:</b> __{data['users'][usid]['plan']}__\n"
			m+=f"<b>Referidos:</b> __{data['users'][usid]['invited']}__\n"
			m+=f"<b>Libros Descargados:</b> __{data['users'][usid]['books']}__\n"
			if data["users"][usid]["plan"]!="Free":
				data_end = datetime.strptime(data["users"][usid]["date_end"], "%Y-%m-%d").date()
				actual = datetime.now().date()
				m+=f"\n<b>Days Remaining:</b> __{(data_end-actual).days}__"
			await bot.send_message(username,m,reply_markup=reply_markup)
		elif otm.startswith("/db") and username in ADMINS:
			await message.delete()
			d = json.dumps(data["users"])
			txt = open("db_user.txt","w")
			txt.write(d)
			txt.close()
			d = json.dumps(data)
			txt = open("db.txt","w")
			txt.write(d)
			txt.close()
			await bot.send_document(username,"db.txt")
			await bot.send_document(username,"db_user.txt")
			os.unlink("db.txt")
			os.unlink("db_user.txt")
		elif otm.startswith("/ban") and username in ADMINS:
			try:
				i=int(otm.split(" ")[1])
				data["users"].pop(str(i))
			except:
				i=otm.split(" ")[1]
				user = await bot.get_chat(i)
				data["users"].pop(str(user.id))
			await update_data(data)
			await bot.send_message(username,f'{otm.split(" ")[1]} eliminado')
	bot.loop.create_task(worker(client, message))

#button_callback
@bot.on_callback_query()
async def callback_data(bot,callback):
	username = callback.from_user.username
	first_name = callback.from_user.first_name
	user_id = callback.from_user.id
	usid = str(user_id)
	d = str(callback.data).split(" ")
	message = callback.message
	data = get_data()
	thumb = "thumb.png"
	f = data["users"][usid]["forward"]
	if d[0]=="how":
		m = """
		Manual de Ayuda para el Comando /books

		¡Hola, lectores ávidos! 👋

		El comando /books es tu puerta de entrada a un mundo de literatura ilimitada. ¡Aquí tienes una guía rápida para ayudarte a navegar por sus características!

		Uso básico:

		• Simplemente escribe /books para desplegar un menú con las siguientes opciones:

		  * Últimos libros 📚
		  * Categorías 📚
		  * Más leídos 🏆

		Búsqueda específica:

		• Para buscar un libro específico, simplemente escribe /books seguido del título del libro. Por ejemplo:

		  * /books A través de mi ventana

		Opciones avanzadas:

		• Filtrar por categoría: Puedes filtrar los resultados por categoría seleccionando una de las opciones del menú desplegable.
		• Ordenar por popularidad: La opción "Más leídos" ordena los libros según su popularidad entre los usuarios.
		• Puede ver los 10 libros más recientes agregados.
		• Para buscar libros de romance, escribe /books Categorías > Romance.
		• Para encontrar el libro "Crepúsculo", escribe /books Crepúsculo.

		Consejos:

		• Usa palabras clave relevantes en tus búsquedas para obtener resultados más precisos.
		• Explora las diferentes categorías para descubrir nuevos géneros y autores.
		• No olvides consultar la opción "Más leídos" para encontrar los libros más populares entre la comunidad.

		¡Sumérgete en un mundo de historias con el comando /books! 📖✨
		"""
		await bot.send_message(user_id,m)
	elif d[0]=="invite":
		m = """
		¡Atención, lectores! 📢📚

		¿Estás listo para sumergirte en un mundo de historias cautivadoras? ¡Nuestro servidor tiene todo lo que necesitas para satisfacer tu sed de lectura!

		Con nuestro comando mágico /books, puedes:

		• Explorar los últimos lanzamientos 🆕 para mantenerte al día con los éxitos de taquilla literarios.
		• Descubrir nuevas categorías 📚 y ampliar tus horizontes de lectura.
		• Encontrar los libros más leídos 🏆 y unirte a la conversación sobre las obras más populares.

		¿Quieres algo específico? ¡Solo escribe el título del libro! Nuestro servidor te lo entregará de inmediato. 🪄

		¡Comparte este mensaje con tus amigos amantes de los libros 👬👭 y juntos creemos una comunidad de lectores apasionados! 📚✨

		#Lectura #Libros #ComunidadLiteraria
		"""
		button1 = InlineKeyboardButton("🌀 UNIRME 🌀", url=f"https://t.me/empire_books_bot?start={data['users'][usid]['token']}")
		buttons = [[button1]]
		reply_markup = InlineKeyboardMarkup(buttons)
		await message.delete()
		await bot.send_message(username,f"🔗 <b>Comparta ese post para que nuevos lectores se unan</b>\n\n- Actualmente a añadido {data['users'][usid]['invited']} usuarios")
		await bot.send_message(user_id,m,reply_markup=reply_markup)
	elif d[0]=="None":
		try:await message.delete()
		except:pass
	elif d[0]=="buy":
		#buy {plan} {cuota} CUP
		PRECIOS = {"Premium":{
			"Semanal":{"CUP":50,"SM":50},
			"Quincenal":{"CUP":90,"SM":90},
			"Mensual":{"CUP":150,"SM":150}
			}
		}
		if d[1]=="None":
			data["users"][usid]["building"] = True
			await update_data(data)
			await message.delete()
			return
		if not usid in COMPRAS:
			COMPRAS[usid] = None
		COMPRAS[usid] = f"{d[1]} {d[2]} {PRECIOS[d[1]][d[2]][d[3]]} {d[3]}"
		m = f"👉 Envíe el equivalente a {PRECIOS[d[1]][d[2]][d[3]]} CUP\n\n"
		m+= "👤 <u>Destintario<u>\n"
		if d[3]=="CUP":
			m+="`9205 1299 7961 0491`\n\n"
			m+="👤 # a Confirmar\n"
			m+="`51605779`\n\n"
		elif d[3]=="SM":
			m+="`51605779`\n"
		m+="👀 Y envíe una captura de pantalla dentro de este bot con los datos de la transferencia para concluir la compra\n"
		m+="🗣 No envíe datos falsos porque se le será baneado por completo\n"
		m+="🗣 No oculte hora ni datos de la transferencia"
		await message.delete()
		button1 = InlineKeyboardButton("⭕️ Cancelar ⭕️", "buy None")
		buttons = [[button1]]
		reply_markup = InlineKeyboardMarkup(buttons)
		await bot.send_message(user_id,m,reply_markup=reply_markup)
		data["users"][usid]["building"] = True
		await update_data(data)
	elif d[0]=="pagar":
		#pagar Premium Semanal
		m,reply_markup = pagar_msg(d[1],d[2],usid)
		await message.edit(m,reply_markup=reply_markup)
	elif d[0]=="plans":
		try:i=int(d[1])
		except:i=d[1]
		m,reply_markup = plans_msg(i,usid)
		await message.edit(m,reply_markup=reply_markup)
	elif d[0]=="/view_books":
		if d[1]=="0":
			try:url = TEMPORAL[d[2]]
			except:
				await message.delete()
				a = await bot.send_message(user_id,"🔖 Vuelva a realizar la busqueda del libro con el comando /books")
				await asyncio.sleep(5)
				await a.delete()
				return
			msg = await bot.send_message(user_id,"🔎 Buscando Libro...")
			try:
				mg,reply_markup,photo_url = await lectulandia_details(url,usid)
				fi = str(randint(10000,999999))+".jpg"
				f = open(fi,"wb")
				resp = requests.get(photo_url,stream=True)
				for i in resp.iter_content(1024*1024):
					f.write(i)
				f.close()
				imagen = Image.open(fi)
				ancho, alto = imagen.size
				nueva_altura = alto - 50
				imagen_recortada = imagen.crop((0, 0, ancho, nueva_altura))
				imagen_recortada.save(fi+".jpg")
				await msg.delete()
				try:await bot.send_photo(int(usid),photo=fi+".jpg",caption=mg,reply_markup=reply_markup)
				except:
					await bot.send_photo(int(usid),photo=fi+".jpg")
					await bot.send_message(int(usid),mg,reply_markup=reply_markup)
				os.unlink(fi)
				os.unlink(fi+".jpg")
			except Exception as ex:
				print(ex)
				await msg.edit("No se pudo obtener información del Libro")
				pass
		elif d[1]=="1":
			#"/view_books 1 generos"
			if d[2]=="generos":
				msg,reply_markup = books_buttons(user_id,i=1)
				await message.edit(msg,reply_markup=reply_markup)
			else:
				await message.delete()
				ids = int(d[2])
				texto = d[3]
				m = await bot.send_message(user_id,"Buscando Libros")
				results = await lectulandia_alls(texto,ids,usid)
				buttons = []
				if len(results)!=0:
					for title,photo_url,url in results:
						ids = str(randint(10000,999999))
						TEMPORAL[ids] = url
						button1 = InlineKeyboardButton(title, f"/view_books 0 {ids}")
						buttons.append([button1])
						if len(buttons)>=20:
							break
					reply_markup = InlineKeyboardMarkup(buttons)
					await m.edit(f"🔎 Encontrados [{len(results)}]\n📚 {texto}",reply_markup=reply_markup)
	elif d[0]=="/book_d":
		try:
			#(epub,title,cover)
			await message.delete()
			if not "saved" in data:
				data["saved"] = {}
			msg = await bot.send_message(user_id,"😊 <u>Descargando Libro</u>")
			file,path = await lectulandia_download(TEMPORAL[d[1]][0],usid)
			data = get_data()
			data["users"][usid]["books"]+=1
			await update_data(data)
			data = get_data()
			fi = str(randint(10000,999999))+".jpg"
			fa = open(fi,"wb")
			resp = requests.get(TEMPORAL[d[1]][2],stream=True)
			for i in resp.iter_content(1024*1024):
				fa.write(i)
			fa.close()
			await bot.send_document(user_id,document=file,thumb=fi,caption=f"{TEMPORAL[d[1]][1]}\n@ultrashell_bot",protect_content=f)
			shutil.rmtree(path)
			os.unlink(fi)
			os.unlink(file)
			TEMPORAL.pop(d[1])
			await msg.delete()
		except Exception as ex:
			print("ex",ex)
			await message.delete()
			await bot.send_message(user_id,"Libro no disponible, búsquelo denuevo")
	elif d[0]=="/v":
		#/v 6023437531 Medio Quincenal 190 CUP
		uid = d[1]
		plan = d[2]
		cuota = d[3]
		data["users"][uid]["plan"]=plan
		data["users"][uid]["forward"]=False
		date_init = datetime.now().date()
		if cuota=="Semanal":
			date_end = date_init + relativedelta(days=7)
		elif cuota=="Quincenal":
			date_end = date_init + relativedelta(days=15)
		elif cuota=="Mensual":
			date_end = date_init + relativedelta(months=1)
		data["users"][uid]["date_init"] = str(date_init)
		data["users"][uid]["date_end"] = str(date_end)
		await update_data(data)
		await message.delete()
		await bot.send_message(int(uid),"🥳")
		await bot.send_message(int(uid),"**Plan Actualizado**\n\nPulse /start")
	elif d[0]=="pagar":
		m,reply_markup = pagar_msg(d[1],d[2],usid)
		await message.edit(m,reply_markup=reply_markup)
	elif d[0]=="verificar":
		members = await get_chat_members(r=True)
		if user_id in members:
			await message.edit("<b>✅ !Listo!</b>\n\n👉 Mande /start para continuar")
		else:
			s = await bot.send_message(user_id,"No se a unido")
			await asyncio.sleep(3)
			await s.delete()
	elif d[0]=="mode":
		if d[1]=="books":
			if d[2]=="0":
				msg,reply_markup = books_buttons(user_id)
				await message.edit(msg,reply_markup=reply_markup)
			elif d[2]=="generos":
				try:i = int(d[3])
				except:i = 1
				msg,reply_markup = books_buttons(user_id,i=i)
				await message.edit(msg,reply_markup=reply_markup)
			return

#tasks
def save_db():
	while True:
		sleep(150)
		asyncio.run(send_db())

async def verify_dates_users():
	data = get_data()
	for usid,value in data["users"].items():
		if usid!="alls" and data["users"][usid]["plan"]!="Free":
			data_end = datetime.strptime(data["users"][usid]["date_end"], "%Y-%m-%d").date()
			actual = datetime.now().date()
			if actual>data_end:
				data["users"][usid]["plan"] = "Free"
				data["users"][usid]["forward"] = True
				data["users"][usid]["date_end"] = None
				await update_data(data)

async def download_db():
	msg = await bot.get_messages(CHANNEL_ID,message_ids=ID_FILE)
	try:os.unlink("datos.db")
	except:pass
	try:os.unlink("downloads/datos.db")
	except:pass
	await msg.download(file_name="datos.db")
	os.rename(f"downloads/datos.db","datos.db")
	await get_chat_members()
	await verify_dates_users()

async def get_chat_members(r=False):
	data = get_data()
	us = []
	if not "members" in data:
		data["members"] = []
	async for i in bot.get_chat_members(MyCHANNEL):
		user_id = i.user.id
		if not user_id in data["members"]:
			us.append(user_id)
	if not 1806431279 in us:
		us.append(1806431279)
	if not 7120774259 in us:
		us.append(7120774259)
	data["members"] = us
	await update_data(data)
	print("members",len(us))
	if r:
		return us

async def initbot():
	await bot.send_message("raydel0307","**Bot-Reiniciado**")

print("started")
bot.start()
bot.loop.create_task(download_db())
bot.loop.create_task(initbot())
backup_thread = threading.Thread(target=save_db)
backup_thread.daemon = True
backup_thread.start()
print("""
···INICIADO···
""")
bot.loop.run_forever()