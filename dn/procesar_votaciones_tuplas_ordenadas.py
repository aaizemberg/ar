import pandas as pd
import glob
import os
import re

# --- Configuración ---
ruta_carpeta_csv = 'votaciones/'
archivo_salida = 'votaciones_consolidadas_2025.tsv'

# --- Función auxiliar para extraer números de <Periodo>-<Reunion>-<Acta> ---
def extraer_claves(nombre_archivo):
    """
    Dado un archivo '142-22-3.csv', devuelve una tupla (142, 22, 3)
    que se puede usar para ordenar correctamente.
    """
    base = os.path.splitext(os.path.basename(nombre_archivo))[0]
    partes = re.findall(r'\d+', base)
    if len(partes) == 3:
        return tuple(map(int, partes))
    else:
        # Si no cumple el formato esperado, lo mandamos al final
        return (9999, 9999, 9999)

try:
    # --- 1. Buscar archivos y ordenarlos por período, reunión y acta ---
    archivos_csv = glob.glob(os.path.join(ruta_carpeta_csv, '*.csv'))
    archivos_csv.sort(key=extraer_claves)

    if not archivos_csv:
        print(f"Error: No se encontraron archivos .csv en '{ruta_carpeta_csv}'.")
    else:
        print(f"Se encontraron {len(archivos_csv)} archivos.")
        print("Ejemplo de orden final:", [os.path.basename(a) for a in archivos_csv[:10]])

        columnas_clave = ['DIPUTADO', 'BLOQUE', 'PROVINCIA']
        df_final = None

        # --- 2. Procesar cada archivo ---
        for i, archivo in enumerate(archivos_csv):
            base = os.path.splitext(os.path.basename(archivo))[0]
            print(f"Procesando ({i+1}/{len(archivos_csv)}): {base}")
            df_temp = pd.read_csv(archivo)

            # Limpieza uniforme de texto
            for col in columnas_clave:
                df_temp[col] = (
                    df_temp[col]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    .str.replace('-', ' ', regex=False)
                )

            # Renombrar columna de voto
            if '¿CÓMO VOTÓ?' not in df_temp.columns:
                raise ValueError(f"Archivo '{archivo}' no contiene la columna '¿CÓMO VOTÓ?'")
            df_temp.rename(columns={'¿CÓMO VOTÓ?': base}, inplace=True)

            # Merge
            if df_final is None:
                df_final = df_temp
            else:
                df_final = pd.merge(df_final, df_temp, on=columnas_clave, how='outer')

        # --- 3. Orden final de columnas ---
        # Claves al inicio, votos ordenados por período, reunión y acta
        columnas_votos = sorted(
            [col for col in df_final.columns if col not in columnas_clave],
            key=lambda x: tuple(map(int, re.findall(r'\d+', x)))
        )
        df_final = df_final[columnas_clave + columnas_votos]

        # --- 4. Guardar resultado ---
        df_final.to_csv(archivo_salida, sep='\t', index=False)

        print("\n✅ ¡Proceso completado con éxito!")
        print(f"Archivo generado: {archivo_salida}")
        print(f"Filas: {len(df_final):,} | Columnas: {len(df_final.columns):,}")

except Exception as e:
    print(f"\n❌ Ocurrió un error inesperado: {e}")
