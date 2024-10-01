import mysql.connector
from tkinter import *
from tkinter import messagebox
from main_interface import abrir_interfaz_principal

# Conectar a la base de datos
def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia por tu usuario
        password="",  # Cambia por tu contraseña
        database="sonometro"
    )
    return conexion

# Verificar credenciales
def verificar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    conexion = conectar()
    cursor = conexion.cursor()

    # Consulta SQL para verificar usuario y contraseña
    query = "SELECT idUsuario, nombreUsuario FROM usuario WHERE nombreUsuario = %s AND password = %s"
    cursor.execute(query, (usuario, contrasena))
    resultado = cursor.fetchone()

    if resultado:
        id_usuario = resultado[0]
        messagebox.showinfo("Login exitoso", f"Bienvenido {resultado[1]}")
        root.destroy()  # Cierra la ventana de login
        abrir_interfaz_principal(id_usuario)  # Abre la siguiente interfaz
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    cursor.close()
    conexion.close()

# Crear la ventana de login con un estilo mejorado
root = Tk()
root.title("Inicio de Sesión")
root.geometry("400x300")
root.config(bg="#2C3E50")

# Frame para centrar el contenido
frame_login = Frame(root, bg="#34495E", bd=5)
frame_login.place(relx=0.5, rely=0.5, anchor=CENTER, width=350, height=250)

# Título
Label(frame_login, text="Inicio de Sesión", font=("Helvetica", 18, "bold"), fg="white", bg="#34495E").pack(pady=10)

# Etiqueta y entrada para el nombre de usuario
Label(frame_login, text="Usuario", font=("Helvetica", 12), fg="white", bg="#34495E").pack(pady=5)
entry_usuario = Entry(frame_login, font=("Helvetica", 12), bd=3, relief=RIDGE)
entry_usuario.pack(pady=5, fill=X, padx=20)

# Etiqueta y entrada para la contraseña
Label(frame_login, text="Contraseña", font=("Helvetica", 12), fg="white", bg="#34495E").pack(pady=5)
entry_contrasena = Entry(frame_login, font=("Helvetica", 12), show="*", bd=3, relief=RIDGE)
entry_contrasena.pack(pady=5, fill=X, padx=20)

# Botón de login
btn_login = Button(frame_login, text="Iniciar Sesión", font=("Helvetica", 12), bg="#1ABC9C", fg="white", relief=FLAT, command=verificar_login)
btn_login.pack(pady=12, fill=X, padx=25)

root.mainloop()


