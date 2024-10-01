import mysql.connector
import matplotlib.pyplot as plt

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sonometro2"
    )
    return conexion

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

def crear_grafico_barras_nserie(datos):
    tipos_serie = [row[0] for row in datos]
    cuenta_registros = [row[1] for row in datos]
    
    colores = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#9370DB', '#FF69B4', '#8A2BE2', '#A52A2A']
    
    plt.figure(figsize=(10, 6))
    plt.bar(tipos_serie, cuenta_registros, color=colores[:len(tipos_serie)])
    plt.xlabel('Tipo de Serie Trigonométrica')
    plt.ylabel('Número de Registros')
    plt.title('Número de Registros por Tipo de Serie Trigonométrica')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def crear_grafico_torta_nserie(datos):
    tipos_serie = [row[0] for row in datos]
    cuenta_registros = [row[1] for row in datos]
    total_registros = sum(cuenta_registros)
    
    porcentajes = [(count / total_registros) * 100 for count in cuenta_registros]
    
    plt.figure(figsize=(10, 8))
    plt.pie(porcentajes, labels=tipos_serie, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Porcentaje de Registros por Tipo de Serie Trigonométrica')
    plt.show()

# Nuevas funciones para usuarios
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

def crear_grafico_barras_usuarios(datos):
    nombres_usuarios = [row[0] for row in datos]
    cuenta_registros = [row[1] for row in datos]
    
    colores = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#9370DB', '#FF69B4', '#8A2BE2', '#A52A2A']
    
    plt.figure(figsize=(12, 6))
    plt.bar(nombres_usuarios, cuenta_registros, color=colores[:len(nombres_usuarios)])
    plt.xlabel('Nombre de Usuario')
    plt.ylabel('Número de Registros')
    plt.title('Número de Registros por Usuario')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def crear_grafico_torta_usuarios(datos):
    nombres_usuarios = [row[0] for row in datos]
    cuenta_registros = [row[1] for row in datos]
    total_registros = sum(cuenta_registros)
    
    porcentajes = [(count / total_registros) * 100 for count in cuenta_registros]
    
    plt.figure(figsize=(10, 8))
    plt.pie(porcentajes, labels=nombres_usuarios, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Porcentaje de Registros por Usuario')
    plt.show()

if __name__ == "__main__":
    # Gráficos por tipo de serie
    datos_serie = obtener_datos_nserie()
    crear_grafico_barras_nserie(datos_serie)
    crear_grafico_torta_nserie(datos_serie)
    
    # Gráficos por usuario
    datos_usuarios = obtener_datos_usuarios()
    crear_grafico_barras_usuarios(datos_usuarios)
    crear_grafico_torta_usuarios(datos_usuarios)