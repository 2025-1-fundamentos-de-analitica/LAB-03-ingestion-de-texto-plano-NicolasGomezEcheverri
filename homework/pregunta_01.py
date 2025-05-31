import pandas as pd
import re

def pregunta_01():
    """
    Construye y retorna un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requerimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    
    # Leer el archivo
    with open('files/input/clusters_report.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Dividir el contenido en líneas
    lines = content.strip().split('\n')
    
    # Encontrar la línea de separación para identificar donde empiezan los datos
    separator_line_idx = None
    for i, line in enumerate(lines):
        if '-----' in line:
            separator_line_idx = i
            break
    
    # Extraer los datos después de la línea separadora
    data_lines = lines[separator_line_idx + 1:]
    
    # Filtrar líneas vacías
    data_lines = [line for line in data_lines if line.strip()]
    
    # Procesar cada línea de datos
    data = []
    current_cluster = None
    current_cantidad = None
    current_porcentaje = None
    current_keywords = ""
    
    for line in data_lines:
        line = line.strip()
        if not line:
            continue
            
        # Detectar si la línea comienza con un número (nuevo cluster)
        match = re.match(r'^\s*(\d+)\s+(\d+)\s+([\d,]+\s*%)\s+(.+)$', line)
        
        if match:
            # Si ya teníamos un cluster anterior, guardarlo
            if current_cluster is not None:
                # Limpiar y formatear las palabras clave
                keywords_clean = re.sub(r'\s+', ' ', current_keywords.strip())
                keywords_clean = re.sub(r'\s*,\s*', ', ', keywords_clean)
                # Eliminar punto final si existe
                keywords_clean = keywords_clean.rstrip('.')
                
                data.append({
                    'cluster': current_cluster,
                    'cantidad_de_palabras_clave': current_cantidad,
                    'porcentaje_de_palabras_clave': current_porcentaje,
                    'principales_palabras_clave': keywords_clean
                })
            
            # Nuevo cluster
            current_cluster = int(match.group(1))
            current_cantidad = int(match.group(2))
            # Extraer el valor numérico del porcentaje (sin el símbolo %)
            porcentaje_str = match.group(3).replace(',', '.').replace('%', '').strip()
            current_porcentaje = float(porcentaje_str)
            current_keywords = match.group(4)
            
        else:
            # Línea de continuación de palabras clave
            current_keywords += " " + line
    
    # No olvidar el último cluster
    if current_cluster is not None:
        keywords_clean = re.sub(r'\s+', ' ', current_keywords.strip())
        keywords_clean = re.sub(r'\s*,\s*', ', ', keywords_clean)
        # Eliminar punto final si existe
        keywords_clean = keywords_clean.rstrip('.')
        
        data.append({
            'cluster': current_cluster,
            'cantidad_de_palabras_clave': current_cantidad,
            'porcentaje_de_palabras_clave': current_porcentaje,
            'principales_palabras_clave': keywords_clean
        })
    
    # Crear el DataFrame
    df = pd.DataFrame(data)
    
    return df

# Ejemplo de uso
if __name__ == "__main__":
    df = pregunta_01()
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"\nColumnas: {list(df.columns)}")
    print(f"\nTipos de datos:\n{df.dtypes}")