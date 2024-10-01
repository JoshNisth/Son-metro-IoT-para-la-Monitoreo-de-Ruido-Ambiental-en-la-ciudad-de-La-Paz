import mysql.connector
import matplotlib.pyplot as plt

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        #port="3307",
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

# Nuevas gráficas adicionales
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

def crear_grafico_barras_ruido_promedio_por_usuario(datos):
    nombres_usuarios = [row[0] for row in datos]
    promedio_ruido = [row[1] for row in datos]
    
    colores = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#9370DB', '#FF69B4', '#8A2BE2', '#A52A2A']
    
    plt.figure(figsize=(12, 6))
    plt.bar(nombres_usuarios, promedio_ruido, color=colores[:len(nombres_usuarios)])
    plt.xlabel('Nombre de Usuario')
    plt.ylabel('Ruido Promedio')
    plt.title('Ruido Promedio por Usuario')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

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

def crear_grafico_ruido_vs_error(datos):
    ruido = [row[0] for row in datos]
    error = [row[1] for row in datos]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(ruido, error, color='#4682B4')
    plt.xlabel('Ruido')
    plt.ylabel('Error')
    plt.title('Relación entre Ruido y Error')
    plt.tight_layout()
    plt.show()

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

def crear_grafico_barras_rango_ruido(datos):
    rangos_ruido = [row[0] for row in datos]
    cuenta_registros = [row[1] for row in datos]
    
    colores = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#9370DB']
    
    plt.figure(figsize=(10, 6))
    plt.bar(rangos_ruido, cuenta_registros, color=colores[:len(rangos_ruido)])
    plt.xlabel('Rango de Ruido')
    plt.ylabel('Número de Registros')
    plt.title('Número de Registros por Rango de Ruido')
    plt.tight_layout()
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
    
    # Nuevas gráficas
    datos_ruido_promedio = obtener_datos_ruido_promedio_por_usuario()
    crear_grafico_barras_ruido_promedio_por_usuario(datos_ruido_promedio)
    
    datos_ruido_vs_error = obtener_datos_ruido_vs_error()
    crear_grafico_ruido_vs_error(datos_ruido_vs_error)
    
    datos_rangos_ruido = obtener_datos_por_rangos_ruido()
    crear_grafico_barras_rango_ruido(datos_rangos_ruido)

