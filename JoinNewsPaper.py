import os
import pandas as pd


# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RUTA_NOTICIAS = os.path.join(
    BASE_DIR,
    "noticias"
)

RUTA_PIURA = os.path.join(
    RUTA_NOTICIAS,
    "piura",
    "parquet"
)

RUTA_LAMBAYEQUE = os.path.join(
    RUTA_NOTICIAS,
    "lambayeque",
    "parquet"
)


# ============================================================
# ARCHIVOS DE SALIDA
# ============================================================

RUTA_SALIDA_PIURA = os.path.join(
    RUTA_NOTICIAS,
    "noticias_piura.parquet"
)

RUTA_SALIDA_LAMBAYEQUE = os.path.join(
    RUTA_NOTICIAS,
    "noticias_lambayeque.parquet"
)


# ============================================================
# FUNCIÓN PARA LEER TODOS LOS PARQUETS
# ============================================================

def leer_parquets(carpeta, region):

    print()
    print("=" * 60)
    print(f"LEYENDO PARQUETS - {region.upper()}")
    print("=" * 60)

    # --------------------------------------------------------
    # Verificar carpeta
    # --------------------------------------------------------

    if not os.path.exists(carpeta):

        print(
            f"⚠ No existe la carpeta:"
        )

        print(carpeta)

        return pd.DataFrame()


    # --------------------------------------------------------
    # Buscar archivos Parquet
    # --------------------------------------------------------

    archivos = []

    for archivo in os.listdir(carpeta):

        if not archivo.lower().endswith(".parquet"):
            continue

        # No leer el archivo consolidado
        if archivo == f"noticias_{region}.parquet":
            continue

        archivos.append(archivo)


    archivos.sort()


    print(
        f"Parquets encontrados: "
        f"{len(archivos)}"
    )


    # --------------------------------------------------------
    # Si no hay archivos
    # --------------------------------------------------------

    if not archivos:

        print(
            "⚠ No hay archivos Parquet."
        )

        return pd.DataFrame()


    # --------------------------------------------------------
    # Leer archivos
    # --------------------------------------------------------

    dataframes = []

    for archivo in archivos:

        ruta_archivo = os.path.join(
            carpeta,
            archivo
        )

        print()
        print(
            f"Leyendo: {ruta_archivo}"
        )

        try:

            df = pd.read_parquet(
                ruta_archivo
            )

            # -----------------------------------------------
            # Agregar nombre del archivo original
            # -----------------------------------------------

            df["ARCHIVO_ORIGEN"] = archivo

            dataframes.append(df)

            print(
                f"  ✓ {len(df)} filas"
            )

        except Exception as error:

            print(
                f"  ✗ ERROR leyendo {archivo}"
            )

            print(error)


    # --------------------------------------------------------
    # Verificar resultados
    # --------------------------------------------------------

    if not dataframes:

        print()
        print(
            "⚠ No se pudo leer ningún Parquet."
        )

        return pd.DataFrame()


    # --------------------------------------------------------
    # Unir todos los DataFrames
    # --------------------------------------------------------

    print()
    print(
        "Uniendo archivos..."
    )

    df_final = pd.concat(
        dataframes,
        ignore_index=True
    )


    # --------------------------------------------------------
    # Normalizar columna DIA
    # --------------------------------------------------------

    if "DIA" in df_final.columns:

        print(
            "Normalizando columna DIA..."
        )

        df_final["DIA"] = pd.to_datetime(
            df_final["DIA"],
            errors="coerce"
        )


    # --------------------------------------------------------
    # Ordenar por fecha
    # --------------------------------------------------------

    if "DIA" in df_final.columns:

        df_final = df_final.sort_values(
            by="DIA",
            ascending=False,
            na_position="last"
        ).reset_index(
            drop=True
        )


    # --------------------------------------------------------
    # Mostrar resumen
    # --------------------------------------------------------

    print()
    print(
        f"TOTAL DE FILAS: "
        f"{len(df_final)}"
    )

    print(
        f"TOTAL DE COLUMNAS: "
        f"{len(df_final.columns)}"
    )

    print()
    print(
        "Columnas:"
    )

    for columna in df_final.columns:

        print(
            f"  - {columna}"
        )


    return df_final


# ============================================================
# LEER PIURA
# ============================================================

df_p = leer_parquets(
    RUTA_PIURA,
    "piura"
)


# ============================================================
# LEER LAMBAYEQUE
# ============================================================

df_l = leer_parquets(
    RUTA_LAMBAYEQUE,
    "lambayeque"
)


# ============================================================
# GUARDAR PIURA
# ============================================================

print()
print("=" * 60)
print("GUARDANDO PIURA")
print("=" * 60)

if not df_p.empty:

    df_p.to_parquet(
        RUTA_SALIDA_PIURA,
        index=False
    )

    print(
        "✓ Piura guardado correctamente:"
    )

    print(
        RUTA_SALIDA_PIURA
    )

    print(
        f"Filas: {len(df_p)}"
    )

else:

    print(
        "⚠ No hay datos de Piura para guardar."
    )


# ============================================================
# GUARDAR LAMBAYEQUE
# ============================================================

print()
print("=" * 60)
print("GUARDANDO LAMBAYEQUE")
print("=" * 60)

if not df_l.empty:

    df_l.to_parquet(
        RUTA_SALIDA_LAMBAYEQUE,
        index=False
    )

    print(
        "✓ Lambayeque guardado correctamente:"
    )

    print(
        RUTA_SALIDA_LAMBAYEQUE
    )

    print(
        f"Filas: {len(df_l)}"
    )

else:

    print(
        "⚠ No hay datos de Lambayeque para guardar."
    )


# ============================================================
# RESUMEN FINAL
# ============================================================

print()
print("=" * 60)
print("PROCESO TERMINADO")
print("=" * 60)

print()
print(
    f"Piura:       {len(df_p)} noticias"
)

print(
    f"Lambayeque:  {len(df_l)} noticias"
)

print()
print(
    "Archivos consolidados:"
)

print(
    RUTA_SALIDA_PIURA
)

print(
    RUTA_SALIDA_LAMBAYEQUE
)

print()
print("=" * 60)
