import os
import pandas as pd


# ============================================================
# RUTAS
# ============================================================

ruta_p1 = r'/workspaces/Storage/noticias/piura/parquet'
ruta_l1 = r'/workspaces/Storage/noticias/lambayeque/parquet'

ruta_output = r'/workspaces/Storage/noticias'


# ============================================================
# LEER TODOS LOS PARQUET DE UNA CARPETA
# ============================================================

def leer_parquets(carpeta):

    dataframes = []

    archivos = sorted(
        [
            archivo
            for archivo in os.listdir(carpeta)
            if archivo.lower().endswith(".parquet")
        ]
    )

    print()
    print("=" * 60)
    print(f"CARPETA: {carpeta}")
    print("=" * 60)

    print(
        f"Parquets encontrados: {len(archivos)}"
    )

    for archivo in archivos:

        ruta_archivo = os.path.join(
            carpeta,
            archivo
        )

        print(
            f"Leyendo: {ruta_archivo}"
        )

        df = pd.read_parquet(
            ruta_archivo
        )

        # ----------------------------------------------------
        # GUARDAR NOMBRE DEL ARCHIVO ORIGINAL
        # ----------------------------------------------------

        df["ARCHIVO_ORIGEN"] = archivo

        dataframes.append(df)

        print(
            f"  ✓ {len(df)} filas"
        )

    if not dataframes:

        return pd.DataFrame()

    return pd.concat(
        dataframes,
        ignore_index=True
    )


# ============================================================
# NORMALIZAR TIPOS
# ============================================================

def normalizar_dataframe(df):

    if df.empty:
        return df

    df = df.copy()

    # --------------------------------------------------------
    # NORMALIZAR DIA
    # --------------------------------------------------------

    if "DIA" in df.columns:

        df["DIA"] = pd.to_datetime(
            df["DIA"],
            errors="coerce"
        )

    # --------------------------------------------------------
    # NORMALIZAR COLUMNAS DE TEXTO
    # --------------------------------------------------------

    columnas_texto = [
        "DIARIO",
        "TITULAR",
        "DESCRIPCIÓN",
        "LINKS",
        "ARCHIVO_ORIGEN"
    ]

    for columna in columnas_texto:

        if columna in df.columns:

            df[columna] = (
                df[columna]
                .astype("string")
            )

    return df


# ============================================================
# PIURA
# ============================================================

df_p = leer_parquets(
    ruta_p1
)

df_p = normalizar_dataframe(
    df_p
)


# ============================================================
# LAMBAYEQUE
# ============================================================

df_l = leer_parquets(
    ruta_l1
)

df_l = normalizar_dataframe(
    df_l
)


# ============================================================
# CREAR CARPETA DE SALIDA
# ============================================================

os.makedirs(
    ruta_output,
    exist_ok=True
)


# ============================================================
# GUARDAR PIURA
# ============================================================

ruta_salida_piura = os.path.join(
    ruta_output,
    "noticias_piura.parquet"
)

print()
print("=" * 60)
print("GUARDANDO PIURA")
print("=" * 60)

df_p.to_parquet(
    ruta_salida_piura,
    index=False
)

print(
    f"✓ Guardado: {ruta_salida_piura}"
)

print(
    f"✓ Filas: {len(df_p)}"
)


# ============================================================
# GUARDAR LAMBAYEQUE
# ============================================================

ruta_salida_lambayeque = os.path.join(
    ruta_output,
    "noticias_lambayeque.parquet"
)

print()
print("=" * 60)
print("GUARDANDO LAMBAYEQUE")
print("=" * 60)

df_l.to_parquet(
    ruta_salida_lambayeque,
    index=False
)

print(
    f"✓ Guardado: {ruta_salida_lambayeque}"
)

print(
    f"✓ Filas: {len(df_l)}"
)


# ============================================================
# RESUMEN
# ============================================================

print()
print("=" * 60)
print("PROCESO TERMINADO CORRECTAMENTE")
print("=" * 60)

print(
    f"Piura:       {len(df_p)} filas"
)

print(
    f"Lambayeque:  {len(df_l)} filas"
)

print()
print(
    "Archivos creados:"
)

print(
    ruta_salida_piura
)

print(
    ruta_salida_lambayeque
)
