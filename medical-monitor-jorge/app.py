"""
Sistema de Monitoreo Médico - Jorge Agustín
Aplicación principal Streamlit
"""

import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.core.models import PatientData, LabResult, ConditionType, AlertLevel
from src.core.calculators import MedicalCalculator
from src.core.validators import MedicalValidator
from src.core import database as db
from src.ui.forms import render_lab_form, render_condition_form
from src.ui.dashboard import render_dashboard, render_alerts
from src.ui.charts import create_trend_chart

# Configuración de la página
st.set_page_config(
    page_title="Monitor Médico - Jorge Agustín",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stAlert {
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .critical {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .warning {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .normal {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Inicializa el estado de la sesión"""
    if 'patient_data' not in st.session_state:
        st.session_state.patient_data = PatientData()
        # Inicializar base de datos y cargar datos existentes
        st.session_state.db_conn = db.init_database()
        db.load_existing_data(st.session_state.db_conn, st.session_state.patient_data)
    if 'show_lab_form' not in st.session_state:
        st.session_state.show_lab_form = False
    if 'show_condition_form' not in st.session_state:
        st.session_state.show_condition_form = False


def main():
    """Función principal de la aplicación"""
    initialize_session_state()

    # Header
    st.title("🏥 Sistema de Monitoreo Médico")
    st.markdown("### Jorge Agustín Delgado Puentes")

    # Información de última actualización
    col1, col2, col3 = st.columns([2, 2, 3])
    with col1:
        st.caption(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    with col2:
        st.caption(f"🕐 Hora: {datetime.now().strftime('%H:%M')}")
    with col3:
        total_labs = len(st.session_state.patient_data.lab_results)
        if total_labs > 0:
            st.caption(f"📊 Total de análisis registrados: {total_labs}")
        else:
            st.caption("📊 Sin datos registrados aún")

    # Sidebar para entrada de datos
    with st.sidebar:
        st.header("📝 Entrada de Datos")

        # Botones para mostrar formularios
        if st.button("➕ Agregar Resultado de Laboratorio", use_container_width=True):
            st.session_state.show_lab_form = not st.session_state.show_lab_form

        if st.button("🏥 Actualizar Condiciones Médicas", use_container_width=True):
            st.session_state.show_condition_form = not st.session_state.show_condition_form

        if st.button("💊 Registrar Medicación", use_container_width=True):
            st.info("Función en desarrollo")

        if st.button("📊 Registrar Signos Vitales", use_container_width=True):
            st.info("Función en desarrollo")

        st.divider()

        # Información del paciente
        st.subheader("👤 Información del Paciente")
        st.text(f"Nombre: {st.session_state.patient_data.name}")
        st.text(f"Edad: {st.session_state.patient_data.age} años")

        if st.session_state.patient_data.conditions:
            st.subheader("📋 Condiciones Actuales")
            for condition in st.session_state.patient_data.conditions:
                st.text(f"• {condition.value}")
        else:
            st.info("Sin condiciones registradas")

    # Área principal
    if st.session_state.show_lab_form:
        render_lab_form()

    if st.session_state.show_condition_form:
        render_condition_form()

    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "📈 Tendencias",
        "🧮 Calculadoras",
        "❓ Preguntas Sugeridas",
        "📚 Educación"
    ])

    with tab1:
        render_dashboard()

    with tab2:
        render_trends_tab()

    with tab3:
        render_calculators_tab()

    with tab4:
        render_questions_tab()

    with tab5:
        render_education_tab()


def render_trends_tab():
    """Renderiza la pestaña de tendencias"""
    st.header("📈 Tendencias de Valores")

    if not st.session_state.patient_data.lab_results:
        st.info("No hay datos de laboratorio para mostrar tendencias. Ingrese algunos resultados primero.")
        return

    # Obtener lista de tests únicos
    test_names = list(set(r.test_name for r in st.session_state.patient_data.lab_results))

    if test_names:
        selected_test = st.selectbox("Seleccione el test a visualizar:", test_names)

        if selected_test:
            results = st.session_state.patient_data.get_lab_trend(selected_test, days=365)
            if len(results) > 1:
                chart = create_trend_chart(results, selected_test)
                st.plotly_chart(chart, use_container_width=True)
            else:
                st.info(f"Se necesitan al menos 2 mediciones de {selected_test} para mostrar tendencia.")


def render_calculators_tab():
    """Renderiza la pestaña de calculadoras médicas"""
    st.header("🧮 Calculadoras Médicas")

    # Obtener datos más recientes del paciente
    patient_data = st.session_state.patient_data
    calculator = MedicalCalculator()

    # Obtener valores más recientes si existen
    latest_creatinine = patient_data.get_latest_lab("Creatinina")
    latest_tsh = patient_data.get_latest_lab("TSH")
    latest_t4 = patient_data.get_latest_lab("T4 Libre")
    latest_calcium = patient_data.get_latest_lab("Calcio")
    latest_pth = patient_data.get_latest_lab("PTH")
    latest_phosphorus = patient_data.get_latest_lab("Fósforo")
    latest_hemoglobin = patient_data.get_latest_lab("Hemoglobina")

    # Calculadora eGFR
    with st.expander("Tasa de Filtración Glomerular (eGFR)", expanded=True):
        if latest_creatinine:
            st.success(f"📊 Usando valor más reciente: Creatinina de {latest_creatinine.date.strftime('%d/%m/%Y')}")

        col1, col2, col3 = st.columns(3)
        with col1:
            default_cr = latest_creatinine.value if latest_creatinine else 1.0
            cr = st.number_input("Creatinina (mg/dL)",
                               min_value=0.1,
                               max_value=20.0,
                               value=float(default_cr),
                               step=0.1,
                               help=f"Último valor: {default_cr} mg/dL ({latest_creatinine.date.strftime('%d/%m/%Y')})" if latest_creatinine else "Sin datos previos")
        with col2:
            age = st.number_input("Edad (años)", min_value=18, max_value=120, value=patient_data.age, step=1)
        with col3:
            sex = st.selectbox("Sexo", ["Masculino", "Femenino"], key="egfr_sex")

        if st.button("Calcular eGFR") or latest_creatinine:
            result = calculator.egfr_ckdepi_2021(cr, age, sex == "Femenino")
            if 'error' not in result:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("eGFR", f"{result['egfr']} {result['unit']}")
                with col2:
                    color = "🟢" if result['color'] == 'green' else "🟡" if result['color'] == 'yellow' else "🔴"
                    st.metric("Estadio", f"{color} {result['stage']}")
                st.info(result['interpretation'])
                if result['requires_dialysis']:
                    st.error("⚠️ Requiere diálisis o trasplante renal")

    # Calculadora de riesgo de crisis tiroidea
    with st.expander("Riesgo de Crisis Mixedematosa"):
        if latest_tsh or latest_t4:
            st.success(f"📊 Usando valores más recientes disponibles")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            default_tsh = latest_tsh.value if latest_tsh else 4.0
            tsh = st.number_input("TSH (μUI/mL)",
                                min_value=0.01,
                                max_value=100000.0,
                                value=float(default_tsh),
                                step=1.0,
                                help=f"Último valor: {default_tsh} μUI/mL ({latest_tsh.date.strftime('%d/%m/%Y')})" if latest_tsh else "Sin datos previos")
        with col2:
            default_t4 = latest_t4.value if latest_t4 else 1.0
            t4 = st.number_input("T4 libre (ng/dL)",
                               min_value=0.1,
                               max_value=10.0,
                               value=float(default_t4),
                               step=0.1,
                               help=f"Último valor: {default_t4} ng/dL ({latest_t4.date.strftime('%d/%m/%Y')})" if latest_t4 else "Sin datos previos")
        with col3:
            # Temperatura: asumimos hipotermia leve por el estado crítico del paciente
            temp = st.number_input("Temperatura (°C)",
                                 min_value=32.0,
                                 max_value=42.0,
                                 value=35.5,  # Hipotermia común en UCI con sedación
                                 step=0.1,
                                 help="Paciente en UCI con sedación - común hipotermia leve")
        with col4:
            # Estado mental: estuporoso por TCE y sedación
            mental = st.selectbox("Estado mental",
                                ["normal", "confuso", "somnoliento", "estuporoso"],
                                index=3,  # Selecciona "estuporoso" por defecto
                                key="thyroid_mental",
                                help="Paciente con TCE severo + sedación = estuporoso")

        if st.button("Evaluar Riesgo Tiroideo") or (latest_tsh and latest_tsh.value > 10):
            result = calculator.thyroid_crisis_risk(tsh, t4, temp, mental)
            color_emoji = "🟢" if result['color'] == 'green' else "🟡" if result['color'] == 'yellow' else "🟠" if result['color'] == 'orange' else "🔴"

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Nivel de Riesgo", f"{color_emoji} {result['risk_level']}")
            with col2:
                st.metric("Puntaje de Riesgo", f"{result['risk_score']}/100",
                        help="≥70: Crítico | 40-69: Alto | 20-39: Moderado | <20: Bajo")

            if result['risk_factors']:
                st.warning("**Factores de riesgo identificados:**")
                for factor in result['risk_factors']:
                    st.write(f"• {factor}")

            if result['recommendations']:
                st.info("**Recomendaciones:**")
                for rec in result['recommendations']:
                    st.write(f"• {rec}")

            if result['requires_urgent_action']:
                st.error("⚠️ REQUIERE ACCIÓN URGENTE - Contactar endocrinólogo inmediatamente")

    # Nueva calculadora: Análisis Calcio-PTH
    with st.expander("Análisis Calcio-PTH"):
        if latest_calcium or latest_pth:
            st.success(f"📊 Usando valores más recientes disponibles")

        col1, col2, col3 = st.columns(3)
        with col1:
            default_ca = latest_calcium.value if latest_calcium else 9.5
            calcium = st.number_input("Calcio (mg/dL)",
                                     min_value=5.0,
                                     max_value=15.0,
                                     value=float(default_ca),
                                     step=0.1,
                                     help=f"Último valor: {default_ca} mg/dL ({latest_calcium.date.strftime('%d/%m/%Y')})" if latest_calcium else "Sin datos previos")
        with col2:
            default_pth = latest_pth.value if latest_pth else 50.0
            pth = st.number_input("PTH (pg/mL)",
                                min_value=1.0,
                                max_value=500.0,
                                value=float(default_pth),
                                step=1.0,
                                help=f"Último valor: {default_pth} pg/mL ({latest_pth.date.strftime('%d/%m/%Y')})" if latest_pth else "Sin datos previos")
        with col3:
            default_phos = latest_phosphorus.value if latest_phosphorus else 3.5
            phosphorus = st.number_input("Fósforo (mg/dL)",
                                        min_value=1.0,
                                        max_value=10.0,
                                        value=float(default_phos),
                                        step=0.1,
                                        help=f"Último valor: {default_phos} mg/dL ({latest_phosphorus.date.strftime('%d/%m/%Y')})" if latest_phosphorus else "Sin datos previos")

        if st.button("Analizar Balance Mineral") or (latest_pth and latest_calcium):
            result = calculator.calcium_pth_analysis(calcium, pth, phosphorus, has_irc=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                ca_color = "🟢" if result['calcium_status'] == 'normal' else "🟡" if result['calcium_status'] == 'bajo' else "🔴"
                st.metric("Calcio", f"{ca_color} {result['calcium_status'].capitalize()}")
            with col2:
                pth_color = "🟢" if result['pth_status'] == 'normal' else "🟡" if result['pth_status'] == 'bajo' else "🔴"
                st.metric("PTH", f"{pth_color} {result['pth_status'].capitalize()}")
            with col3:
                if phosphorus:
                    ca_p_product = calcium * phosphorus
                    product_color = "🟢" if ca_p_product <= 55 else "🔴"
                    st.metric("Producto Ca×P", f"{product_color} {ca_p_product:.1f} mg²/dL²")

            st.info(result['interpretation'])

            if result['findings']:
                st.warning("**Hallazgos:**")
                for finding in result['findings']:
                    st.write(f"• {finding}")

            if result['requires_treatment']:
                st.error("⚠️ Requiere evaluación médica para ajuste de tratamiento")

    # Evaluación de Anemia
    with st.expander("Evaluación de Anemia"):
        if latest_hemoglobin:
            st.success(f"📊 Usando hemoglobina más reciente: {latest_hemoglobin.date.strftime('%d/%m/%Y')}")

        col1, col2 = st.columns(2)
        with col1:
            default_hb = latest_hemoglobin.value if latest_hemoglobin else 12.0
            hb = st.number_input("Hemoglobina (g/dL)",
                               min_value=3.0,
                               max_value=20.0,
                               value=float(default_hb),
                               step=0.1,
                               help=f"Último valor: {default_hb} g/dL ({latest_hemoglobin.date.strftime('%d/%m/%Y')})" if latest_hemoglobin else "Sin datos previos")
        with col2:
            is_male = st.selectbox("Sexo", ["Masculino", "Femenino"], key="anemia_sex") == "Masculino"

        if st.button("Evaluar Anemia") or (latest_hemoglobin and latest_hemoglobin.value < 12):
            result = calculator.anemia_evaluation(hb, is_male, has_irc=True)

            color = "🟢" if result['severity'] == 'Sin anemia' else "🟡" if result['severity'] == 'Leve' else "🟠" if result['severity'] == 'Moderada' else "🔴"
            st.metric("Severidad", f"{color} {result['severity']}")
            st.metric("Hemoglobina", f"{result['value']} g/dL")

            if result['recommendation']:
                st.info(f"**Recomendación:** {result['recommendation']}")

            if result.get('requires_urgent_eval', False):
                st.error("⚠️ **Requiere evaluación urgente**")


def render_questions_tab():
    """Renderiza la pestaña de preguntas sugeridas"""
    st.header("❓ Preguntas Sugeridas para el Equipo Médico")

    patient = st.session_state.patient_data
    questions = []

    # Generar preguntas basadas en los datos disponibles
    if patient.lab_results:
        # Buscar valores críticos
        critical_values = patient.get_critical_values()
        for value in critical_values:
            questions.append({
                'priority': '🔴 Alta',
                'category': 'Valores Críticos',
                'question': f"¿Qué acciones se están tomando para el {value.test_name} de {value.value} {value.unit}?",
                'context': f"Valor fuera de rango normal"
            })

    # Preguntas basadas en condiciones
    if ConditionType.IRC_TERMINAL in patient.conditions:
        questions.extend([
            {
                'priority': '🟡 Media',
                'category': 'IRC',
                'question': "¿Los medicamentos actuales están ajustados para función renal?",
                'context': "Paciente con IRC terminal"
            },
            {
                'priority': '🟡 Media',
                'category': 'IRC',
                'question': "¿Cuál es el plan de diálisis actual y su adecuación?",
                'context': "Evaluación de Kt/V o URR"
            }
        ])

    if ConditionType.HIPOTIROIDISMO in patient.conditions:
        questions.append({
            'priority': '🔴 Alta',
            'category': 'Endocrino',
            'question': "¿Se ha considerado el riesgo de crisis mixedematosa?",
            'context': "Hipotiroidismo severo"
        })

    # Mostrar preguntas
    if questions:
        for q in questions:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"**{q['priority']}**")
                    st.caption(q['category'])
                with col2:
                    st.markdown(f"**{q['question']}**")
                    st.caption(f"Contexto: {q['context']}")
                st.divider()
    else:
        st.info("Las preguntas sugeridas aparecerán aquí basadas en los datos ingresados y las condiciones del paciente.")


def render_education_tab():
    """Renderiza la pestaña de educación"""
    st.header("📚 Información Educativa")

    topics = {
        "Insuficiencia Renal Crónica (IRC)": {
            "descripcion": "La IRC es la pérdida gradual de la función renal. Los riñones filtran los desechos y el exceso de líquidos de la sangre.",
            "sintomas": ["Fatiga", "Hinchazón", "Cambios en la orina", "Náuseas"],
            "tratamiento": ["Diálisis", "Trasplante", "Medicamentos", "Dieta especial"],
            "monitoreo": ["Creatinina", "Urea", "Potasio", "Fósforo", "Hemoglobina"]
        },
        "Hipotiroidismo": {
            "descripcion": "Condición donde la glándula tiroides no produce suficientes hormonas tiroideas.",
            "sintomas": ["Fatiga", "Aumento de peso", "Sensibilidad al frío", "Depresión"],
            "tratamiento": ["Levotiroxina", "Monitoreo regular de TSH"],
            "monitoreo": ["TSH", "T4 libre", "T3"]
        },
        "Valores de Laboratorio": {
            "descripcion": "Entender los valores de laboratorio ayuda a seguir la evolución del paciente.",
            "importantes": {
                "Creatinina": "Mide la función renal. Valores altos indican daño renal.",
                "TSH": "Hormona estimulante de tiroides. Valores muy altos indican hipotiroidismo.",
                "Hemoglobina": "Transporta oxígeno. Valores bajos indican anemia.",
                "Potasio": "Electrolito crucial. Niveles anormales pueden causar arritmias."
            }
        }
    }

    for topic, info in topics.items():
        with st.expander(topic):
            if "descripcion" in info:
                st.write(f"**Descripción:** {info['descripcion']}")

            if "sintomas" in info:
                st.write("**Síntomas comunes:**")
                for sintoma in info['sintomas']:
                    st.write(f"• {sintoma}")

            if "tratamiento" in info:
                st.write("**Opciones de tratamiento:**")
                for trat in info['tratamiento']:
                    st.write(f"• {trat}")

            if "monitoreo" in info:
                st.write("**Valores a monitorear:**")
                for valor in info['monitoreo']:
                    st.write(f"• {valor}")

            if "importantes" in info:
                st.write("**Valores importantes:**")
                for key, desc in info['importantes'].items():
                    st.write(f"• **{key}:** {desc}")

    st.divider()
    st.info("💡 **Tip:** Esta información es educativa. Siempre consulte con el equipo médico para decisiones de tratamiento.")


if __name__ == "__main__":
    main()