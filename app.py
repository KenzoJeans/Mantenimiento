import streamlit as st
import datetime

st.set_page_config(page_title="Reporte de Mantenimiento", layout="wide")

st.title("🔧 Reporte de Mantenimiento")
st.markdown("---")

# --- LISTAS DE DATOS (Listas preparadas para cuando envíes el inventario) ---
mecanicos = ["Jonathan Borrego", "Cristobal Castellanos", "Felipe Cárdenas", "Jhon Jairo Gómez"]
tipos_intervencion_conf = ["Ajuste mecánico", "Instalación del folder", "Ajuste de tensión", "Cambio de elementos", "Programación de máquina"]

# ESPERANDO TUS DATOS PARA LLENAR ESTAS LISTAS:
maquinas_tintoreria = ["Lavadora", "Secadora", "Caldera", "Otro"] 
maquinas_tiendas = ["Aire Acondicionado", "Iluminación", "Vitrina", "Otro"]
maquinas_confeccion = ["Plana", "Fileteadora", "Recubridora", "Otro"]
tiendas_kenzo = ["Tienda Centro", "Tienda Norte", "Tienda Sur"]

# Selector principal
area = st.selectbox(
    "1. ÁREA A LA QUE VA A REALIZAR EL MANTENIMIENTO", 
    ["Seleccione un área...", "Tintorería / Planta", "Tiendas", "Confección"]
)

if area != "Seleccione un área...":
    with st.form(key=f"form_mantenimiento_{area}"):
        
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
                elementos = st.text_area("8. Elementos a intervenir")
            
            observaciones = st.text_area("9. Observaciones del mantenimiento")
            colaborador = st.text_input("17. Colaborador que realizó el mantenimiento")

        # --- SECCIÓN: TIENDAS ---
        elif area == "Tiendas":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora inicio mantenimiento", datetime.datetime.now().time())
                tipo_mantenimiento = st.selectbox("4. Tipo de mantenimiento", ["Preventivo", "Correctivo", "Locativo"])
                elementos = st.text_area("6. Elementos a intervenir")
            with col2:
                tienda = st.selectbox("3. Tienda donde se realiza", tiendas_kenzo) 
                tipo_intervencion = st.text_input("5. Tipo de intervención")
                operario = st.text_input("12. Operario que realizó el mantenimiento")
            
            observaciones = st.text_area("7. Observaciones del mantenimiento")

        # --- SECCIÓN: CONFECCIÓN ---
        elif area == "Confección":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora inicio mantenimiento", datetime.datetime.now().time())
                codigo_inv = st.text_input("4. Código Inventario KPL").upper()
                # Actualizado con Alistamiento y Adecuación
                tipo_mantenimiento = st.selectbox("6. Tipo de mantenimiento", ["Preventivo", "Correctivo", "Alistamiento", "Adecuación"])
                trabajo_realizado = st.text_area("8. Trabajo realizado")
                # Lista de mecánicos actualizada
                mecanico = st.selectbox("15. Mecánico", mecanicos)
            with col2:
                num_modulo = st.text_input("3. Número de módulo")
                tipo_maquina = st.selectbox("5. Tipo de máquina", maquinas_confeccion)
                # Lista de intervención actualizada
                intervencion = st.selectbox("7. Intervención", tipos_intervencion_conf)
                operario = st.text_input("16. Nombre Operario")

        st.markdown("### ⚙️ Repuestos y Residuos")
        col_rep, col_res = st.columns(2)
        
        with col_rep:
            if area in ["Tintorería / Planta", "Confección"]:
                req_repuestos = st.radio("¿Se requieren repuestos?", ["No", "Sí"])
                if req_repuestos == "Sí":
                    tipo_repuesto = st.text_input("Tipo de repuesto")
                    costo_repuesto = st.number_input("Costo de repuesto ($)", min_value=0.0, step=1000.0)

        with col_res:
            gen_residuos = st.radio("¿Generó residuos?", ["No", "Sí"])
            if gen_residuos == "Sí":
                tipo_residuo = st.selectbox("Tipo de residuo", ["Aprovechable", "No Aprovechable", "Peligroso / Químico", "Especial"])
                desc_residuo = st.text_input("Descripción del residuo")
                disposicion = st.text_input("Disposición final")

        st.markdown("### 📸 Evidencia")
        foto = st.file_uploader("Registro Fotográfico", type=['png', 'jpg', 'jpeg'])

        st.markdown("---")
        submit_btn = st.form_submit_button("Guardar Reporte", type="primary")

        if submit_btn:
            st.success("¡Datos listos para enviar!")
            # Aquí irá la lógica del Webhook a Google Sheets
