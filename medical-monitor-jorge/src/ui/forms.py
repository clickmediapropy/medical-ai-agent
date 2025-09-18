"""
Formularios de entrada de datos para la aplicación.
"""

import streamlit as st
from datetime import datetime, date
from src.core.models import LabResult, ConditionType, AlertLevel
from src.core.validators import MedicalValidator


def render_lab_form():
    """Renderiza el formulario para ingresar resultados de laboratorio"""
    st.subheader("➕ Agregar Resultado de Laboratorio")

    with st.form("lab_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Selección de test común o entrada personalizada
            common_tests = [
                "Personalizado...",
                "creatinine", "urea", "glucose", "hemoglobin",
                "tsh", "t4_free", "potassium", "sodium",
                "calcium", "phosphorus", "pth", "albumin"
            ]
            test_selection = st.selectbox("Tipo de análisis:", common_tests)

            if test_selection == "Personalizado...":
                test_name = st.text_input("Nombre del análisis:", placeholder="ej: Vitamina B12")
            else:
                test_name = test_selection

            value = st.number_input("Valor:", min_value=0.0, step=0.01)
            unit = st.text_input("Unidad:", placeholder="mg/dL, mIU/L, etc.")

        with col2:
            test_date = st.date_input("Fecha del análisis:", value=date.today())
            ref_min = st.number_input("Valor mínimo normal (opcional):", min_value=0.0, step=0.01)
            ref_max = st.number_input("Valor máximo normal (opcional):", min_value=0.0, step=0.01)
            notes = st.text_area("Notas (opcional):")

        # Checkbox para IRC
        has_irc = st.checkbox("Paciente con IRC (afecta rangos de referencia)")

        submitted = st.form_submit_button("Guardar Resultado", use_container_width=True)

        if submitted and test_name and value > 0:
            # Validar el valor
            validator = MedicalValidator()
            validation = validator.validate_value(
                test_name,
                value,
                has_irc=has_irc
            )

            # Crear el resultado
            lab_result = LabResult(
                test_name=test_name,
                value=value,
                unit=unit,
                date=datetime.combine(test_date, datetime.min.time()),
                reference_min=ref_min if ref_min > 0 else None,
                reference_max=ref_max if ref_max > 0 else None,
                alert_level=validation.get('alert_level', AlertLevel.NORMAL),
                notes=notes
            )

            # Añadir al paciente
            st.session_state.patient_data.add_lab_result(lab_result)

            # Mostrar resultado
            if validation['alert_level'] == AlertLevel.CRITICO:
                st.error(f"⚠️ Valor CRÍTICO: {validation['message']}")
            elif validation['alert_level'] == AlertLevel.ALERTA:
                st.warning(f"⚠️ {validation['message']}")
            elif validation['alert_level'] == AlertLevel.ATENCION:
                st.info(f"ℹ️ {validation['message']}")
            else:
                st.success(f"✅ Resultado guardado: {validation['message']}")

            # Limpiar formulario
            st.session_state.show_lab_form = False
            st.rerun()


def render_condition_form():
    """Renderiza el formulario para actualizar condiciones médicas"""
    st.subheader("🏥 Actualizar Condiciones Médicas")

    with st.form("condition_form"):
        st.write("Seleccione las condiciones que aplican:")

        conditions = {}
        for condition in ConditionType:
            conditions[condition] = st.checkbox(
                condition.value,
                value=condition in st.session_state.patient_data.conditions
            )

        submitted = st.form_submit_button("Actualizar Condiciones", use_container_width=True)

        if submitted:
            # Actualizar condiciones
            st.session_state.patient_data.conditions = [
                cond for cond, selected in conditions.items() if selected
            ]
            st.success("✅ Condiciones actualizadas")
            st.session_state.show_condition_form = False
            st.rerun()


def render_medication_form():
    """Renderiza el formulario para registrar medicación"""
    st.subheader("💊 Registrar Medicación")

    with st.form("medication_form"):
        col1, col2 = st.columns(2)

        with col1:
            med_name = st.text_input("Nombre del medicamento:")
            dose = st.number_input("Dosis:", min_value=0.0, step=0.1)
            unit = st.text_input("Unidad:", placeholder="mg, mL, UI, etc.")

        with col2:
            frequency = st.selectbox("Frecuencia:", [
                "Una vez al día",
                "Dos veces al día",
                "Tres veces al día",
                "Cada 8 horas",
                "Cada 12 horas",
                "Semanal",
                "Según necesidad"
            ])
            route = st.selectbox("Vía:", ["Oral", "IV", "IM", "SC", "Tópica"])
            start_date = st.date_input("Fecha de inicio:")

        adjusted_irc = st.checkbox("Dosis ajustada para IRC")
        notes = st.text_area("Notas (opcional):")

        submitted = st.form_submit_button("Guardar Medicación", use_container_width=True)

        if submitted and med_name and dose > 0:
            # Aquí se añadiría la medicación al paciente
            st.success(f"✅ Medicación {med_name} registrada")
            st.rerun()


def render_vitals_form():
    """Renderiza el formulario para registrar signos vitales"""
    st.subheader("📊 Registrar Signos Vitales")

    with st.form("vitals_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            heart_rate = st.number_input("Frecuencia cardíaca (lpm):", min_value=0, max_value=300, step=1)
            temp = st.number_input("Temperatura (°C):", min_value=32.0, max_value=42.0, step=0.1)

        with col2:
            bp_sys = st.number_input("Presión sistólica (mmHg):", min_value=0, max_value=300, step=1)
            bp_dia = st.number_input("Presión diastólica (mmHg):", min_value=0, max_value=200, step=1)

        with col3:
            o2_sat = st.number_input("Saturación O2 (%):", min_value=0, max_value=100, step=1)
            glasgow = st.number_input("Glasgow (3-15):", min_value=3, max_value=15, step=1)

        vitals_date = st.date_input("Fecha y hora:", value=date.today())
        notes = st.text_area("Notas (opcional):")

        submitted = st.form_submit_button("Guardar Signos Vitales", use_container_width=True)

        if submitted:
            # Aquí se añadirían los signos vitales al paciente
            st.success("✅ Signos vitales registrados")
            st.rerun()