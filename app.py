import streamlit as st
import datetime
from zoneinfo import ZoneInfo
import gspread
import os

st.set_page_config(page_title="Reporte de Mantenimiento - Kenzo Jeans", page_icon="🔧", layout="wide")

TZ_BOGOTA = ZoneInfo("America/Bogota")
PLACEHOLDER = "Seleccione..."

# Nombre del archivo del logo. Súbelo al repositorio (junto a este app.py) con este nombre exacto,
# o cambia la ruta aquí si lo guardas en una subcarpeta (ej. "assets/logo.png").
LOGO_PATH = "logo.png"


def col_letter(n: int) -> str:
    """Convierte un número de columna (1, 2, 3...) a su letra de Google Sheets (A, B, C...)."""
    letra = ""
    while n > 0:
        n, resto = divmod(n - 1, 26)
        letra = chr(65 + resto) + letra
    return letra


# --- Conexión con Google Sheets mediante gspread + st.secrets ---
@st.cache_resource
def get_gsheet_client():
    creds_dict = dict(st.secrets["gcp_service_account"])
    return gspread.service_account_from_dict(creds_dict)


SPREADSHEET_ID = "1eyXRRNUGEMbWTdNW-hpFraoSCvn-A_LzscTwLrVfAvg"

# Nombres exactos de las pestañas nuevas (deben existir ya en tu Google Sheet)
HOJA_TINTORERIA = "Tintorería"
HOJA_TIENDAS = "Tiendas"
HOJA_PLANTA = "Planta"


def guardar_en_hoja(nombre_hoja: str, row_data: list):
    """Calcula la siguiente fila vacía (según columna A) y escribe con rango explícito,
    evitando que Sheets 'adivine' mal la tabla si hay otros objetos en la pestaña."""
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


# --- ENCABEZADO CON LOGO ---
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=110)
    else:
        st.write("")  # deja el espacio reservado aunque el logo aún no esté subido
with col_titulo:
    st.title("🔧 Reporte de Mantenimiento - Kenzo Jeans")
    st.caption("Completa todos los campos marcados y guarda el reporte antes de cambiar de área.")

st.markdown("---")

# --- LISTAS DE DATOS ---
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

area = st.selectbox(
    "1. ÁREA A LA QUE VA A REALIZAR EL MANTENIMIENTO",
    ["Seleccione un área...", "Tintorería", "Tiendas", "Planta/Confección"]
)

if area != "Seleccione un área...":
    with st.form(key=f"form_mantenimiento_{area}", clear_on_submit=True):

        hora_default = datetime.datetime.now(TZ_BOGOTA).time()

        # --- SECCIÓN: TINTORERÍA / PLANTA ---
        if area == "Tintorería":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora de mantenimiento", hora_default)
                num_maquina = st.text_input("3. Número de máquina (KPL)")
                tipo_maquina = st.selectbox("5. Tipo de máquina", maquinas_tintoreria)
                tipo_intervencion = st.text_input("7. Tipo de intervención")
            with col2:
                codigo_inv = st.text_input("4. Código de inventario").upper()
                tipo_mantenimiento = st.selectbox("6. Tipo de mantenimiento", tipos_mantenimiento_general)
                elementos = st.multiselect("8. Elementos a intervenir", elementos_tintoreria)
                elementos_str = ", ".join(elementos)

            observaciones = st.text_area("9. Observaciones del mantenimiento")
            colaborador = st.text_input("17. Colaborador que realizó el mantenimiento")

        # --- SECCIÓN: TIENDAS ---
        elif area == "Tiendas":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora inicio mantenimiento", hora_default)
                tipo_mantenimiento = st.selectbox("4. Tipo de mantenimiento", tipos_mantenimiento_tiendas)
                elementos_str = st.text_area("6. Elementos a intervenir")
            with col2:
                tienda = st.selectbox("3. Tienda donde se realiza", tiendas_kenzo)
                tipo_intervencion = st.text_input("5. Tipo de intervención")
                colaborador = st.text_input("12. Operario que realizó el mantenimiento")

            observaciones = st.text_area("7. Observaciones del mantenimiento")

        # --- SECCIÓN: CONFECCIÓN ---
        elif area == "Planta/Confección":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora inicio mantenimiento", hora_default)
                codigo_inv = st.text_input("4. Código Inventario KPL").upper()
                tipo_mantenimiento = st.selectbox("6. Tipo de mantenimiento", tipos_mantenimiento_confeccion)
                trabajo_realizado = st.text_area("8. Trabajo realizado")
                mecanico = st.selectbox("15. Mecánico", mecanicos)
            with col2:
                num_modulo = st.text_input("3. Número de módulo")
                tipo_maquina = st.selectbox("5. Tipo de máquina", maquinas_confeccion)
                tipo_intervencion = st.selectbox("7. Intervención", tipos_intervencion_conf)
                operario_conf = st.text_input("16. Nombre Operario")

        st.markdown("### ⚙️ Repuestos y Residuos")
        col_rep, col_res = st.columns(2)

        req_repuestos = "No"
        tipo_repuesto = ""
        costo_repuesto = 0.0

        with col_rep:
            if area in ["Tintorería", "Planta/Confección"]:
                req_repuestos = st.radio("¿Se requieren repuestos?", ["No", "Sí"])
                if req_repuestos == "Sí":
                    tipo_repuesto = st.text_input("Tipo de repuesto")
                    costo_repuesto = st.number_input("Costo de repuesto ($)", min_value=0.0, step=1000.0)

        gen_residuos = "No"
        tipo_residuo = ""
        desc_residuo = ""
        disposicion = ""

        with col_res:
            gen_residuos = st.radio("¿Generó residuos?", ["No", "Sí"])
            if gen_residuos == "Sí":
                tipo_residuo = st.selectbox("Tipo de residuo", ["Aprovechable", "No Aprovechable", "Peligroso / Químico", "Especial"])
                desc_residuo = st.text_input("Descripción del residuo")
                disposicion = st.text_input("Disposición final")

        st.markdown("---")
        submit_btn = st.form_submit_button("Guardar Reporte", type="primary")

        if submit_btn:
            # --- VALIDACIÓN DE CAMPOS OBLIGATORIOS ---
            errores = []
            if area in ["Tintorería", "Planta/Confección"] and tipo_maquina == PLACEHOLDER:
                errores.append("Selecciona el tipo de máquina.")
            if tipo_mantenimiento == PLACEHOLDER:
                errores.append("Selecciona el tipo de mantenimiento.")
            if area == "Planta/Confección" and mecanico == PLACEHOLDER:
                errores.append("Selecciona el mecánico.")
            if area == "Confección" and tipo_intervencion == PLACEHOLDER:
                errores.append("Selecciona la intervención.")
            if area == "Tiendas" and tienda == PLACEHOLDER:
                errores.append("Selecciona la tienda.")

            if errores:
                for e in errores:
                    st.warning(f"⚠️ {e}")
            else:
                marca_temporal = datetime.datetime.now(TZ_BOGOTA).strftime("%Y-%m-%d %H:%M:%S")
                try:
                    if area == "Tintorería":
                        row_data = [
                            marca_temporal, str(hora), num_maquina, codigo_inv, tipo_maquina,
                            tipo_mantenimiento, tipo_intervencion, elementos_str, observaciones,
                            colaborador, req_repuestos, tipo_repuesto,
                            costo_repuesto if req_repuestos == "Sí" else 0,
                            gen_residuos, tipo_residuo, desc_residuo, disposicion
                        ]
                        guardar_en_hoja(HOJA_TINTORERIA, row_data)

                    elif area == "Tiendas":
                        row_data = [
                            marca_temporal, str(hora), tienda, tipo_mantenimiento, tipo_intervencion,
                            elementos_str, observaciones, colaborador,
                            gen_residuos, tipo_residuo, desc_residuo, disposicion
                        ]
                        guardar_en_hoja(HOJA_TIENDAS, row_data)

                    elif area == "Planta":
                        row_data = [
                            marca_temporal, str(hora), num_modulo, codigo_inv, tipo_maquina,
                            tipo_mantenimiento, tipo_intervencion, trabajo_realizado,
                            mecanico, operario_conf, req_repuestos, tipo_repuesto,
                            costo_repuesto if req_repuestos == "Sí" else 0,
                            gen_residuos, tipo_residuo, desc_residuo, disposicion
                        ]
                        guardar_en_hoja(HOJA_PLANTA, row_data)

                    st.success("✅ ¡El reporte se guardó correctamente en Google Sheets!")

                except Exception as e:
                    st.error(f"❌ Error al conectar o guardar en Google Sheets: {e}")
