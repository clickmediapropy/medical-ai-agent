"""
Componentes del dashboard principal.
"""

import streamlit as st
from src.core.models import AlertLevel, ConditionType
from src.core.calculators import MedicalCalculator


def render_dashboard():
    """Renderiza el dashboard principal"""
    patient = st.session_state.patient_data

    if not patient.lab_results:
        st.info("👋 Bienvenido al Sistema de Monitoreo Médico. Comience ingresando algunos datos de laboratorio usando el menú lateral.")
        render_empty_state()
        return

    # Alertas críticas primero
    render_alerts()

    # Métricas principales
    st.subheader("📊 Valores Más Recientes")
    render_latest_values()

    # Resumen del paciente
    st.subheader("📋 Resumen del Paciente")
    render_patient_summary()


def render_alerts():
    """Renderiza alertas basadas en valores críticos"""
    patient = st.session_state.patient_data
    critical_values = patient.get_critical_values()

    if critical_values:
        st.error("⚠️ **VALORES CRÍTICOS DETECTADOS**")
        for value in critical_values:
            alert_emoji = "🔴" if value.alert_level == AlertLevel.CRITICO else "🟡"
            st.warning(f"{alert_emoji} **{value.test_name}**: {value.value} {value.unit}")


def render_latest_values():
    """Renderiza los valores más recientes de laboratorio"""
    patient = st.session_state.patient_data

    # Obtener tests únicos
    test_names = list(set(r.test_name for r in patient.lab_results))

    # Crear columnas para métricas
    cols = st.columns(min(4, len(test_names)))

    for idx, test_name in enumerate(test_names[:4]):
        latest = patient.get_latest_lab(test_name)
        if latest:
            with cols[idx % 4]:
                # Color según nivel de alerta
                if latest.alert_level == AlertLevel.CRITICO:
                    color = "🔴"
                elif latest.alert_level == AlertLevel.ALERTA:
                    color = "🟡"
                elif latest.alert_level == AlertLevel.ATENCION:
                    color = "🟠"
                else:
                    color = "🟢"

                st.metric(
                    label=f"{color} {test_name}",
                    value=f"{latest.value} {latest.unit}",
                    delta=None  # Podríamos calcular cambio vs anterior
                )
                st.caption(f"Fecha: {latest.date.strftime('%d/%m/%Y')}")


def render_patient_summary():
    """Renderiza el resumen del paciente"""
    patient = st.session_state.patient_data
    summary = patient.get_summary()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Análisis Totales", summary['total_labs'])
        st.metric("Tests Únicos", summary['unique_tests'])

    with col2:
        st.metric("Medicaciones Activas", summary['active_medications'])
        st.metric("Valores Críticos", summary['critical_values'])

    with col3:
        st.metric("Condiciones", len(patient.conditions))
        st.caption(f"Última actualización: {summary['latest_update']}")


def render_empty_state():
    """Renderiza el estado vacío del dashboard"""
    st.markdown("""
    ### 🚀 Cómo empezar:

    1. **Registre las condiciones médicas** usando el botón en el menú lateral
    2. **Ingrese resultados de laboratorio** con los valores más recientes
    3. **Agregue medicaciones** actuales si las conoce
    4. **Registre signos vitales** cuando estén disponibles

    El sistema calculará automáticamente:
    - Valores fuera de rango
    - Alertas críticas
    - Tendencias temporales
    - Preguntas sugeridas para médicos
    """)

    # Mostrar información educativa básica
    with st.expander("ℹ️ ¿Para qué sirve este sistema?"):
        st.write("""
        Este sistema le ayuda a:
        - **Entender** mejor los valores de laboratorio
        - **Detectar** valores que requieren atención
        - **Seguir** la evolución en el tiempo
        - **Preparar** preguntas para el equipo médico
        - **Aprender** sobre las condiciones médicas

        **Importante:** Este sistema es educativo y de apoyo.
        No reemplaza el criterio médico profesional.
        """)


def render_calculator_cards():
    """Renderiza tarjetas con calculadoras rápidas"""
    calculator = MedicalCalculator()

    st.subheader("🧮 Calculadoras Rápidas")

    # Si hay creatinina, calcular eGFR
    patient = st.session_state.patient_data
    cr_result = patient.get_latest_lab('creatinine')

    if cr_result:
        col1, col2 = st.columns(2)
        with col1:
            egfr = calculator.egfr_ckdepi_2021(
                cr_result.value,
                patient.age,
                False  # Asumir masculino por ahora
            )
            if 'error' not in egfr:
                st.info(f"**eGFR:** {egfr['egfr']} mL/min/1.73m²")
                st.caption(egfr['stage'])

    # Si hay TSH, evaluar riesgo
    tsh_result = patient.get_latest_lab('tsh')
    if tsh_result:
        risk = calculator.thyroid_crisis_risk(tsh_result.value)
        color_map = {'green': '🟢', 'yellow': '🟡', 'orange': '🟠', 'red': '🔴'}
        color = color_map.get(risk['color'], '⚪')
        st.warning(f"{color} Riesgo Mixedematoso: {risk['risk_level']}")