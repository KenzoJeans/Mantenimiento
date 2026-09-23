import streamlit as st
import datetime
from zoneinfo import ZoneInfo
import gspread
import pandas as pd
import os

st.set_page_config(page_title="Reporte de Mantenimiento - Kenzo Jeans", page_icon="🔧", layout="wide")

TZ_BOGOTA = ZoneInfo("America/Bogota")
PLACEHOLDER = "Seleccione..."
LOGO_PATH = "logo.png"

# Paleta de color de la app (tono cian, igual al de los botones)
COLOR_PRIMARIO = "#22D3EE"
COLOR_SECUNDARIO = "#0EA5B7"
COLOR_TERCIARIO = "#67E8F9"


def col_letter(n: int) -> str:
    letra = ""
    while n > 0:
        n, resto = divmod(n - 1, 26)
        letra = chr(65 + resto) + letra
    return letra


@st.cache_resource
def get_gsheet_client():
    creds_dict = dict(st.secrets["gcp_service_account"])
    return gspread.service_account_from_dict(creds_dict)


SPREADSHEET_ID = "1eyXRRNUGEMbWTdNW-hpFraoSCvn-A_LzscTwLrVfAvg"

HOJA_TINTORERIA = "Tintorería"
HOJA_TIENDAS = "Tiendas"
HOJA_PLANTA = "Planta"


def guardar_en_hoja(nombre_hoja: str, row_data: list):
    gc = get_gsheet_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.worksheet(nombre_hoja)

    col_a_values = worksheet.col_values(1)
    siguiente_fila = len(col_a_values) + 1
    ultima_col = col_letter(len(row_data))

    worksheet.update(
        f"A{siguiente_fila}:{ultima_col}{siguiente_fila}",
        [row_data],
        value_input_option="USER_ENTERED"
    )


def _leer_filas(nombre_hoja: str):
    gc = get_gsheet_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.worksheet(nombre_hoja)
    valores = worksheet.get_all_values()
    return valores[1:] if len(valores) > 1 else []


def _parsear_fecha(s):
    try:
        return datetime.datetime.strptime(s.strip(), "%d/%m/%Y %H:%M:%S")
    except Exception:
        return pd.NaT


def _parsear_costo(v):
    try:
        return float(str(v).replace(",", "").replace("$", "").strip() or 0)
    except Exception:
        return 0.0


@st.cache_data(ttl=120)
def cargar_datos_dashboard():
    registros = []

    for f in _leer_filas(HOJA_TINTORERIA):
        if len(f) < 18:
            continue
        registros.append({
            "area": "Tintorería", "marca_temporal": f[0], "tipo_mantenimiento": f[5],
            "tipo_maquina": f[4], "costo": f[11], "residuos": f[12], "responsable": f[17],
        })

    for f in _leer_filas(HOJA_TIENDAS):
        if len(f) < 13:
            continue
        registros.append({
            "area": "Tiendas", "marca_temporal": f[0], "tipo_mantenimiento": f[3],
            "tipo_maquina": "", "costo": 0, "residuos": f[7], "responsable": f[12],
        })

    for f in _leer_filas(HOJA_PLANTA):
        if len(f) < 17:
            continue
        registros.append({
            "area": "Planta/Confección", "marca_temporal": f[0], "tipo_mantenimiento": f[5],
            "tipo_maquina": f[4], "costo": f[10], "residuos": f[12], "responsable": f[15],
        })

    df = pd.DataFrame(registros)
    if df.empty:
        return df

    df["fecha"] = df["marca_temporal"].apply(_parsear_fecha)
    df["costo_num"] = df["costo"].apply(_parsear_costo)
    return df


# --- ENCABEZADO CON LOGO ---
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=110)
    else:
        st.write("")
with col_titulo:
    st.title("🔧 Reporte de Mantenimiento - Kenzo Jeans")
    st.caption("Completa todos los campos marcados y guarda el reporte antes de cambiar de área.")

st.markdown("---")

tab_registro, tab_dashboard = st.tabs(["📝 Registrar Reporte", "📊 Dashboard"])

# ============================================================
# PESTAÑA 1: REGISTRAR REPORTE  (sin st.form, para que los
# campos de repuestos/residuos reaccionen al instante)
# ============================================================
with tab_registro:

    mecanicos = [PLACEHOLDER, "Jonathan Borrego", "Cristobal Castellanos", "Felipe Cárdenas", "Jhon Jairo Gómez"]
    tipos_intervencion_conf = [
        PLACEHOLDER, "Ajuste mecánico", "Instalación del folder", "Ajuste de tensión",
        "Cambio de elementos", "Programación de máquina"
    ]
    tipos_mantenimiento_general = [PLACEHOLDER, "Preventivo", "Correctivo", "Predictivo"]
    tipos_mantenimiento_tiendas = [PLACEHOLDER, "Preventivo", "Correctivo", "Locativo"]
    tipos_mantenimiento_confeccion = [PLACEHOLDER, "Preventivo", "Correctivo", "Alistamiento", "Adecuación"]

    maquinas_confeccion = [PLACEHOLDER] + [
        "CADENETA", "FILETEADORA", "PLANA", "DOS AGUJAS", "COLLARIN PLANA", "COLLARIN CILINDRICA",
        "COLLARIN CODO", "EMPRETINADORA", "PRESILLADORA", "MAQUINA DE BOTAS", "MAQUINA DE J",
        "DIBUJADORA", "OJALADORA DE CAMISA", "OJALADORA DE LÁGRIMA", "PEGAR PASADORES", "HACER PASADORES",
        "RIBETEADORA", "FUSIONADORA", "VOLTEADORA DE PANTALÓN", "DOBLADILLADORA DE BOLSILLO", "CERRADORA",
        "CERRADORA DE CAMISA", "CERRADORA DE CODO", "CERRADORA DE PEDESTAL", "CORTADORA VERTICAL",
        "CORTADORA AUTOMÁTICA", "LÁSER", "BORDADORA", "TACHADORA", "PARCHADORA", "MULTIAGUJAS",
        "BOTONADORA", "REVISADORA DE TELAS", "MAQUINA FUSIONADORA"
    ]

    maquinas_tintoreria = [PLACEHOLDER] + [
        "LAVADORA", "SECADORA", "CENTÍFUGA", "LASER", "LAVADORA DE MUESTRAS",
        "SECADORA DE MUESTRAS", "CENTRÍFUGA DE MUESTRAS", "TERMOFIJADORA",
        "MOTORTOOL", "VARIBOOSTER", "PRENSA"
    ]

    elementos_tintoreria = [
        "CABLES", "MOTOR", "MULETILLAS", "RELÉS", "PULSADORES", "CONTACTORES", "TARJETAS",
        "PLC", "RESISTENCIAS", "CILINDROS", "VÁLVULAS", "ELECTROVÁLVULAS", "RODAMIENTOS",
        "EJES", "CHUMACERAS", "ENGRASES", "BOMBAS", "BOOSTER", "VÁLVULA MANUAL", "SERPENTINES",
        "PIÑONES", "TEMPORIZADOR", "POLEAS", "CORREA", "FUSIBLES", "AJUSTE DE BORNES", "RESORTES"
    ]

    tiendas_kenzo = [PLACEHOLDER] + [
        "SALITRE PLAZA", "RESTREPO 1", "FONTIBON", "QUIRIGUA", "TUNAL",
        "PLAZA D LAS AMERICAS 1(Mujer)", "CENTRO SUBA", "SANTA HELENITA", "KENNEDY",
        "CHAPINERO", "ESTRADA", "CENTRO 1", "RESTREPO 2", "OUTLET ZONA", "PORTAL 80",
        "UNICENTRO OCCIDENTE", "YOPAL", "TINTAL PLAZA", "IMPERIAL", "SANTAFE",
        "CENTRO MAYOR", "TITAN PLAZA", "DIVER PLAZA", "ZIPAQUIRA", "MERCURIO",
        "FACTORY", "MOSQUERA", "HAYUELOS", "PLAZA D LAS AMERICAS 2 (Hombre)",
        "FUNZA MICENTRO", "GIRARDOT", "IPIALES", "CALLE 13 ZONA", "POPAYAN",
        "PLAZA CENTRAL", "BOSA PIAMONTE CALLE", "TOBERIN", "VENTURA TERREROS",
        "GRAN PLAZA ENSUEÑO", "CAJICA", "TUNJA", "GRAN PLAZA BOSA", "PASEO VILLA DEL RIO",
        "NUESTRO BOGOTA", "ATREVETE FONTIBON", "ATREVETE SEVILLANA", "MADRID",
        "CARRERA 62", "OUTLET CENTER", "FUSAGASUGA", "ALTA VISTA", "OUTLET CARRERA 62",
        "RIO NEGRO - ANTIOQUIA", "OUTLET FLORESTA", "ESPINAL", "FUNZA CENTRO"
    ]

    if "form_version" not in st.session_state:
        st.session_state.form_version = 0
    v = st.session_state.form_version  # sufijo de key: cambia tras guardar y resetea todos los widgets

    area = st.selectbox(
        "1. ÁREA A LA QUE VA A REALIZAR EL MANTENIMIENTO",
        ["Seleccione un área...", "Tintorería", "Tiendas", "Planta/Confección"],
        key=f"area_{v}"
    )

    if area != "Seleccione un área...":
        hora_default = datetime.datetime.now(TZ_BOGOTA).time()

        if area == "Tintorería":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora de mantenimiento", hora_default, key=f"hora_{v}")
                num_maquina = st.text_input("3. Número de máquina (KPL)", key=f"num_maquina_{v}")
                tipo_maquina = st.selectbox("5. Tipo de máquina", maquinas_tintoreria, key=f"tipo_maquina_{v}")
                tipo_intervencion = st.text_input("7. Tipo de intervención", key=f"tipo_intervencion_{v}")
            with col2:
                codigo_inv = st.text_input("4. Código de inventario", key=f"codigo_inv_{v}").upper()
                tipo_mantenimiento = st.selectbox("6. Tipo de mantenimiento", tipos_mantenimiento_general, key=f"tipo_mant_{v}")
                elementos = st.multiselect("8. Elementos a intervenir", elementos_tintoreria, key=f"elementos_{v}")
                elementos_str = ", ".join(elementos)

            observaciones = st.text_area("9. Observaciones del mantenimiento", key=f"obs_{v}")
            colaborador = st.text_input("17. Colaborador que realizó el mantenimiento", key=f"colaborador_{v}")

        elif area == "Tiendas":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora inicio mantenimiento", hora_default, key=f"hora_{v}")
                tipo_mantenimiento = st.selectbox("4. Tipo de mantenimiento", tipos_mantenimiento_tiendas, key=f"tipo_mant_{v}")
                elementos_str = st.text_area("6. Elementos a intervenir", key=f"elementos_str_{v}")
            with col2:
                tienda = st.selectbox("3. Tienda donde se realiza", tiendas_kenzo, key=f"tienda_{v}")
                tipo_intervencion = st.text_input("5. Tipo de intervención", key=f"tipo_intervencion_{v}")
                colaborador = st.text_input("12. Operario que realizó el mantenimiento", key=f"colaborador_{v}")

            observaciones = st.text_area("7. Observaciones del mantenimiento", key=f"obs_{v}")

        elif area == "Planta/Confección":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora inicio mantenimiento", hora_default, key=f"hora_{v}")
                codigo_inv = st.text_input("4. Código Inventario KPL", key=f"codigo_inv_{v}").upper()
                tipo_mantenimiento = st.selectbox("6. Tipo de mantenimiento", tipos_mantenimiento_confeccion, key=f"tipo_mant_{v}")
                trabajo_realizado = st.text_area("8. Trabajo realizado", key=f"trabajo_{v}")
                mecanico = st.selectbox("15. Mecánico", mecanicos, key=f"mecanico_{v}")
            with col2:
                num_modulo = st.text_input("3. Número de módulo", key=f"num_modulo_{v}")
                tipo_maquina = st.selectbox("5. Tipo de máquina", maquinas_confeccion, key=f"tipo_maquina_{v}")
                tipo_intervencion = st.selectbox("7. Intervención", tipos_intervencion_conf, key=f"tipo_intervencion_{v}")
                operario_conf = st.text_input("16. Nombre Operario", key=f"operario_{v}")

        st.markdown("### ⚙️ Repuestos y Residuos")
        col_rep, col_res = st.columns(2)

        req_repuestos = "No"
        tipo_repuesto = ""
        costo_repuesto = 0.0

        with col_rep:
            if area in ["Tintorería", "Planta/Confección"]:
                req_repuestos = st.radio("¿Se requieren repuestos?", ["No", "Sí"], key=f"req_repuestos_{v}")
                if req_repuestos == "Sí":
                    tipo_repuesto = st.text_input("Tipo de repuesto", key=f"tipo_repuesto_{v}")
                    costo_repuesto = st.number_input("Costo de repuesto ($)", min_value=0.0, step=1000.0, key=f"costo_repuesto_{v}")

        gen_residuos = "No"
        tipo_residuo = ""
        desc_residuo = ""
        disposicion = ""

        with col_res:
            gen_residuos = st.radio("¿Generó residuos?", ["No", "Sí"], key=f"gen_residuos_{v}")
            if gen_residuos == "Sí":
                tipo_residuo = st.selectbox("Tipo de residuo", ["Aprovechable", "No Aprovechable", "Peligroso / Químico", "Especial"], key=f"tipo_residuo_{v}")
                desc_residuo = st.text_input("Descripción del residuo", key=f"desc_residuo_{v}")
                disposicion = st.text_input("Disposición final", key=f"disposicion_{v}")

        st.markdown("---")
        submit_btn = st.button("Guardar Reporte", type="primary", key=f"submit_{v}")

        if submit_btn:
            errores = []
            if area in ["Tintorería", "Planta/Confección"] and tipo_maquina == PLACEHOLDER:
                errores.append("Selecciona el tipo de máquina.")
            if tipo_mantenimiento == PLACEHOLDER:
                errores.append("Selecciona el tipo de mantenimiento.")
            if area == "Planta/Confección" and mecanico == PLACEHOLDER:
                errores.append("Selecciona el mecánico.")
            if area == "Planta/Confección" and tipo_intervencion == PLACEHOLDER:
                errores.append("Selecciona la intervención.")
            if area == "Tiendas" and tienda == PLACEHOLDER:
                errores.append("Selecciona la tienda.")

            if errores:
                for e in errores:
                    st.warning(f"⚠️ {e}")
            else:
                marca_temporal = datetime.datetime.now(TZ_BOGOTA).strftime("%d/%m/%Y %H:%M:%S")
                try:
                    costo_final = costo_repuesto if req_repuestos == "Sí" else 0
                    FOTO = ""

                    if area == "Tintorería":
                        row_data = [
                            marca_temporal, str(hora), num_maquina, codigo_inv, tipo_maquina,
                            tipo_mantenimiento, tipo_intervencion, elementos_str, observaciones,
                            req_repuestos, tipo_repuesto, costo_final,
                            gen_residuos, tipo_residuo, desc_residuo, FOTO,
                            disposicion, colaborador
                        ]
                        guardar_en_hoja(HOJA_TINTORERIA, row_data)

                    elif area == "Tiendas":
                        row_data = [
                            marca_temporal, str(hora), tienda, tipo_mantenimiento, tipo_intervencion,
                            elementos_str, observaciones,
                            gen_residuos, tipo_residuo, desc_residuo, FOTO,
                            disposicion, colaborador
                        ]
                        guardar_en_hoja(HOJA_TIENDAS, row_data)

                    elif area == "Planta/Confección":
                        row_data = [
                            marca_temporal, str(hora), num_modulo, codigo_inv, tipo_maquina,
                            tipo_mantenimiento, tipo_intervencion, trabajo_realizado,
                            req_repuestos, tipo_repuesto, costo_final, FOTO,
                            gen_residuos, tipo_residuo, desc_residuo,
                            mecanico, operario_conf
                        ]
                        guardar_en_hoja(HOJA_PLANTA, row_data)
                    else:
                        st.error("❌ Área no reconocida, no se guardó el reporte.")
                        st.stop()

                    cargar_datos_dashboard.clear()
                    st.session_state.form_version += 1  # fuerza que todos los widgets reinicien
                    st.success("✅ ¡El reporte se guardó correctamente en Google Sheets!")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error al conectar o guardar en Google Sheets: {e}")

# ============================================================
# PESTAÑA 2: DASHBOARD (versión recortada: KPIs, área/tipo, top máquinas)
# ============================================================
with tab_dashboard:
    st.subheader("📊 Vista general de mantenimiento")

    if st.button("🔄 Actualizar datos"):
        cargar_datos_dashboard.clear()

    df = cargar_datos_dashboard()

    if df.empty:
        st.info("Todavía no hay reportes guardados para mostrar.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de reportes", len(df))
        col2.metric("Costo total en repuestos", f"${df['costo_num'].sum():,.0f}")

        residuos_si = df["residuos"].astype(str).str.strip().str.lower().eq("sí").mean() * 100
        col3.metric("% con residuos generados", f"{residuos_si:.0f}%")

        if df["fecha"].notna().any():
            mes_actual = datetime.datetime.now(TZ_BOGOTA).month
            anio_actual = datetime.datetime.now(TZ_BOGOTA).year
            reportes_mes = df[(df["fecha"].dt.month == mes_actual) & (df["fecha"].dt.year == anio_actual)].shape[0]
        else:
            reportes_mes = 0
        col4.metric("Reportes este mes", reportes_mes)

        st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Reportes por área**")
            st.bar_chart(df["area"].value_counts(), color=COLOR_PRIMARIO)
        with c2:
            st.markdown("**Distribución por tipo de mantenimiento**")
            tm = df["tipo_mantenimiento"].replace("", "Sin dato")
            st.bar_chart(tm.value_counts(), color=COLOR_SECUNDARIO)

        st.markdown("**Top 10 máquinas con más intervenciones**")
        top_maquinas = df[df["tipo_maquina"] != ""]["tipo_maquina"].value_counts().head(10)
        if not top_maquinas.empty:
            st.bar_chart(top_maquinas, color=COLOR_TERCIARIO)
        else:
            st.caption("Sin datos de máquina todavía.")
