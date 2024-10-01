import mysql.connector
import math
import random
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from dashboards import ejecutar_todo
# Conectar a la base de datos
def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia por tu usuario
        password="",  # Cambia por tu contraseña
        database="sonometro"  # Nombre de la base de datos
    )
    return conexion

# Insertar valores en la base de datos y graficar
def insertar_y_graficar(id_usuario, tipo_serie):
    try:
        num_terminos = int(entry_terminos.get())
        conexion = conectar()
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
                valor_serie = funcion(n)  # Valor puro de la función trigonométrica

            error = random.uniform(-0.5, 0.5)  # Generar error aleatorio
            ruido = valor_serie + error  # Valor con ruido (valor + error)

            # Insertar en la tabla registro
            sql = """
                INSERT INTO registro (valorSerie, ruido, error, serieTrigonometrica_idSerie, usuario_idUsuario) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (valor_serie, ruido, error, id_serie, id_usuario))

        conexion.commit()
        messagebox.showinfo("Éxito", "Valores insertados correctamente.")
        cursor.close()
        conexion.close()

        # Graficar los valores
        graficar_datos(id_usuario, id_serie, tipo_serie)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Definir la serie de Fibonacci
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Graficar los datos
def graficar_datos(id_usuario, id_serie, tipo_serie):
    try:
        # Limpiar el gráfico sin eliminar otros widgets
        for widget in frame_canvas.winfo_children():
            widget.forget()

        conexion = conectar()
        cursor = conexion.cursor()

        # Consultar los datos insertados para graficar
        sql = "SELECT n, valorSerie, ruido, error FROM registro WHERE usuario_idUsuario = %s AND serieTrigonometrica_idSerie = %s"
        cursor.execute(sql, (id_usuario, id_serie))
        resultados = cursor.fetchall()

        if resultados:
            n = []
            valor_serie = []
            ruido = []
            error = []

            for fila in resultados:
                n_valor = fila[0]
                valor_serie_valor = fila[1]
                ruido_valor = fila[2]
                error_valor = fila[3]

                n.append(n_valor)  # ID (n)
                valor_serie.append(valor_serie_valor)  # Valores puros
                ruido.append(ruido_valor)  # Valores con ruido
                error.append(error_valor)  # Error

            # Crear el gráfico
            fig, ax = plt.subplots(figsize=(8, 6))

            # Graficar
            ax.plot(n, valor_serie, label="Valor puro", linestyle='-', color='blue', marker='x')
            ax.plot(n, ruido, label="Valor con ruido", marker='o')
            ax.plot(n, error, label="Error", linestyle='--', color='red')

            ax.set_title(f"Serie de {tipo_serie.capitalize()}")
            ax.set_xlabel("ID (n)")
            ax.set_ylabel("Valores")
            ax.legend()
            ax.grid(True)

            # Mostrar gráfico en Tkinter
            canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
            canvas.draw()
            canvas.get_tk_widget().pack()

        else:
            messagebox.showinfo("Información", "No se encontraron datos para graficar.")

        cursor.close()
        conexion.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Función que se llamará cuando se presione el botón
def abrir_nueva_interfaz():
    ejecutar_todo()
    
# Abrir la interfaz principal
def abrir_interfaz_principal(id_usuario):
    global entry_terminos, frame_canvas
    root = Tk()
    root.title("Serie Trigonométrica")
    root.geometry("800x600")

    # Frame superior para los botones y entradas
    frame_superior = Frame(root)
    frame_superior.pack(side=TOP, fill=X, padx=20, pady=10)

    Label(frame_superior, text=f"Usuario ID: {id_usuario}", font=("Arial", 12)).pack(pady=10)

    Label(frame_superior, text="Número de términos:").pack(pady=5)
    entry_terminos = Entry(frame_superior)
    entry_terminos.pack(pady=5)

    # Menú desplegable para seleccionar la serie
    opciones = ["coseno", "tangente", "fibonacci"]
    seleccion_serie = StringVar(root)
    seleccion_serie.set(opciones[0])  # Valor por defecto
    menu_serie = OptionMenu(frame_superior, seleccion_serie, *opciones)
    menu_serie.pack(pady=5)

    # Botón para insertar valores y graficar
    btn_insertar_y_graficar = Button(frame_superior, text="Insertar y Graficar", command=lambda: insertar_y_graficar(id_usuario, seleccion_serie.get()))
    btn_insertar_y_graficar.pack(pady=5)
    # Nuevo botón para redirigir a otra interfaz
    btn_redirigir = Button(frame_superior, text="Ir a otra interfaz", command=abrir_nueva_interfaz)
    btn_redirigir.pack(pady=5)

    # Frame inferior para el gráfico
    frame_inferior = Frame(root)
    frame_inferior.pack(side=BOTTOM, fill=BOTH, expand=True)

    # Frame para el gráfico dentro del frame inferior
    frame_canvas = Frame(frame_inferior)
    frame_canvas.pack(pady=20, fill=BOTH, expand=True)

    root.mainloop()

