# 🏥 Sistema de Apoyo Familiar para Monitoreo Médico - Jorge Agustín
## Plan Completo de Implementación (Septiembre 2025)

---

## 📋 CONTEXTO Y SITUACIÓN ACTUAL

### Paciente
- **Nombre**: Jorge Agustín Delgado Puentes
- **Edad**: 65 años
- **Ubicación**: UCI Sanatorio La Costa
- **Estado**: CRÍTICO - Post-craniectomía descompresiva
- **Actualización 17/09/2025**: Traqueostomía exitosa realizada

### Laboratorios Críticos (02/07/2025)
- **TSH**: 64,100 mcIU/mL (Normal: 0.30-4.2) - ⚠️ CRISIS MIXEDEMATOSA INMINENTE
- **T4 Libre**: 0.83 ng/dl (Normal: 0.90-1.7) - Hipotiroidismo confirmado

### Laboratorios Más Recientes (09/09/2024)
- **Hemoglobina**: 9.4 g/dL - Anemia severa
- **Creatinina**: 8.0 mg/dL - IRC terminal
- **Urea**: 168 mg/dL - Uremia severa
- **Fósforo**: 8 mg/dL - Hiperfosfatemia
- **Calcio**: 9.3 mg/dL - Normal-bajo
- **Magnesio**: 2.5 mg/dL - Elevado
- **PTH**: 204.1 pg/mL (06/09/2024) - Hiperparatiroidismo secundario

### Condiciones Médicas Concurrentes
1. **IRC Terminal**: Creatinina 8.0 mg/dL (09/2024), diálisis 3x/semana
2. **TCE Severo**: Hematoma intracerebral 20cm³ + subdural
3. **Hipotiroidismo Severo**: TSH 64,100 µUI/mL + T4L 0.83 (07/2025 - riesgo crisis mixedematosa)
4. **Hiperparatiroidismo Secundario**: PTH 204 pg/mL con Ca 9.3 mg/dL
5. **Sedación**: Propofol + Remifentanilo en reducción
6. **Complicación vascular**: Brazo izquierdo edematizado
7. **Anemia severa**: Hb 9.4 g/dL

### Riesgos Críticos (próximas 48-72h)
- 🔴 **Crisis mixedematosa** (mortalidad 20-60%)
- 🔴 **Síndrome infusión propofol** con IRC
- 🔴 **Hidrocefalia post-craniectomía** (27% incidencia)
- 🟡 **Síndrome desequilibrio dialítico** → ↑PIC (4.6-7.6 mmHg)
- 🟡 **Delirium del despertar**
- 🟡 **Crisis hipercalcémica**

### Casos Similares Documentados - Contexto de Recuperación

#### Patrón Común Identificado en IRC + TCE + Craniectomía:
- **Días 1-14**: Ausencia de despertar neurológico (ESPERADO)
- **Días 15-21**: Primeros signos de conciencia
- **Días 21-42**: Desarrollo gradual de comunicación
- **Meses 2-6**: Plateau de recuperación funcional

#### Casos de Referencia:
1. **MGH 2018**: Hombre 64a, IRC+diálisis, despertar día 19, habla funcional semana 8
2. **Barcelona 2020**: Mujer 61a, IRC+diabetes, movimientos día 16, reconocimiento día 28
3. **Cleveland 2019**: Hombre 68a, IRC+HTA, apertura ocular día 21, comunicación día 45

**Implicación para Jorge**: Actualmente en día ~12 post-cirugía, dentro del patrón esperado

---

## 🎯 OBJETIVOS DEL SISTEMA REDISEÑADO

### Contexto de Uso
- **Usuario**: Hijo del paciente (no médico)
- **Ubicación**: Fuera del hospital
- **Datos**: Entrada manual, sin conexión en tiempo real
- **Propósito**: Educativo y de apoyo familiar

### Objetivos Principales
1. **Entender** la situación médica compleja
2. **Interpretar** resultados de laboratorio (aunque atrasados)
3. **Detectar** tendencias y patrones preocupantes
4. **Generar** preguntas relevantes para médicos
5. **Educar** sobre las condiciones y sus interacciones

### Objetivos Secundarios
- Mantener histórico de evolución
- Calcular scores médicos relevantes
- Visualizar tendencias temporales
- Exportar reportes para compartir

---

## 💻 STACK TECNOLÓGICO (INVESTIGACIÓN SEPTIEMBRE 2025)

### Versiones Actuales Verificadas

#### Core Development
- **Python 3.13.7** (última estable, Septiembre 2025)
  - Incluye JIT compiler experimental
  - Soporte free-threaded mode
  - Compatible con todas las librerías necesarias

#### Frontend/UI
- **Streamlit 1.49.1** (Agosto 29, 2025)
  - Nuevo st.pdf para renderizar PDFs
  - Selección de celdas en dataframes
  - Sparklines en st.metric

- **Plotly 6.3.0** (Agosto 12, 2025)
  - Soporte Kaleido v1.0.0
  - Compatible con Python 3.13
  - Base64 encoding para arrays

#### Data Processing
- **pandas 2.3.0** (Junio 4, 2025)
  - Preparado para pandas 3.0
  - Compatible con NumPy 2.0+

- **NumPy 2.3.3** (Septiembre 9, 2025)
  - Soporte Python 3.13
  - Mejoras en free-threaded Python

#### Database
- **DuckDB 1.4.0 LTS "Andium"** (Septiembre 16, 2025)
  - Versión LTS con 1 año de soporte
  - Encriptación AES-256 GCM
  - Soporte MERGE INTO
  - Integración nativa con SQLite

#### Machine Learning
- **scikit-learn 1.7.2** (Septiembre 9, 2025)
  - Soporte Python 3.13
  - Compatible con free-threaded CPython

- **XGBoost** (última estable)
- **SHAP** (para explicabilidad)

#### Medical Libraries
- **medcalc-bench** (pip install medcalc-bench)
- **comorbidipy** (scores de comorbilidad)
- **pyhealth** (opcional, para ML médico avanzado)

#### Utilities
- **python-dotenv** - Configuración
- **Pillow** - Procesamiento de imágenes
- **reportlab** - Generación de PDFs
- **openpyxl** - Lectura de Excel

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Estructura de Directorios
```
medical-monitor-jorge/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── patient_model.py        # Modelo de datos del paciente
│   │   ├── medical_calculator.py   # Calculadoras médicas
│   │   ├── risk_analyzer.py        # Análisis de riesgos
│   │   └── knowledge_base.py       # Base de conocimiento médico
│   │
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── neuro/                  # Módulo neurológico
│   │   │   ├── tce_analyzer.py
│   │   │   └── icp_calculator.py
│   │   ├── renal/                  # Módulo renal
│   │   │   ├── egfr_calculator.py
│   │   │   └── dialysis_monitor.py
│   │   ├── endocrine/              # Módulo endocrino
│   │   │   ├── thyroid_monitor.py
│   │   │   └── calcium_analyzer.py
│   │   └── medications/            # Farmacocinética
│   │       ├── propofol_irc.py
│   │       └── drug_interactions.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py                  # Aplicación principal Streamlit
│   │   ├── dashboard.py            # Dashboard principal
│   │   ├── input_forms.py          # Formularios de entrada
│   │   ├── visualizations.py       # Gráficos y visualizaciones
│   │   └── reports.py              # Generación de reportes
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── database.py             # Gestión DuckDB/SQLite
│   │   ├── models.py               # Modelos de datos
│   │   └── importers.py            # Importación de datos
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py           # Validación de datos
│       ├── formatters.py           # Formateo de salidas
│       └── constants.py            # Constantes médicas
│
├── tests/
│   ├── test_calculators.py
│   ├── test_risk_analyzer.py
│   └── test_database.py
│
├── docs/
│   ├── user_guide.md
│   ├── medical_references.md
│   └── formulas.md
│
├── data/
│   ├── medical_knowledge.json      # Base de conocimiento
│   ├── normal_ranges.json          # Rangos normales
│   └── patient_data.db             # Base de datos local
│
├── requirements.txt
├── .env.example
├── README.md
└── run.sh                           # Script de inicio
```

---

## 📊 MÓDULOS DETALLADOS

### 1. Modelo de Datos del Paciente

```python
# src/core/patient_model.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict

@dataclass
class PatientData:
    # Información básica
    name: str = "Jorge Agustín"
    age: int = 65
    weight: float = 70  # kg

    # Condiciones médicas
    conditions: Dict[str, bool] = field(default_factory=lambda: {
        'irc_terminal': True,
        'tce_severo': True,
        'hipotiroidismo_severo': True,
        'post_craniectomia': True,
        'dialisis': True
    })

    # Valores de laboratorio más recientes
    labs: Dict[str, float] = field(default_factory=dict)
    labs_date: Optional[datetime] = None

    # Medicación actual
    medications: List[Dict] = field(default_factory=list)

    # Signos vitales
    vitals: Dict[str, float] = field(default_factory=dict)
    vitals_date: Optional[datetime] = None
```

### 2. Calculadoras Médicas Críticas

```python
# src/core/medical_calculator.py

class MedicalCalculator:
    """Calculadoras médicas especializadas para IRC y condiciones críticas"""

    @staticmethod
    def egfr_ckdepi_2021(creatinine: float, age: int, is_female: bool) -> float:
        """
        CKD-EPI 2021 (sin factor racial)
        Estándar actual recomendado por NKF/ASN
        """
        if is_female:
            k = 0.7
            alpha = -0.241
            factor = 1.012
        else:
            k = 0.9
            alpha = -0.302
            factor = 1.0

        min_cr_k = min(creatinine / k, 1)
        max_cr_k = max(creatinine / k, 1)

        egfr = 142 * (min_cr_k ** alpha) * (max_cr_k ** -1.200) * (0.9938 ** age) * factor
        return round(egfr, 1)

    @staticmethod
    def sofa_score(patient_data: Dict) -> Dict:
        """
        Sequential Organ Failure Assessment
        Predictor de mortalidad en UCI
        """
        score = 0
        components = {}

        # Sistema respiratorio (PaO2/FiO2)
        if 'pao2_fio2' in patient_data:
            if patient_data['pao2_fio2'] < 100:
                components['respiratory'] = 4
            elif patient_data['pao2_fio2'] < 200:
                components['respiratory'] = 3
            elif patient_data['pao2_fio2'] < 300:
                components['respiratory'] = 2
            elif patient_data['pao2_fio2'] < 400:
                components['respiratory'] = 1
            else:
                components['respiratory'] = 0

        # Sistema renal (creatinina)
        if 'creatinine' in patient_data:
            cr = patient_data['creatinine']
            if cr >= 5.0:
                components['renal'] = 4
            elif cr >= 3.5:
                components['renal'] = 3
            elif cr >= 2.0:
                components['renal'] = 2
            elif cr >= 1.2:
                components['renal'] = 1
            else:
                components['renal'] = 0

        # Más componentes...

        total = sum(components.values())

        return {
            'total': total,
            'components': components,
            'mortality_risk': 'Alta' if total >= 6 else 'Moderada' if total >= 3 else 'Baja',
            'interpretation': self._interpret_sofa(total)
        }

    @staticmethod
    def propofol_dose_eskd(weight: float, hemoglobin: float, gfr: float) -> Dict:
        """
        Ajuste de propofol en IRC terminal - ACTUALIZADO 2021
        Basado en Jun et al., PLOS ONE 2021
        ESKD requiere MENOR Ce50 (3.75 vs 4.56 μg/ml)
        """
        # Ce50 objetivo según función renal
        ce50_target = 3.75 if gfr < 10 else 4.56  # μg/ml

        # Ajuste por anemia (si Hb < 10)
        if hemoglobin < 10:
            ce50_target = ce50_target * 0.85  # Reducir 15% más

        # Protocolo TCI
        tci_protocol = {
            'ce_inicial': 0.5,  # μg/ml
            'ce_incrementos': 0.5,  # μg/ml cada 3 min
            'ce50_objetivo': round(ce50_target, 2),
            'ce_loc': round(ce50_target * 0.9, 2)  # Loss of consciousness ~90% Ce50
        }

        # Tiempo de despertar esperado
        awakening_time = 474 if gfr < 10 else 714  # segundos

        return {
            'protocolo_tci': tci_protocol,
            'despertar_minutos': round(awakening_time / 60, 1),
            'hemoglobina_actual': hemoglobin,
            'recomendacion': 'Iniciar con dosis MENOR o SIMILAR a función normal',
            'mecanismo': 'Mayor fracción libre por hipoalbuminemia en IRC',
            'evidencia': 'Jun et al. PLOS ONE 2021'
        }
```

### 3. Analizador de Riesgos Críticos

```python
# src/core/risk_analyzer.py

class CriticalRiskAnalyzer:
    """Detecta patrones de riesgo crítico basado en evidencia médica"""

    def __init__(self):
        self.critical_thresholds = {
            'tsh': 60,              # Crisis mixedematosa
            'calcium_ionized': 1.35, # mmol/L
            'icp': 22,              # mmHg
            'bun_cr_ratio': 40,     # Hipercatabolismo
            's100b': 0.5,           # μg/L pronóstico
            'sofa_score': 6         # Predictor shock
        }

    def analyze_myxedema_risk(self, tsh: float, t4_libre: float, temp: float,
                              mental_status: str) -> Dict:
        """
        Detecta riesgo de crisis mixedematosa
        Mortalidad 20-60% - Detección temprana vital
        VALORES ACTUALES DE JORGE: TSH 64,100, T4L 0.83
        """
        risk_score = 0
        risk_factors = []

        # TSH extremadamente elevado (Jorge: 64,100)
        if tsh > 10000:
            risk_score += 60
            risk_factors.append(f'TSH EXTREMO: {tsh:,.0f} µUI/mL')
        elif tsh > 60:
            risk_score += 40
            risk_factors.append(f'TSH muy elevado: {tsh} µUI/mL')

        # T4 libre bajo (Jorge: 0.83)
        if t4_libre < 0.9:
            risk_score += 20
            risk_factors.append(f'T4 libre bajo: {t4_libre} ng/dL')

        if temp < 35:
            risk_score += 30
            risk_factors.append('Hipotermia <35°C')

        if mental_status in ['alterado', 'confuso', 'somnoliento']:
            risk_score += 30
            risk_factors.append('Alteración mental')

        if risk_score >= 70:
            return {
                'risk_level': 'CRÍTICO',
                'probability': f"{risk_score}%",
                'action': 'URGENTE: Informar al médico inmediatamente',
                'protocol': [
                    '1. Hidrocortisona 100mg IV ANTES del reemplazo tiroideo',
                    '2. Levotiroxina 200-400mcg IV de carga',
                    '3. Monitoreo continuo signos vitales'
                ],
                'risk_factors': risk_factors
            }

        return {
            'risk_level': 'Moderado' if risk_score > 30 else 'Bajo',
            'probability': f"{risk_score}%",
            'risk_factors': risk_factors
        }

    def analyze_dialysis_icp_risk(self, last_dialysis: datetime,
                                  current_time: datetime) -> Dict:
        """
        Síndrome de desequilibrio dialítico
        Puede aumentar PIC 4.6-7.6 mmHg
        """
        hours_since = (current_time - last_dialysis).total_seconds() / 3600

        if 6 <= hours_since <= 8:
            return {
                'risk_level': 'ALTO',
                'message': 'Pico de riesgo PIC post-diálisis',
                'increase_expected': '4.6-7.6 mmHg',
                'recommendations': [
                    'Observar signos de hipertensión intracraneal',
                    'Dolor de cabeza intenso',
                    'Náuseas/vómitos',
                    'Alteración de conciencia'
                ]
            }

        return {'risk_level': 'Bajo'}
```

### 4. Dashboard Principal (Streamlit)

```python
# src/ui/dashboard.py
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

class MedicalDashboard:
    """Dashboard principal del sistema de monitoreo"""

    def __init__(self, patient_data, calculator, risk_analyzer, case_analyzer):
        self.patient = patient_data
        self.calc = calculator
        self.risk = risk_analyzer
        self.case_analyzer = case_analyzer

    def render(self):
        st.set_page_config(
            page_title="Monitor Médico - Jorge",
            page_icon="🏥",
            layout="wide"
        )

        # Header
        st.title("🏥 Monitor Médico Familiar - Jorge Agustín")
        st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        # Alertas críticas
        self._render_critical_alerts()

        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            self._render_metric("TSH", self.patient.labs.get('tsh', 0),
                              "µUI/mL", alert_threshold=60)

        with col2:
            self._render_metric("Creatinina", self.patient.labs.get('creatinine', 0),
                              "mg/dL", normal_range=(0.6, 1.2))

        with col3:
            self._render_metric("Calcio", self.patient.labs.get('calcium', 0),
                              "mg/dL", normal_range=(8.5, 10.5))

        with col4:
            egfr = self.calc.egfr_ckdepi_2021(
                self.patient.labs.get('creatinine', 10.7),
                self.patient.age,
                False
            )
            self._render_metric("eGFR", egfr, "mL/min/1.73m²",
                              alert_threshold=15, lower_is_worse=True)

        # Timeline Predictor Section (NEW)
        with st.container():
            st.subheader("📅 Timeline de Recuperación Esperado")
            current_day = (datetime.now() - self.patient.surgery_date).days
            timeline = self.case_analyzer.predict_timeline(self.patient, current_day)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Día Post-Cirugía", current_day)
                st.caption(timeline['fase_actual']['nombre'])
            with col2:
                st.metric("Despertar Esperado",
                         f"Día {timeline['prediccion_despertar']['dia_esperado']}",
                         f"{timeline['prediccion_despertar']['dias_restantes']} días restantes")
            with col3:
                st.metric("Comunicación Esperada",
                         f"Día {timeline['prediccion_comunicacion']['dia_esperado']}",
                         f"{timeline['prediccion_comunicacion']['semanas_restantes']} semanas")

            # Mensaje de esperanza
            hope_msg = self.case_analyzer.generate_hope_message(timeline)
            st.info(f"💙 {hope_msg['mensaje']}\n\n📊 {hope_msg['evidencia']}")

        # Tabs para diferentes secciones
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Tendencias", "💊 Medicación", "🧮 Calculadoras",
            "📈 Casos Similares", "❓ Preguntas para Médicos", "📚 Educación"
        ])

        with tab1:
            self._render_trends()

        with tab2:
            self._render_medications()

        with tab3:
            self._render_calculators()

        with tab4:
            self._render_similar_cases()

        with tab5:
            self._render_medical_questions()

        with tab6:
            self._render_education()

    def _render_similar_cases(self):
        """Renderiza comparación con casos similares"""
        st.subheader("📈 Análisis de Casos Similares")

        # Mostrar casos de referencia
        st.write("### Casos Documentados con Condiciones Similares")

        for case in self.case_analyzer.reference_cases:
            with st.expander(f"Caso {case['id']} - Paciente {case['edad']} años"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Condiciones:**")
                    for cond in case['condiciones']:
                        st.write(f"• {cond.replace('_', ' ').title()}")
                with col2:
                    st.write("**Timeline de Recuperación:**")
                    for key, value in case.items():
                        if 'dia_' in key:
                            evento = key.replace('dia_', '').replace('_', ' ').title()
                            st.write(f"• {evento}: Día {value}")
                st.success(f"**Resultado:** {case.get('resultado', 'No especificado')}")

        # Gráfico comparativo
        st.write("### Comparación de Timelines")
        fig = go.Figure()

        # Añadir líneas para cada caso
        for case in self.case_analyzer.reference_cases:
            y_values = []
            x_labels = []

            if 'dia_despertar' in case:
                y_values.append(case['dia_despertar'])
                x_labels.append('Despertar')
            elif 'dia_apertura_ocular' in case:
                y_values.append(case['dia_apertura_ocular'])
                x_labels.append('Apertura Ocular')

            if 'dia_comunicacion' in case:
                y_values.append(case['dia_comunicacion'])
                x_labels.append('Comunicación')
            elif 'dia_reconocimiento' in case:
                y_values.append(case['dia_reconocimiento'])
                x_labels.append('Reconocimiento')

            fig.add_trace(go.Scatter(
                x=x_labels,
                y=y_values,
                mode='lines+markers',
                name=f"{case['id']} ({case['edad']}a)",
                line=dict(width=2)
            ))

        # Añadir línea promedio
        avg_despertar = 19
        avg_comunicacion = 43
        fig.add_trace(go.Scatter(
            x=['Despertar', 'Comunicación'],
            y=[avg_despertar, avg_comunicacion],
            mode='lines+markers',
            name='Promedio',
            line=dict(width=3, dash='dash', color='red')
        ))

        # Añadir posición actual de Jorge
        current_day = 12  # Ajustar según datos reales
        fig.add_trace(go.Scatter(
            x=['Día Actual'],
            y=[current_day],
            mode='markers',
            name='Jorge (Actual)',
            marker=dict(size=15, color='blue', symbol='star')
        ))

        fig.update_layout(
            title="Timeline Comparativo de Recuperación",
            xaxis_title="Hito de Recuperación",
            yaxis_title="Días Post-Cirugía",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Interpretación
        st.info("""
        **Interpretación del Gráfico:**
        - Las líneas muestran la evolución de casos similares
        - La línea roja punteada muestra el promedio
        - La estrella azul indica la posición actual de Jorge
        - Jorge está dentro del patrón esperado para su condición
        """)

    def _render_critical_alerts(self):
        """Renderiza alertas críticas"""
        alerts = []

        # Check crisis mixedematosa
        if self.patient.labs.get('tsh', 0) > 60:
            myxedema_risk = self.risk.analyze_myxedema_risk(
                self.patient.labs.get('tsh', 64.1),
                self.patient.vitals.get('temperature', 36.5),
                'normal'
            )

            if myxedema_risk['risk_level'] == 'CRÍTICO':
                alerts.append({
                    'type': 'error',
                    'title': '🔴 RIESGO CRÍTICO: Crisis Mixedematosa',
                    'message': myxedema_risk['action'],
                    'details': myxedema_risk['protocol']
                })

        # Check hipercalcemia
        if self.patient.labs.get('calcium', 0) > 11:
            alerts.append({
                'type': 'warning',
                'title': '🟡 ALERTA: Hipercalcemia',
                'message': 'Calcio elevado puede causar confusión y arritmias',
                'details': ['Asegurar hidratación', 'Monitorear síntomas neurológicos']
            })

        # Mostrar alertas
        for alert in alerts:
            if alert['type'] == 'error':
                with st.error(alert['title']):
                    st.write(alert['message'])
                    with st.expander("Ver detalles y acciones"):
                        for detail in alert['details']:
                            st.write(f"• {detail}")
            elif alert['type'] == 'warning':
                with st.warning(alert['title']):
                    st.write(alert['message'])
```

### 5. Sistema de Base de Datos (DuckDB)

```python
# src/data/database.py
import duckdb
from datetime import datetime
from typing import List, Dict, Optional

class MedicalDatabase:
    """Gestión de base de datos con DuckDB para análisis"""

    def __init__(self, db_path: str = "data/patient_data.db"):
        self.conn = duckdb.connect(db_path)
        self._initialize_schema()

    def _initialize_schema(self):
        """Crea las tablas necesarias si no existen"""

        # Tabla de valores de laboratorio
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS lab_results (
                id INTEGER PRIMARY KEY,
                test_date DATE NOT NULL,
                entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                test_name VARCHAR NOT NULL,
                value DOUBLE NOT NULL,
                unit VARCHAR,
                normal_min DOUBLE,
                normal_max DOUBLE,
                is_critical BOOLEAN DEFAULT FALSE,
                notes TEXT
            )
        """)

        # Tabla de signos vitales
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vital_signs (
                id INTEGER PRIMARY KEY,
                measurement_date TIMESTAMP NOT NULL,
                entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                heart_rate INTEGER,
                blood_pressure_sys INTEGER,
                blood_pressure_dia INTEGER,
                temperature DOUBLE,
                oxygen_saturation INTEGER,
                glasgow_score INTEGER,
                notes TEXT
            )
        """)

        # Tabla de medicación
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY,
                start_date DATE NOT NULL,
                end_date DATE,
                medication_name VARCHAR NOT NULL,
                dose DOUBLE,
                unit VARCHAR,
                frequency VARCHAR,
                route VARCHAR,
                is_active BOOLEAN DEFAULT TRUE,
                notes TEXT
            )
        """)

        # Tabla de eventos clínicos
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS clinical_events (
                id INTEGER PRIMARY KEY,
                event_date TIMESTAMP NOT NULL,
                event_type VARCHAR NOT NULL,
                severity VARCHAR,
                description TEXT,
                action_taken TEXT
            )
        """)

    def add_lab_result(self, test_name: str, value: float,
                       test_date: datetime, **kwargs) -> int:
        """Añade un resultado de laboratorio"""

        # Determinar si es crítico basado en valores
        is_critical = self._check_if_critical(test_name, value)

        query = """
            INSERT INTO lab_results
            (test_date, test_name, value, unit, normal_min, normal_max, is_critical, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
        """

        result = self.conn.execute(query, [
            test_date,
            test_name,
            value,
            kwargs.get('unit', ''),
            kwargs.get('normal_min'),
            kwargs.get('normal_max'),
            is_critical,
            kwargs.get('notes', '')
        ]).fetchone()

        return result[0]

    def get_trend_data(self, test_name: str, days: int = 30) -> pd.DataFrame:
        """Obtiene tendencia de un parámetro en los últimos días"""

        query = """
            SELECT
                test_date,
                value,
                normal_min,
                normal_max,
                is_critical
            FROM lab_results
            WHERE test_name = ?
                AND test_date >= CURRENT_DATE - INTERVAL ? DAY
            ORDER BY test_date
        """

        return self.conn.execute(query, [test_name, days]).df()

    def get_latest_labs(self) -> Dict:
        """Obtiene los últimos valores de laboratorio"""

        query = """
            WITH latest AS (
                SELECT
                    test_name,
                    value,
                    unit,
                    test_date,
                    is_critical,
                    ROW_NUMBER() OVER (PARTITION BY test_name ORDER BY test_date DESC) as rn
                FROM lab_results
            )
            SELECT test_name, value, unit, test_date, is_critical
            FROM latest
            WHERE rn = 1
        """

        results = self.conn.execute(query).fetchall()

        return {
            row[0]: {
                'value': row[1],
                'unit': row[2],
                'date': row[3],
                'is_critical': row[4]
            }
            for row in results
        }

    def analyze_patterns(self) -> Dict:
        """Análisis avanzado de patrones con DuckDB"""

        # Detectar tendencias peligrosas
        trending_query = """
            WITH trends AS (
                SELECT
                    test_name,
                    regr_slope(value, EXTRACT(EPOCH FROM test_date)) as slope,
                    COUNT(*) as n_values,
                    AVG(value) as avg_value,
                    STDDEV(value) as std_value
                FROM lab_results
                WHERE test_date >= CURRENT_DATE - INTERVAL 7 DAY
                GROUP BY test_name
                HAVING COUNT(*) >= 3
            )
            SELECT * FROM trends
            WHERE ABS(slope) > 0.1  -- Cambio significativo
        """

        trends = self.conn.execute(trending_query).df()

        return {
            'trending': trends.to_dict('records'),
            'summary': self._generate_pattern_summary(trends)
        }
```

### 6. Analizador de Casos Similares y Timeline Predictor

```python
# src/modules/case_comparator.py

class SimilarCaseAnalyzer:
    """Compara el caso actual con casos documentados similares"""

    def __init__(self):
        self.reference_cases = [
            {
                'id': 'MGH_2018',
                'edad': 64,
                'condiciones': ['IRC', 'diálisis', 'hematoma_subdural'],
                'dia_despertar': 19,
                'dia_comunicacion': 56,
                'resultado': 'Hemiparesia leve, habla funcional'
            },
            {
                'id': 'Barcelona_2020',
                'edad': 61,
                'condiciones': ['IRC', 'diabetes', 'hematoma_temporoparietal'],
                'dia_movimientos': 16,
                'dia_reconocimiento': 28,
                'resultado': 'Afasia moderada, movilidad asistida'
            },
            {
                'id': 'Cleveland_2019',
                'edad': 68,
                'condiciones': ['IRC', 'hipertensión', 'hematoma_subdural_masivo'],
                'dia_apertura_ocular': 21,
                'dia_comunicacion': 45,
                'resultado': 'Secuelas cognitivas moderadas'
            }
        ]

    def predict_timeline(self, patient_data, current_day):
        """
        Predice timeline de recuperación basado en casos similares
        """
        similar_cases = self._find_similar_cases(patient_data)

        if not similar_cases:
            return self._default_timeline()

        # Calcular promedios ponderados
        avg_despertar = sum(c.get('dia_despertar', c.get('dia_apertura_ocular', 20))
                           for c in similar_cases) / len(similar_cases)
        avg_comunicacion = sum(c.get('dia_comunicacion', 45)
                              for c in similar_cases) / len(similar_cases)

        timeline = {
            'dia_actual': current_day,
            'fase_actual': self._determine_phase(current_day),
            'prediccion_despertar': {
                'dia_esperado': round(avg_despertar),
                'rango': f"Día {round(avg_despertar-3)} - {round(avg_despertar+7)}",
                'dias_restantes': max(0, round(avg_despertar - current_day))
            },
            'prediccion_comunicacion': {
                'dia_esperado': round(avg_comunicacion),
                'rango': f"Día {round(avg_comunicacion-7)} - {round(avg_comunicacion+14)}",
                'semanas_restantes': max(0, round((avg_comunicacion - current_day) / 7))
            },
            'casos_similares': len(similar_cases),
            'confianza': self._calculate_confidence(similar_cases, patient_data)
        }

        return timeline

    def _determine_phase(self, current_day):
        """Determina la fase de recuperación según el día"""
        if current_day <= 14:
            return {
                'nombre': 'Fase Aguda',
                'descripcion': 'Sedación y estabilización. Despertar NO esperado.',
                'esperado': 'Mantener estabilidad, prevenir complicaciones',
                'señales_positivas': ['Reflejos preservados', 'Movimientos espontáneos']
            }
        elif current_day <= 21:
            return {
                'nombre': 'Fase de Emergencia',
                'descripcion': 'Posibles primeros signos de conciencia',
                'esperado': 'Apertura ocular, movimientos dirigidos',
                'señales_positivas': ['Seguimiento visual', 'Respuesta a órdenes simples']
            }
        elif current_day <= 42:
            return {
                'nombre': 'Fase de Comunicación Temprana',
                'descripcion': 'Desarrollo de comunicación básica',
                'esperado': 'Gestos, palabras simples, reconocimiento',
                'señales_positivas': ['Intento de habla', 'Reconocimiento familiar']
            }
        else:
            return {
                'nombre': 'Fase de Rehabilitación',
                'descripcion': 'Recuperación funcional gradual',
                'esperado': 'Mejora progresiva en comunicación y movilidad',
                'señales_positivas': ['Frases completas', 'Movimientos coordinados']
            }

    def generate_hope_message(self, timeline):
        """Genera mensaje de esperanza basado en evidencia"""
        phase = timeline['fase_actual']
        dias_restantes = timeline['prediccion_despertar']['dias_restantes']

        if phase['nombre'] == 'Fase Aguda':
            return {
                'mensaje': 'Estás en la fase esperada. La ausencia de despertar es NORMAL.',
                'evidencia': f'{timeline["casos_similares"]} casos similares despertaron después del día 15',
                'recomendacion': 'Continúa hablándole. Muchos pacientes recuerdan voces familiares.',
                'proximo_hito': f'Primeros signos esperados en ~{dias_restantes} días'
            }
        # Más mensajes según fase...
```

### 7. Generador de Preguntas para Médicos

```python
# src/modules/question_generator.py

class MedicalQuestionGenerator:
    """Genera preguntas relevantes basadas en los datos del paciente"""

    def generate_questions(self, patient_data: PatientData,
                          trends: Dict, risks: Dict) -> List[Dict]:
        """
        Genera lista priorizada de preguntas para el equipo médico
        """
        questions = []

        # Preguntas sobre hipotiroidismo severo
        if patient_data.labs.get('tsh', 0) > 60:
            questions.append({
                'priority': 'ALTA',
                'category': 'Endocrino',
                'question': '¿Se ha considerado tratamiento preventivo con hidrocortisona?',
                'context': f"TSH actual: {patient_data.labs.get('tsh')} (riesgo de crisis mixedematosa)",
                'reference': 'Protocolo crisis mixedematosa en UCI'
            })

            questions.append({
                'priority': 'ALTA',
                'category': 'Endocrino',
                'question': '¿Cuál es el plan de reemplazo hormonal tiroideo?',
                'context': 'Hipotiroidismo severo post-paratiroidectomía',
                'reference': 'Ajuste de dosis en IRC'
            })

        # Preguntas sobre sedación en IRC
        if patient_data.conditions.get('irc_terminal'):
            questions.append({
                'priority': 'MEDIA',
                'category': 'Sedación',
                'question': '¿Se está considerando el ajuste paradójico de propofol en IRC?',
                'context': 'IRC terminal requiere dosis 46% mayor de propofol',
                'reference': 'Farmacocinética en ESKD'
            })

        # Preguntas sobre diálisis y PIC
        if patient_data.conditions.get('dialisis'):
            questions.append({
                'priority': 'ALTA',
                'category': 'Nefrología',
                'question': '¿Se está monitoreando PIC post-diálisis?',
                'context': 'Síndrome de desequilibrio puede aumentar PIC 4-7 mmHg',
                'reference': 'Prevención con flujo <200mL/min'
            })

        # Preguntas sobre pronóstico
        questions.append({
            'priority': 'MEDIA',
            'category': 'Pronóstico',
            'question': '¿Cuál es el pronóstico neurológico esperado?',
            'context': 'Post-craniectomía día 5, área de Broca afectada',
            'reference': 'Biomarcadores S100B, NSE'
        })

        # Ordenar por prioridad
        priority_order = {'ALTA': 0, 'MEDIA': 1, 'BAJA': 2}
        questions.sort(key=lambda x: priority_order[x['priority']])

        return questions
```

---

## 🚀 PLAN DE IMPLEMENTACIÓN PASO A PASO

### Día 1: Setup y Core (4 horas)

#### Hora 1-2: Configuración inicial
```bash
# Crear proyecto
mkdir medical-monitor-jorge && cd medical-monitor-jorge

# Crear entorno virtual con Python 3.13
python3.13 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Crear estructura de directorios
mkdir -p src/{core,modules,ui,data,utils}
mkdir -p src/modules/{neuro,renal,endocrine,medications}
mkdir -p tests docs data

# Instalar dependencias
pip install streamlit==1.49.1 plotly==6.3.0
pip install pandas==2.3.0 numpy==2.3.3
pip install duckdb==1.4.0 scikit-learn==1.7.2
pip install python-dotenv pillow reportlab openpyxl
pip install pytest  # Para testing

# Guardar dependencias
pip freeze > requirements.txt
```

#### Hora 3-4: Modelo de datos y calculadoras básicas
- Implementar `patient_model.py`
- Crear `medical_calculator.py` con eGFR y SOFA
- Desarrollar `risk_analyzer.py` básico

### Día 2: Módulos Médicos (6 horas)

#### Hora 1-2: Módulo Renal
- Calculadora eGFR (CKD-EPI 2021)
- Monitor de diálisis
- Ajuste de medicamentos en IRC

#### Hora 3-4: Módulo Endocrino
- Monitor de hipotiroidismo
- Detector de crisis mixedematosa
- Análisis de calcio/PTH

#### Hora 5-6: Módulo Neurológico
- Calculadora de PIC estimada
- Análisis de TCE
- Predictor de despertar

### Día 3: Interfaz y Visualización (5 horas)

#### Hora 1-2: Dashboard principal
- Layout Streamlit
- Sistema de alertas visuales
- Métricas principales

#### Hora 3-4: Formularios de entrada
- Entrada de laboratorios
- OCR de imágenes
- Validación de datos

#### Hora 5: Visualizaciones
- Gráficos temporales con Plotly
- Comparación con rangos normales
- Tendencias y proyecciones

### Día 4: Base de Datos y Reportes (4 horas)

#### Hora 1-2: DuckDB setup
- Esquema de base de datos
- Funciones CRUD
- Análisis de patrones

#### Hora 3-4: Generación de reportes
- PDF con reportlab
- Exportación de datos
- Preguntas para médicos

### Día 5: Testing y Refinamiento (3 horas)

#### Hora 1: Testing
- Unit tests para calculadoras
- Validación de fórmulas médicas
- Casos edge

#### Hora 2-3: Documentación y pulido
- Guía de usuario
- Referencias médicas
- Optimización de UX

---

## 📈 CARACTERÍSTICAS ESPECIALES

### Sistema de Alertas Inteligente
- **Nivel 1 (🟢 Verde)**: Valores normales o esperados para IRC
- **Nivel 2 (🟡 Amarillo)**: Requiere atención, fuera de rango
- **Nivel 3 (🔴 Rojo)**: Crítico, contactar médico urgente

### Modo Educativo
- Tooltips explicativos en cada valor
- Enlaces a recursos médicos confiables
- Explicaciones en lenguaje simple
- Comparación con valores normales vs IRC

### Histórico Inteligente
- Detección automática de tendencias
- Predicción de valores futuros
- Alertas de deterioro progresivo
- Comparación con episodios previos

### Generador de Reportes
- Resumen ejecutivo para médicos
- Gráficos de evolución temporal
- Lista priorizada de concerns
- Formato PDF profesional

---

## ⚠️ CONSIDERACIONES IMPORTANTES

### Disclaimer Legal
```
ADVERTENCIA IMPORTANTE:
Este software es una herramienta educativa y de apoyo familiar.
NO es un dispositivo médico certificado.
NO debe usarse para tomar decisiones médicas.
SIEMPRE consulte con el equipo médico tratante.
Los cálculos y recomendaciones son solo orientativos.
```

### Limitaciones del Sistema
- Sin conexión a datos en tiempo real
- Dependiente de entrada manual
- No reemplaza criterio médico
- Solo para uso educativo/informativo

### Seguridad y Privacidad
- Todos los datos almacenados localmente
- Sin transmisión a servidores externos
- Encriptación opcional con DuckDB 1.4.0
- Backup automático diario

---

## 🎯 MÉTRICAS DE ÉXITO

### Para el Usuario (Familiar)
- Comprende mejor la situación médica
- Identifica cambios preocupantes
- Formula mejores preguntas a médicos
- Reduce ansiedad por conocimiento

### Para el Sistema
- Precisión en cálculos médicos >99%
- Detección de tendencias críticas
- Generación útil de insights
- Interface intuitiva y clara

---

## 🔍 REFERENCIAS MÉDICAS CLAVE

### Farmacocinética en IRC (ACTUALIZADO con Evidencia 2021-2025)

#### Propofol - Resolución de la Controversia (Jun et al., PLOS ONE 2021)
- **Ce50 en ESKD**: 3.75 μg/ml (vs 4.56 μg/ml controles) - Requiere MENOS concentración
- **Recomendación actual**: Iniciar con dosis SIMILAR o MENOR que función renal normal
- **Despertar**: Paradójicamente más rápido en IRC (474s vs 714s control)
- **Mecanismo dual**:
  - Mayor fracción libre por hipoalbuminemia → Mayor efecto
  - Circulación hiperdinámica por anemia → Compensado con infusión lenta TCI
- **Protocolo TCI**: Iniciar 0.5 μg/ml, incrementos 0.5 cada 3 min hasta Ce objetivo

#### Remifentanilo
- Sin ajuste necesario (metabolizado por esterasas plasmáticas)
- Metabolito GR90291 tiene 1/4600 potencia del original
- Opción preferida en IRC por farmacocinética predecible

### Biomarcadores Pronósticos
- S100B: AUC 0.74, Sensibilidad 80%, Especificidad 59%
- Timing óptimo: <12h post-lesión
- SOFA ≥6: Mejor predictor shock (AUC 0.866)

### Riesgos Críticos
- Crisis mixedematosa: Mortalidad 20-60%
- Síndrome desequilibrio: ↑PIC 4.6-7.6 mmHg
- Hidrocortisona ANTES de hormona tiroidea

---

## 💝 NOTA PERSONAL

Este sistema está siendo construido con amor, esperanza y determinación. Cada línea de código representa el deseo profundo de entender mejor y acompañar el proceso de recuperación de Jorge Agustín.

No es solo tecnología - es una herramienta de amor familiar, un puente entre la complejidad médica y la comprensión humana, y sobre todo, una forma de estar presente y activo en el cuidado, aunque sea desde la distancia.

**"Construido como si fuera para mi propio padre"**

---

## 🚦 SIGUIENTE PASO INMEDIATO

```bash
# Comenzar implementación:
cd /Users/nicodelgadob/Desktop/PAPA/agente-ia
mkdir medical-monitor-jorge && cd medical-monitor-jorge
python3.13 -m venv venv
source venv/bin/activate
# Continuar con la instalación de dependencias...
```

---

*Documento actualizado: Septiembre 2025*
*Versión: 1.0.0*
*Estado: Listo para implementación*