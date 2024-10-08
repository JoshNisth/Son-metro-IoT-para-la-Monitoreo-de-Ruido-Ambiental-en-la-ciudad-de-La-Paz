import mysql.connector
import math
import random
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración de la conexión a la base de datos
DB_HOST = "192.168.8.55"  # Cambia esto por la IP de tu laptop (servidor)
DB_USER = "josh"  # Cambia esto por tu nombre de usuario de MySQL
DB_PASS = ""  # Cambia esto por tu contraseña de MySQL
DB_NAME = "sonometro"

def conectar():
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
        return None

# Funciones de la interfaz de login
def verificar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    query = "SELECT idUsuario, nombreUsuario FROM usuario WHERE nombreUsuario = %s AND password = %s"
    cursor.execute(query, (usuario, contrasena))
    resultado = cursor.fetchone()

    if resultado:
        id_usuario = resultado[0]
        messagebox.showinfo("Login exitoso", f"Bienvenido {resultado[1]}")
        root_login.destroy()
        abrir_interfaz_principal(id_usuario)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    cursor.close()
    conexion.close()

# Funciones de la interfaz principal
def insertar_y_graficar(id_usuario, tipo_serie):
    try:
        num_terminos = int(entry_terminos.get())
        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()

        if tipo_serie == "coseno":
            id_serie = 3
            funcion = math.cos
        elif tipo_serie == "tangente":
            id_serie = 2
            funcion = math.tan
        elif tipo_serie == "fibonacci":
            id_serie = 1
            funcion = fibonacci

        for n in range(num_terminos):
            if tipo_serie == "fibonacci":
                valor_serie = funcion(n)
            else:
                valor_serie = funcion(n)

            error = random.uniform(-0.5, 0.5)
            ruido = valor_serie + error

            sql = """
                INSERT INTO registro (valorSerie, ruido, error, serieTrigonometrica_idSerie, usuario_idUsuario) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (valor_serie, ruido, error, id_serie, id_usuario))

        conexion.commit()
        messagebox.showinfo("Éxito", "Valores insertados correctamente.")
        cursor.close()
        conexion.close()

        graficar_datos(id_usuario, id_serie, tipo_serie)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def graficar_datos(id_usuario, id_serie, tipo_serie):
    try:
        for widget in frame_canvas.winfo_children():
            widget.destroy()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()

        sql = "SELECT n, valorSerie, ruido, error FROM registro WHERE usuario_idUsuario = %s AND serieTrigonometrica_idSerie = %s"
        cursor.execute(sql, (id_usuario, id_serie))
        resultados = cursor.fetchall()

        if resultados:
            n = [fila[0] for fila in resultados]
            valor_serie = [fila[1] for fila in resultados]
            ruido = [fila[2] for fila in resultados]
            error = [fila[3] for fila in resultados]

            fig, ax = plt.subplots(figsize=(8, 6))

            ax.plot(n, valor_serie, label="Valor puro", linestyle='-', color='blue', marker='x')
            ax.plot(n, ruido, label="Valor con ruido", marker='o')
            ax.plot(n, error, label="Error", linestyle='--', color='red')

            ax.set_title(f"Serie de {tipo_serie.capitalize()}")
            ax.set_xlabel("ID (n)")
            ax.set_ylabel("Valores")
            ax.legend()
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        else:
            messagebox.showinfo("Información", "No se encontraron datos para graficar.")

        cursor.close()
        conexion.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def abrir_nueva_interfaz():
    try:
        # Aquí llamamos a la función del dashboard que se encuentra en dash_compu.py
        dash_compu.crear_interfaz()  # Reemplaza 'crear_interfaz' por el nombre de la función que inicia tu dashboard
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir el dashboard: {str(e)}")
        

# Funciones para obtener datos
def obtener_datos_nserie():
    conexion = conectar()
    cursor = conexion.cursor()
    
    query = """
    SELECT st.tipoSerie, COUNT(r.n) as cuenta_registros
    FROM registro r
    JOIN serieTrigonometrica st ON r.serieTrigonometrica_idSerie = st.idSerie
    GROUP BY st.tipoSerie
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return resultados

def obtener_datos_usuarios():
    conexion = conectar()
    cursor = conexion.cursor()
    
    query = """
    SELECT u.nombreUsuario, COUNT(r.n) as cuenta_registros
    FROM registro r
    JOIN usuario u ON r.usuario_idUsuario = u.idUsuario
    GROUP BY u.nombreUsuario
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return resultados

def obtener_datos_ruido_promedio_por_usuario():
    conexion = conectar()
    cursor = conexion.cursor()
    
    query = """
    SELECT u.nombreUsuario, AVG(r.ruido) as promedio_ruido
    FROM registro r
    JOIN usuario u ON r.usuario_idUsuario = u.idUsuario
    GROUP BY u.nombreUsuario
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return resultados

def obtener_datos_ruido_vs_error():
    conexion = conectar()
    cursor = conexion.cursor()
    
    query = """
    SELECT r.ruido, r.error
    FROM registro r
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return resultados

def obtener_datos_por_rangos_ruido():
    conexion = conectar()
    cursor = conexion.cursor()
    
    query = """
    SELECT
        CASE
            WHEN ruido BETWEEN 0 AND 20 THEN '0-20'
            WHEN ruido BETWEEN 21 AND 40 THEN '21-40'
            WHEN ruido BETWEEN 41 AND 60 THEN '41-60'
            WHEN ruido BETWEEN 61 AND 80 THEN '61-80'
            ELSE '81+'
        END as rango_ruido,
        COUNT(*) as cuenta
    FROM registro
    GROUP BY rango_ruido
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return resultados

# Funciones para crear figuras
def crear_figura_barras(tipos, cuentas, xlabel, ylabel, title, colores=None):
    # Hacemos las figuras más pequeñas
    fig, ax = plt.subplots(figsize=(4, 3))  
    ax.bar(tipos, cuentas, color=colores if colores else '#4682B4')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def crear_figura_torta(tipos, cuentas, title):
    # Reducimos el tamaño de la figura
    fig, ax = plt.subplots(figsize=(4, 3))  
    porcentajes = [(count / sum(cuentas)) * 100 for count in cuentas]
    ax.pie(porcentajes, labels=tipos, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title(title)
    return fig

def crear_figura_scatter(x, y, xlabel, ylabel, title):
    # Reducimos el tamaño de la figura
    fig, ax = plt.subplots(figsize=(4, 3))  
    ax.scatter(x, y, color='#4682B4')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    return fig

# Función principal para crear la interfaz
def crear_interfaz():
    root = tk.Tk()
    root.title("DASHBOARD")  # Agregamos el título de la ventana

    # Habilitar botones de cerrar, minimizar y maximizar
    root.resizable(True, True)

    # Obtener y crear todas las figuras
    # Gráficos por tipo de serie
    datos_serie = obtener_datos_nserie()
    tipos_serie = [row[0] for row in datos_serie]
    cuenta_registros_serie = [row[1] for row in datos_serie]
    fig1 = crear_figura_barras(
        tipos=tipos_serie,
        cuentas=cuenta_registros_serie,
        xlabel='Tipo de Serie Trigonométrica',
        ylabel='Número de Registros',
        title='Número de Registros por Tipo de Serie Trigonométrica',
        colores=['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#9370DB', '#FF69B4', '#8A2BE2', '#A52A2A']
    )
    fig2 = crear_figura_torta(
        tipos=tipos_serie,
        cuentas=cuenta_registros_serie,
        title='Porcentaje de Registros por Tipo de Serie Trigonométrica'
    )

    # Gráficos por usuario
    datos_usuarios = obtener_datos_usuarios()
    nombres_usuarios = [row[0] for row in datos_usuarios]
    cuenta_registros_usuarios = [row[1] for row in datos_usuarios]
    fig3 = crear_figura_barras(
        tipos=nombres_usuarios,
        cuentas=cuenta_registros_usuarios,
        xlabel='Nombre de Usuario',
        ylabel='Número de Registros',
        title='Número de Registros por Usuario',
        colores=['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#9370DB', '#FF69B4', '#8A2BE2', '#A52A2A']
    )
    fig4 = crear_figura_torta(
        tipos=nombres_usuarios,
        cuentas=cuenta_registros_usuarios,
        title='Porcentaje de Registros por Usuario'
    )

    # Ruido promedio por usuario
    datos_ruido_promedio = obtener_datos_ruido_promedio_por_usuario()
    nombres_ruido = [row[0] for row in datos_ruido_promedio]
    promedio_ruido = [row[1] for row in datos_ruido_promedio]
    fig5 = crear_figura_barras(
        tipos=nombres_ruido,
        cuentas=promedio_ruido,
        xlabel='Nombre de Usuario',
        ylabel='Ruido Promedio',
        title='Ruido Promedio por Usuario',
        colores=['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#9370DB', '#FF69B4', '#8A2BE2', '#A52A2A']
    )

    # Relación Ruido vs Error
    datos_ruido_vs_error = obtener_datos_ruido_vs_error()
    ruido = [row[0] for row in datos_ruido_vs_error]
    error = [row[1] for row in datos_ruido_vs_error]
    fig6 = crear_figura_scatter(
        x=ruido,
        y=error,
        xlabel='Ruido',
        ylabel='Error',
        title='Relación entre Ruido y Error'
    )

    # Lista de figuras
    figuras = [fig1, fig2, fig3, fig4, fig5, fig6]

    # Crear un frame contenedor con grid para las figuras
    frame_graficos = ttk.Frame(root)
    frame_graficos.pack(expand=False, fill=tk.BOTH)

    # Colocar cada gráfica en una cuadrícula de 3 columnas y 2 filas
    for i, fig in enumerate(figuras):
        row = i // 3  # Determina la fila
        col = i % 3   # Determina la columna
        canvas_fig = FigureCanvasTkAgg(fig, master=frame_graficos)
        canvas_fig.draw()
        widget = canvas_fig.get_tk_widget()
        widget.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

    root.mainloop()

def abrir_interfaz_principal(id_usuario):
    global entry_terminos, frame_canvas
    root_principal = Tk()
    root_principal.title("Serie Trigonométrica")
    root_principal.geometry("800x600")

    frame_superior = Frame(root_principal)
    frame_superior.pack(side=TOP, fill=X, padx=20, pady=10)

    Label(frame_superior, text=f"Usuario ID: {id_usuario}", font=("Arial", 12)).pack(pady=10)

    Label(frame_superior, text="Número de términos:").pack(pady=5)
    entry_terminos = Entry(frame_superior)
    entry_terminos.pack(pady=5)

    opciones = ["coseno", "tangente", "fibonacci"]
    seleccion_serie = StringVar(root_principal)
    seleccion_serie.set(opciones[0])
    menu_serie = OptionMenu(frame_superior, seleccion_serie, *opciones)
    menu_serie.pack(pady=5)

    btn_insertar_y_graficar = Button(frame_superior, text="Insertar y Graficar", command=lambda: insertar_y_graficar(id_usuario, seleccion_serie.get()))
    btn_insertar_y_graficar.pack(pady=5)

    # Nuevo botón para redirigir a otra interfaz
    btn_redirigir = Button(frame_superior, text="Ir a otra interfaz", command=crear_interfaz)
    btn_redirigir.pack(pady=5)

    frame_inferior = Frame(root_principal)
    frame_inferior.pack(side=BOTTOM, fill=BOTH, expand=True)

    frame_canvas = Frame(frame_inferior)
    frame_canvas.pack(pady=20, fill=BOTH, expand=True)

    root_principal.mainloop()

# Interfaz de login (ajustada para dispositivos móviles)
root_login = Tk()
root_login.title("Inicio de Sesión")
root_login.geometry("1280x1280")  # Tamaño ajustado para móviles
root_login.config(bg="#2C3E50")

frame_login = Frame(root_login, bg="#34495E", bd=5)
frame_login.place(relx=0.5, rely=0.5, anchor=CENTER, width=900, height=900)  # Ajustado el tamaño

Label(frame_login, text="Inicio de Sesión", font=("Helvetica", 16, "bold"), fg="white", bg="#34495E").pack(pady=10)

Label(frame_login, text="Usuario", font=("Helvetica", 12), fg="white", bg="#34495E").pack(pady=5)
entry_usuario = Entry(frame_login, font=("Helvetica", 12), bd=3, relief=RIDGE)
entry_usuario.pack(pady=5, fill=X, padx=20)

Label(frame_login, text="Contraseña", font=("Helvetica", 12), fg="white", bg="#34495E").pack(pady=5)
entry_contrasena = Entry(frame_login, font=("Helvetica", 12), show="*", bd=3, relief=RIDGE)
entry_contrasena.pack(pady=5, fill=X, padx=20)

btn_login = Button(frame_login, text="Iniciar Sesión", font=("Helvetica", 12), bg="#1ABC9C", fg="white", relief=FLAT, command=verificar_login)
btn_login.pack(pady=12, fill=X, padx=25)

root_login.mainloop()