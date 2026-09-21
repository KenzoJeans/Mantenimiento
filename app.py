import streamlit as st
import datetime
import json
# import requests # Descomentar cuando vayas a conectar el Webhook a Google Sheets

st.set_page_config(page_title="Reporte de Mantenimiento", layout="wide")

st.title("🔧 Reporte de Mantenimiento")
st.markdown("---")

# Selector principal que define qué formulario mostrar
area = st.selectbox(
    "1. ÁREA A LA QUE VA A REALIZAR EL MANTENIMIENTO", 
    ["Seleccione un área...", "Tintorería / Planta", "Tiendas", "Confección"]
)

if area != "Seleccione un área...":
    # Usamos st.form para que la página no se recargue con cada tecla que presiona el técnico
    with st.form(key=f"form_mantenimiento_{area}"):
        
        # --- SECCIÓN: TINTORERÍA / PLANTA ---
        if area == "Tintorería / Planta":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora de mantenimiento", datetime.datetime.now().time())
                num_maquina = st.text_input("3. Número de máquina (KPL)")
                tipo_maquina = st.selectbox("5. Tipo de máquina", ["Lavadora", "Secadora", "Caldera", "Otro"])
                tipo_intervencion = st.text_input("7. Tipo de intervención")
            with col2:
                # Forzamos mayúsculas automáticamente en el código
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
                tienda = st.selectbox("3. Tienda", ["Tienda Centro", "Tienda Norte", "Tienda Sur"]) # Llenar con ubicaciones reales
                tipo_intervencion = st.text_input("5. Tipo de intervención")
                operario = st.text_input("12. Operario que realizó el mantenimiento")
            
            observaciones = st.text_area("7. Observaciones del mantenimiento")

        # --- SECCIÓN: CONFECCIÓN ---
        elif area == "Confección":
            col1, col2 = st.columns(2)
            with col1:
                hora = st.time_input("2. Hora inicio mantenimiento", datetime.datetime.now().time())
                codigo_inv = st.text_input("4. Código Inventario KPL").upper()
                tipo_mantenimiento = st.selectbox("6. Tipo de mantenimiento", ["Preventivo", "Correctivo"])
                trabajo_realizado = st.text_area("8. Trabajo realizado")
                mecanico = st.text_input("15. Mecánico")
            with col2:
                num_modulo = st.text_input("3. Número de módulo")
                tipo_maquina = st.selectbox("5. Tipo de máquina", ["Plana", "Fileteadora", "Recubridora", "Otro"])
                intervencion = st.text_input("7. Intervención")
                operario = st.text_input("16. Nombre Operario")

        st.markdown("### ⚙️ Repuestos y Residuos")
        col_rep, col_res = st.columns(2)
        
        with col_rep:
            # Los repuestos no aplican igual para tiendas, por lo que lo filtramos
            if area in ["Tintorería / Planta", "Confección"]:
                req_repuestos = st.radio("¿Necesita/Se requieren repuestos?", ["No", "Sí"])
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
            # Aquí construyes el diccionario con los datos capturados para enviarlo
            payload = {
                "Area": area,
                "Hora": str(hora),
                "Genera_Residuos": gen_residuos,
                # Puedes agregar el resto de variables mapeadas aquí...
            }
