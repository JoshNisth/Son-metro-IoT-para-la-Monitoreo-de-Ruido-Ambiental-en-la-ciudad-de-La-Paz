import mysql.connector
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def conectar():
    conexion = mysql.connector.connect(
        host="192.168.8.55",
        user="josh",
        password="",
        database="sonometro"
    )
    return conexion

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

if __name__ == "__main__":
    crear_interfaz()
