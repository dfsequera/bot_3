import telebot
from telebot.types import ReplyKeyboardRemove
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np
import sqlite3
from datetime import datetime 


# Inicializar el bot de Telegram
bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=["start", "ayuda", "help"])
def cmd_start(message):
    username = message.from_user.first_name
    bot.reply_to(message, f"¡Hola! {username}, ¡Bienvenido a EstaGen! Soy tu Asistente Virtual para el área de la Estadística Descriptiva."
    " Mi objetivo es ayudarte en todo lo relacionado con conceptos básicos, cálculos y gráficas estadísticas.")
    markup = ReplyKeyboardRemove()
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Usa el comando /consulta para realizar una consulta, referente a los conceptos en el área de la Estadística Descriptiva.")
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Usa los comandos para realizar los siguientes cálculos:\n"
    "/media para calcular la Media Aritmética.\n/mediana para calcular la Mediana.\n"
    "/moda para calcular la Moda de los datos.\n/var para calcular la Varianza.\n"
    "/desv para calcular la Desvisión Estándar.\nIngresa los datos separados por un espacio")
    bot.send_chat_action(message.chat.id, "typing") 
    bot.send_message(message.chat.id, "Usa los comandos para realizar los siguientes gráficos:\n"
    "/hist para generar un Histograma.\n/line para generar un Gráfico de línea.\n"
    "/pie para generar un Gráfico Circular.\n/histline para generar Histograma y Polígono de Frecuencia.\n"
    "Ingresa los datos separados por un espacio")
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Bienvenida"),
        telebot.types.BotCommand("/consulta", "Pregunta"),
        telebot.types.BotCommand("/media", "Media Aritmética"),
        telebot.types.BotCommand("/mediana", "Mediana"),
        telebot.types.BotCommand("/moda", "Moda"),
        telebot.types.BotCommand("/desv", "Desviación Estándar"),
        telebot.types.BotCommand("/var", "Varianza"),
        telebot.types.BotCommand("/hist", "Histograma"),
        telebot.types.BotCommand("/line", "Gráfico de linea"),
        telebot.types.BotCommand("/pie", "Gráfico Circular"),
        telebot.types.BotCommand("/histline", "Histograma y Polígono de Frecuencias"),

    ])
    # Guardar la información del usuario en la base de datos
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()

    # Obtener la información del usuario
    nombre = message.from_user.first_name
    usuario = message.from_user.username

    # Verificar si el usuario ya existe en la tabla 'usuario'
    c.execute("SELECT * FROM usuario WHERE usuario=?", (usuario,))
    existing_user = c.fetchone()

    if existing_user:
        # El usuario ya existe, actualizar la fecha y hora
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("UPDATE usuario SET fecha_hora=? WHERE usuario=?", (fecha_hora, usuario))
        conn.commit()
    else:
        # El usuario no existe, insertar los datos en la tabla 'usuario'
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO usuario (nombre, usuario, fecha_hora) VALUES (?, ?, ?)", (nombre, usuario, fecha_hora))
        conn.commit()

    # Cerrar la conexión a la base de datos
    c.close()
    conn.close()
# Definir un controlador para el comando /consulta
@bot.message_handler(commands=['consulta'])
def handle_query(message):
    import sqlite3
    # Configurar la conexión a la base de datos
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()

    # Obtener el parámetro pasado por el usuario
    parametro = message.text.split()[1]

    # Ejecutar la consulta y obtener el resultado
    #c.execute("SELECT descr FROM bot WHERE LOWER(nombre)=LOWER(?)", (parametro,))
    c.execute("SELECT descr FROM definicion WHERE LOWER(nombre) LIKE LOWER(?) ORDER BY nombre='parametro' ASC", (f"%{parametro.replace(' ', '%')}%",))
    resultado = c.fetchone()

    # Responder al usuario con el resultado
    bot.send_chat_action(message.chat.id, "typing")
    if resultado:
        bot.reply_to(message, "{}".format(resultado[0]))
    else:
        bot.reply_to(message, "No se encontró resultado para esta consulta, verifica que la estés realizando correctamente.")
# Cierra la conexión a la base de datos
    c.close()
    conn.close()

# Definir un controlador predeterminado para mensajes que no sean comandos
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_invalid_command(message):
    bot.send_chat_action(message.chat.id, "typing")
    command = message.text.split()[0]  # Obtener el comando ingresado
    
    if command == "/media":
        media(message)
    elif command == "/mediana":
        mediana(message)
    elif command == "/moda":
        moda(message)
    elif command == "/desv":
        desv(message)
    elif command == "/var":
        var(message)
    elif command == "/hist":
        hist(message)
    elif command == "/line":
        line(message)
    elif command == "/pie":
        pie(message)
    elif command == "/histline":
        histline(message)
    else:
        bot.reply_to(message, "Lo siento, no entendí ese comando. Por favor, usa uno de los comandos disponibles o revisa la especificación del bot para obtener más información.")

# Crear una función de respuesta de comando para el cálculo de la media
@bot.message_handler(commands=['media'])
def media(message):
  # Obtener los números del mensaje enviado por el usuario
  nums = list(map(float, message.text.split()[1:]))
  
  # Crear un objeto DataFrame con los números
  df = pd.DataFrame(nums, columns=['numbers'])
  
  # Calcular la media utilizando la función mean() de Pandas
  media = df.mean().values[0]
  
  # Enviar respuesta de vuelta al usuario
  respuesta = f"La Media Aritmética de los números {nums} es: {media}"
  bot.send_chat_action(message.chat.id, "typing")
  bot.send_message(message.chat.id, respuesta)

# Crear una función de respuesta de comando para el cálculo de la mediana
@bot.message_handler(commands=['mediana'])
def mediana(message):

  # Obtener los números del mensaje enviado por el usuario
  nums = list(map(float, message.text.split()[1:]))
  
  # Crear un objeto DataFrame con los números
  df = pd.DataFrame(nums, columns=['numbers'])
  
  # Calcular la mediana utilizando la función median() de Pandas
  mediana = df.median().values[0]
  
  # Enviar respuesta de vuelta al usuario
  respuesta = f"La Mediana de los números {nums} es: {mediana}"
  bot.send_chat_action(message.chat.id, "typing")
  bot.send_message(message.chat.id, respuesta)

# Crear una función de respuesta de comando para el cálculo de la moda
@bot.message_handler(commands=['moda'])
def moda(message):
  # Obtener los números del mensaje enviado por el usuario
  nums = list(map(float, message.text.split()[1:]))
  
  # Crear un objeto DataFrame con los números
  df = pd.DataFrame(nums, columns=['numbers'])
  
  # Calcular la moda utilizando la función mode() de Pandas
  moda = df.mode()
  
  # Enviar respuesta de vuelta al usuario
  respuesta = f"La(s) Moda(s) de los números {nums} es: {', '.join(map(str, moda.values.tolist()[0]))}"
  bot.send_chat_action(message.chat.id, "typing")
  bot.send_message(message.chat.id, respuesta)


@bot.message_handler(commands=['desv'])
def desv(message):

  # Obtener los números del mensaje enviado por el usuario
  nums = list(map(float, message.text.split()[1:]))

# Crear un objeto DataFrame con los números
  df = pd.DataFrame(nums, columns=['numbers'])

# Calcular la desviación estándar utilizando las función std() de Pandas
  desv_est = df.std().values[0]

  # Enviar respuesta de vuelta al usuario
  respuesta = f"La Desviación Estándar de los números {nums} es: {desv_est}"
  bot.send_chat_action(message.chat.id, "typing")
  bot.send_message(message.chat.id, respuesta)

@bot.message_handler(commands=['var'])
def var(message):
    # Obtener los números del mensaje enviado por el usuario
    nums = list(map(float, message.text.split()[1:]))

    # Crear un objeto DataFrame con los números
    df = pd.DataFrame(nums, columns=['numbers'])

    # Calcular la varianza utilizando la función var() de Pandas
    varianza = df.var().values[0]

    # Enviar respuesta de vuelta al usuario
    respuesta = f"La Varianza de los números {nums} es: {varianza}"
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, respuesta)

# Establecer la variable de entorno MPLBACKEND para usar Agg
os.environ['MPLBACKEND'] = 'Agg'

# Obtener los datos ingresados por el usuario en Telegram
@bot.message_handler(commands=['hist'])
def hist(message):
    text = message.text
    # Convertir los valores en una lista
    data = list(map(int, text.split()[1:]))
    # Crear el gráfico a partir de los datos
    create_plot(data, bot, message.chat.id)

# Crear el gráfico a partir de los datos
def create_plot(data, bot, chat_id):
    # Crear el histograma
    plt.hist(data, bins=10)
    plt.title('Histograma')
    # Guardar la figura en un buffer de memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    # Enviar la figura como mensaje en Telegram
    buf.seek(0)
    bot.send_photo(chat_id=chat_id, photo=buf)
    plt.clf()
    
@bot.message_handler(commands=['pie'])
def pie(message):
    text = message.text
    # Convertir los valores en una lista
    data = list(map(int, text.split()[1:]))
    # Crear el gráfico a partir de los datos
    create_pie(data, bot, message.chat.id)

# Crear el gráfico a partir de los datos
def create_pie(data, bot, chat_id):
    # Crear el gráfico circular
    plt.pie(data)
    plt.title('Gráfico Circular')
    # Agregar las etiquetas a cada porción del gráfico
    plt.legend(labels=data, loc="best")
    # Guardar la figura en un buffer de memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    # Enviar la figura como mensaje en Telegram
    buf.seek(0)
    bot.send_photo(chat_id=chat_id, photo=buf)
    plt.clf()


@bot.message_handler(commands=['line'])
def line(message):
    text = message.text
    # Convertir los valores en una lista
    data = list(map(int, text.split()[1:]))
    # Crear el gráfico a partir de los datos
    create_line(data, bot, message.chat.id)

# Crear el gráfico de línea a partir de los datos
def create_line(data, bot, chat_id):
    plt.title('Gráfico de Línea')
    # Crear el gráfico de línea
    plt.plot(data)
    # Guardar la figura en un buffer de memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    # Enviar la figura como mensaje en Telegram
    buf.seek(0)
    bot.send_photo(chat_id=chat_id, photo=buf)
    plt.clf()

@bot.message_handler(commands=['histline'])
def histline(message):
    text = message.text
    # Convertir los valores en una lista
    data = list(map(int, text.split()[1:]))
    # Crear el gráfico a partir de los datos
    create_histline(data, bot, message.chat.id)

# Crear el histograma y el polígono de frecuencia a partir de los datos
def create_histline(data, bot, chat_id):
    # Calcular los valores del histograma y el polígono de frecuencia
    values, edges, _ = plt.hist(data, bins=10, density=True)
    midpoints = (edges[:-1] + edges[1:]) / 2
    density = np.sum(values * np.diff(edges))
    plt.plot(midpoints, values)
    # Crear el título y la etiqueta Y del gráfico
    plt.title('Histograma y Polígono de Frecuencia')
    plt.ylabel('Frecuencia')
    # Mostrar la densidad en el gráfico
    plt.text(0.95, 0.95, f'Densidad: {density:.2f}', ha='right', va='top', transform=plt.gca().transAxes)
    # Guardar la figura en un buffer de memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    # Enviar la figura como mensaje en Telegram
    buf.seek(0)
    bot.send_photo(chat_id=chat_id, photo=buf)    
    plt.clf()

# Ejecuta el bot
if __name__ == '__main__':
    print('Bot Iniciado')
    bot.infinity_polling()
