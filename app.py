import streamlit as st
import datetime
import gspread

st.set_page_config(page_title="Reporte de Mantenimiento", layout="wide")

# Conexión con Google Sheets mediante gspread
@st.cache_resource
def get_gsheet_client():
    creds_dict = dict(st.secrets["gcp_service_account"])
    return gspread.service_account_from_dict(creds_dict)

# ID de tu hoja de Google Sheets
SPREADSHEET_ID = "1eyXRRNUGEMbWTdNW-hpFraoSCvn-A_LzscTwLrVfAvg"

st.title("🔧 Reporte de Mantenimiento - Kenzo Jeans")
st.markdown("---")

# --- LISTAS DE DATOS ---
mecanicos = ["Jonathan Borrego", "Cristobal Castellanos", "Felipe Cárdenas", "Jhon Jairo Gómez"]
tipos_intervencion_conf = [
    "Ajuste mecánico", "Instalación del folder", "Ajuste de tensión", 
    "Cambio de elementos", "Programación de máquina"
]

maquinas_confeccion = [
    "CADENETA", "FILETEADORA", "PLANA", "DOS AGUJAS", "COLLARIN PLANA", "COLLARIN CILINDRICA", 
    "COLLARIN CODO", "EMPRETINADORA", "PRESILLADORA", "MAQUINA DE BOTAS", "MAQUINA DE J", 
    "DIBUJADORA", "OJALADORA DE CAMISA", "OJALADORA DE LÁGRIMA", "PEGAR PASADORES", "HACER PASADORES", 
    "RIBETEADORA", "FUSIONADORA", "VOLTEADORA DE PANTALÓN", "DOBLADILLADORA DE BOLSILLO", "CERRADORA", 
    "CERRADORA DE CAMISA", "CERRADORA DE CODO", "CERRADORA DE PEDESTAL", "CORTADORA VERTICAL", 
    "CORTADORA AUTOMÁTICA", "LÁSER", "BORDADORA", "TACHADORA", "PARCHADORA", "MULTIAGUJAS", 
    "BOTONADORA", "REVISADORA DE TELAS", "MAQUINA FUSIONADORA"
]

maquinas_tintoreria = [
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

tiendas_kenzo = [
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
    ["Seleccione un área...", "Tintorería / Planta", "Tiendas", "Confección"]
)

if area != "Seleccione un área...":
    with st.form(key=f"form_mantenimiento_{area}"):
        
        # Variable inicializadoras
        num_maquina = ""
        codigo_inv = ""
        tipo_maquina = ""
        tipo_mantenimiento = ""
        tipo_intervencion = ""
        elementos_str = ""
        observaciones = ""
        colaborador = ""
        tienda = ""
        num_modulo = ""
        trabajo_realizado = ""
        
        # --- SECCIÓN: TINTORERÍA / PLANTA ---
        if area == "Tintorería / Planta":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora de mantenimiento", datetime.datetime.now().time())
                num_maquina = st.text_input("3. Número de máquina (KPL)")
                tipo_maquina = st.selectbox("5. Tipo de máquina", maquinas_tintoreria)
                tipo_intervencion = st.text_input("7. Tipo de intervención")
            with col2:
                codigo_inv = st.text_input("4. Código de inventario").upper()
                tipo_mantenimiento = st.selectbox("6. Tipo de mantenimiento", ["Preventivo", "Correctivo", "Predictivo"])
                elementos = st.multiselect("8. Elementos a intervenir", elementos_tintoreria)
                elementos_str = ", ".join(elementos)
            
            observaciones = st.text_area("9. Observaciones del mantenimiento")
            colaborador = st.text_input("17. Colaborador que realizó el mantenimiento")

        # --- SECCIÓN: TIENDAS ---
        elif area == "Tiendas":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora inicio mantenimiento", datetime.datetime.now().time())
                tipo_mantenimiento = st.selectbox("4. Tipo de mantenimiento", ["Preventivo", "Correctivo", "Locativo"])
                elementos_str = st.text_area("6. Elementos a intervenir")
            with col2:
                tienda = st.selectbox("3. Tienda donde se realiza", tiendas_kenzo) 
                tipo_intervencion = st.text_input("5. Tipo de intervención")
                colaborador = st.text_input("12. Operario que realizó el mantenimiento")
            
            observaciones = st.text_area("7. Observaciones del mantenimiento")

        # --- SECCIÓN: CONFECCIÓN ---
        elif area == "Confección":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora inicio mantenimiento", datetime.datetime.now().time())
                codigo_inv = st.text_input("4. Código Inventario KPL").upper()
                tipo_mantenimiento = st.selectbox("6. Tipo de mantenimiento", ["Preventivo", "Correctivo", "Alistamiento", "Adecuación"])
                trabajo_realizado = st.text_area("8. Trabajo realizado")
                mecanico = st.selectbox("15. Mecánico", mecanicos)
            with col2:
                num_modulo = st.text_input("3. Número de módulo")
                tipo_maquina = st.selectbox("5. Tipo de máquina", maquinas_confeccion)
                tipo_intervencion = st.selectbox("7. Intervención", tipos_intervencion_conf)
                operario_conf = st.text_input("16. Nombre Operario")
                colaborador = f"{mecanico} (Operario: {operario_conf})" if operario_conf else mecanico

        st.markdown("### ⚙️ Repuestos y Residuos")
        col_rep, col_res = st.columns(2)
        
        req_repuestos = "No"
        tipo_repuesto = ""
        costo_repuesto = 0.0
        
        with col_rep:
            if area in ["Tintorería / Planta", "Confección"]:
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
            try:
                # 1. Autenticar con Google Sheets
                gc = get_gsheet_client()
                sh = gc.open_by_key(SPREADSHEET_ID)
                worksheet = sh.worksheet("DATOS GENERALES")
                
                # 2. Generar Timestamp
                marca_temporal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # 3. Construir la fila mapeando exactamente a las 21 columnas
                row_data = [
                    marca_temporal,
                    area,
                    str(hora),
                    num_maquina,
                    codigo_inv,
                    tipo_maquina,
                    tipo_mantenimiento,
                    tipo_intervencion,
                    elementos_str,
                    observaciones,
                    colaborador,
                    tienda,
                    num_modulo,
                    trabajo_realizado,
                    req_repuestos,
                    tipo_repuesto,
                    costo_repuesto if req_repuestos == "Sí" else 0,
                    gen_residuos,
                    tipo_residuo,
                    desc_residuo,
                    disposicion
                ]
                
                # 4. Insertar fila en Google Sheets
                worksheet.append_row(row_data)
                st.success("✅ ¡El reporte se guardó correctamente en Google Sheets!")
                
            except Exception as e:
                st.error(f"❌ Error al conectar o guardar en Google Sheets: {e}")
