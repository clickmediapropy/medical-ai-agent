# 🚨 PROMPT PARA CLAUDE CODE: CONSTRUCCIÓN DE AGENTE MÉDICO IA CRÍTICO

## CONTEXTO DE EMERGENCIA MÉDICA

Necesito que construyas **URGENTEMENTE** un sistema de inteligencia artificial médica ultra-especializado para monitorear y predecir complicaciones en mi padre, quien está en UCI con una situación médica extremadamente compleja y crítica. Cada hora cuenta, y este sistema puede literalmente salvar su vida detectando patrones que los médicos podrían pasar por alto.

### 📋 SITUACIÓN ACTUAL DEL PACIENTE (14 Sept 2025, 14:00)

**Identificación:** Jorge Agustín Delgado Puentes, 65 años, UCI Sanatorio La Costa
**Estado:** CRÍTICO - Post-craniectomía descompresiva día 5, traqueostomía programada mañana

**Condiciones concurrentes críticas:**
1. **IRC Terminal**: 6% función renal, diálisis 3x/semana, fístula AV dañada
2. **TCE Severo**: Hematoma intracerebral 20cm³ + subdural, área Broca afectada
3. **Hipotiroidismo Severo**: TSH 64.100 µUI/mL (RIESGO CRISIS MIXEDEMATOSA)
4. **Hipercalcemia Paradójica**: 11.5 mg/dL con síndrome hueso hambriento
5. **Sedación**: Propofol + Remifentanilo (reducción 67% = despertar cercano)
6. **Complicación vascular**: Brazo izquierdo edematizado

### ⚠️ RIESGOS INMINENTES (próximas 48-72h)

```
🔴 CRÍTICO - ACTUAR YA:
- Crisis mixedematosa (mortalidad 20-60%)
- Síndrome infusión propofol + IRC
- Hidrocefalia post-craniectomía
- Síndrome desequilibrio dialítico → ↑PIC

🟡 ALTO RIESGO (3-7 días):
- Infección nosocomial post-traqueostomía
- Delirium del despertar
- Crisis hipercalcémica
```

## 🎯 REQUERIMIENTOS DEL SOFTWARE

### ARQUITECTURA CORE - PRIORIDAD MÁXIMA

```python
# ESTRUCTURA BÁSICA REQUERIDA
medical_ai_agent/
├── core/
│   ├── patient_monitor.py      # Monitoreo tiempo real
│   ├── risk_predictor.py       # Predicción 24-48h
│   ├── alert_system.py         # Alertas críticas
│   └── drug_interactions.py    # Interacciones farmacológicas
├── modules/
│   ├── neuro/                  # TCE, PIC, edema
│   ├── renal/                  # IRC, diálisis, clearance
│   ├── endocrine/              # Tiroides, calcio, PTH
│   └── critical_care/          # Sedación, ventilación
├── ml_models/
│   ├── lstm_attention.py       # Predicción temporal
│   ├── random_forest.py        # Mortalidad
│   ├── isolation_forest.py     # Anomalías
│   └── explainers.py          # LIME/SHAP
├── data/
│   ├── loaders/                # CSV, PDF, DICOM
│   ├── processors/             # Normalización
│   └── storage/                # SQLite DB
├── api/
│   ├── fhir_client.py         # Integración hospitalaria
│   ├── drugbank_api.py        # Interacciones
│   └── realtime_stream.py     # WebSocket monitoring
└── ui/
    ├── dashboard.py            # Streamlit/Gradio
    └── reports.py              # Generación PDF
```

### MÓDULO 1: SISTEMA DE ALERTA TEMPRANA [CRÍTICO]

```python
class CriticalAlertSystem:
    """
    DETECTAR ESTAS CRISIS 24-48H ANTES:
    - Crisis mixedematosa (TSH >60)
    - Acumulación propofol en IRC
    - Aumento PIC post-diálisis
    - Síndrome hueso hambriento
    """
    
    def __init__(self):
        self.critical_thresholds = {
            'tsh': 60,              # Crisis mixedematosa
            'calcium_ionized': 1.35, # mmol/L
            'icp': 22,              # mmHg
            'bun_cr_ratio': 40,     # Hipercatabolismo
            's100b': 0.5,           # μg/L pronóstico
            'sofa_score': 6         # Shock predictor
        }
        
    def detect_pattern(self, patient_data):
        """
        PATRONES NO OBVIOS A DETECTAR:
        1. IRC → Propofol acumulación → Despertar retardado
        2. Hipotiroidismo → Metabolismo -50% → Sedación prolongada
        3. Diálisis → Shift osmótico → ↑PIC 4-7 mmHg
        4. Anemia (Hb 8.3) → Hipoxia cerebral → Recuperación lenta
        """
```

### MÓDULO 2: PREDICTOR ML CON EVIDENCIA MÉDICA

```python
class ICUPredictor:
    """
    Basado en investigación 2024-2025:
    - LSTM-Attention: AUC 0.876 sepsis, 0.823 IAM
    - Random Forest: AUC 0.945 mortalidad
    - XGBoost: AUC 0.889 despertar
    """
    
    def build_models(self):
        # Modelo 1: Despertar neurológico
        self.awakening_model = self.create_awakening_predictor()
        # Factores: Propofol clearance + TSH + Edema + IRC
        
        # Modelo 2: Crisis mixedematosa
        self.myxedema_model = self.create_crisis_detector()
        # Signos: TSH>60 + Hipotermia + Alteración mental
        
        # Modelo 3: Complicaciones diálisis
        self.dialysis_model = self.create_dialysis_optimizer()
        # Balance: Flujo <200mL/min + Duración >4h + PIC
```

### MÓDULO 3: FARMACOCINÉTICA PERSONALIZADA

```python
class DrugKineticsIRC:
    """
    CRÍTICO: Ajustes en IRC terminal (TFG <10%)
    """
    
    def propofol_dosing(self, weight, hgb, gfr):
        """
        PARADOJA DOCUMENTADA:
        - ESKD requiere DOSIS 46% MAYOR (2.03 vs 1.39 mg/kg)
        - Despertar MÁS RÁPIDO (474s vs 714s)
        - Anemia aumenta requerimientos
        """
        base_dose = 2.03 if gfr < 10 else 1.39
        anemia_factor = 1 + (0.1 * (9 - hgb))  # Ajuste por Hb
        return weight * base_dose * anemia_factor
    
    def remifentanil_advantage(self):
        """
        MEJOR OPCIÓN EN IRC:
        - NO requiere ajuste dosis
        - Metabolito GR90291: potencia 1/4600
        """
        return "NO_ADJUSTMENT_NEEDED"
```

### MÓDULO 4: DASHBOARD MÉDICO EN TIEMPO REAL

```python
import streamlit as st
import plotly.graph_objects as go

class MedicalDashboard:
    """
    VISUALIZACIÓN CRÍTICA - Actualización cada 30 segundos
    """
    
    def render(self):
        # Panel 1: SEMÁFORO DE RIESGO
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔴 RIESGO CRISIS", "87%", "↑12%")
            st.warning("Crisis mixedematosa probable 48h")
        
        with col2:
            st.metric("🟡 DESPERTAR", "72h", "Optimista")
            st.info("Reducir Propofol 10% más")
        
        with col3:
            st.metric("🟢 INFECCIÓN", "Bajo", "Estable")
        
        # Panel 2: TENDENCIAS CRÍTICAS
        self.plot_critical_trends()
        
        # Panel 3: RECOMENDACIONES ACCIONABLES
        st.header("⚡ ACCIONES INMEDIATAS")
        st.error("""
        1. Solicitar T4 libre + cortisol URGENTE
        2. Preparar hidrocortisona 100mg
        3. Reducir flujo diálisis <200 mL/min
        4. Monitoreo PIC continuo post-diálisis
        """)
```

### MÓDULO 5: BIOMARCADORES PREDICTIVOS

```python
class BiomarkerAnalyzer:
    """
    Evidencia 2024: S100B supera NSE consistentemente
    """
    
    def neurological_prognosis(self, s100b, nse, gfap):
        """
        S100B: AUC 0.74, Sens 80%, Spec 59%
        Timing óptimo: <12h post-lesión
        Combinación S100B+NSE+GFAP mejora precisión
        """
        if s100b > 0.5:  # μg/L
            risk_score = 0.7
            if nse > 17:  # μg/L
                risk_score += 0.2
            if gfap > 0.08:  # ng/mL
                risk_score += 0.1
            return {
                'mortality_risk': risk_score,
                'confidence': 0.82,
                'recommendation': 'Intensificar neuroprotección'
            }
```

### MÓDULO 6: INTEGRACIÓN HOSPITALARIA

```python
class HospitalIntegration:
    """
    Conexión con sistemas hospitalarios
    """
    
    def __init__(self):
        # FHIR para historia clínica
        self.fhir = FHIRClient({'api_base': 'https://hospital.fhir/r4'})
        
        # HL7 para laboratorios
        self.hl7_parser = HL7Parser()
        
        # DICOM para neuroimagen
        self.dicom_processor = DICOMProcessor()
        
        # DrugBank para interacciones
        self.drug_api = DrugBankAPI(api_key=DRUGBANK_KEY)
```

## 📊 DATOS DE ENTRADA REQUERIDOS

### Formato esperado (CSV/JSON):
```json
{
  "timestamp": "2025-09-14T14:00:00",
  "vitals": {
    "hr": 78, "bp": "130/80", "temp": 36.5,
    "spo2": 98, "glasgow": 8
  },
  "labs": {
    "creatinine": 10.7, "urea": 173, "hgb": 8.3,
    "tsh": 64.1, "calcium": 11.5, "phosphorus": 5.2,
    "s100b": 0.45, "nse": 15.2
  },
  "medications": {
    "propofol": {"dose": 150, "rate": "mg/h"},
    "remifentanil": {"dose": 0.1, "rate": "mcg/kg/min"}
  },
  "dialysis": {
    "last_session": "2025-09-14T08:00:00",
    "ultrafiltration": 2.5, "kt_v": 1.3
  }
}
```

## 🚀 INSTRUCCIONES DE CONSTRUCCIÓN PASO A PASO

### PASO 1: Setup inicial (5 minutos)
```bash
# Crear estructura y ambiente
mkdir medical_ai_jorge && cd medical_ai_jorge
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Instalar dependencias críticas
pip install pandas numpy scikit-learn xgboost
pip install torch tensorflow  # para LSTM
pip install streamlit plotly
pip install lime shap
pip install lifelines scikit-survival
pip install fhirclient hl7apy pydicom
```

### PASO 2: Core del sistema (30 minutos)
1. Implementar `patient_monitor.py` con clase base
2. Crear `risk_predictor.py` con modelos ML
3. Desarrollar `alert_system.py` con umbrales críticos
4. Construir `drug_interactions.py` con ajustes IRC

### PASO 3: Módulos especializados (45 minutos)
1. **Neuro**: Predictor PIC, edema, hidrocefalia
2. **Renal**: Optimizador diálisis, clearance drogas
3. **Endocrino**: Detector crisis mixedematosa
4. **UCI**: Predictor despertar, weaning

### PASO 4: Machine Learning (60 minutos)
1. LSTM-Attention para series temporales
2. Random Forest para mortalidad
3. Isolation Forest para anomalías
4. LIME/SHAP para explicabilidad

### PASO 5: Dashboard (30 minutos)
1. Streamlit con actualización real-time
2. Gráficos Plotly interactivos
3. Sistema de alertas visuales
4. Exportación de reportes PDF

### PASO 6: Testing y validación (30 minutos)
1. Cargar datos históricos
2. Simular escenarios críticos
3. Validar alertas y predicciones
4. Ajustar umbrales

## 🔥 FEATURES CRÍTICAS QUE SALVAN VIDAS

### 1. DETECTOR DE CRISIS MIXEDEMATOSA
```python
def detect_myxedema_crisis(tsh, temp, mental_status, cortisol=None):
    """
    MORTALIDAD 20-60% - DETECTAR TEMPRANO ES VITAL
    """
    if tsh > 60 and temp < 35 and mental_status == 'altered':
        return {
            'crisis_probability': 0.95,
            'action': 'HIDROCORTISONA 100mg INMEDIATO',
            'then': 'Levotiroxina 200-400mcg IV'
        }
```

### 2. OPTIMIZADOR DIÁLISIS-PIC
```python
def optimize_dialysis_for_icp(current_icp, weight, fluid_overload):
    """
    Prevenir síndrome desequilibrio (↑PIC 4-7 mmHg)
    """
    if current_icp > 20:
        return {
            'mode': 'CRRT',  # Continua mejor que intermitente
            'flow_rate': min(150, 200),  # mL/min
            'duration': '>4 hours',
            'prophylaxis': 'Manitol 0.5g/kg si diuresis residual'
        }
```

### 3. PREDICTOR DESPERTAR NEUROLÓGICO
```python
def predict_awakening(propofol_hours, gfr, tsh, edema_score):
    """
    Modelo multivariable personalizado
    """
    base_time = 48  # horas
    irc_factor = 1.5 if gfr < 10 else 1.0
    thyroid_factor = 1 + (tsh / 100)  # Metabolismo lento
    edema_factor = 1 + (edema_score * 0.2)
    
    predicted_hours = base_time * irc_factor * thyroid_factor * edema_factor
    return {
        'awakening_eta': f"{predicted_hours:.0f} horas",
        'confidence': 0.75,
        'optimize': 'Reducir Propofol 10-15% cada 12h'
    }
```

## 📈 MÉTRICAS DE ÉXITO

- **Detección crisis**: 24-48h anticipación (objetivo: 95% sensibilidad)
- **Predicción despertar**: Error <12 horas
- **Prevención complicaciones**: Reducir 30% eventos adversos
- **Adopción médica**: Dashboard usado cada 2 horas por equipo

## ⚠️ CONSIDERACIONES CRÍTICAS

### SEGURIDAD MÉDICA
- **NUNCA** sugerir cambios de medicación sin validación médica
- **SIEMPRE** mostrar nivel de confianza en predicciones
- **DOCUMENTAR** fuente de cada recomendación (paper, guía clínica)

### DATOS SENSIBLES
- Encriptar todo con AES-256
- No usar nombres reales en logs
- Cumplir HIPAA/GDPR
- Backup automático cada hora

### PERFORMANCE
- Latencia <100ms para alertas críticas
- Actualización dashboard cada 30 segundos
- Procesamiento paralelo para ML
- Cache de predicciones frecuentes

## 🆘 CÓDIGO DE EMERGENCIA

Si detectas cualquiera de estas condiciones, ALERTA INMEDIATA:

```python
EMERGENCY_CONDITIONS = {
    'icp': lambda x: x > 25,  # mmHg
    'cpp': lambda x: x < 50,  # mmHg
    'temperature': lambda x: x < 35,  # °C
    'glasgow': lambda x: x < 5,
    'spo2': lambda x: x < 88,
    'ph': lambda x: x < 7.2 or x > 7.6,
    'potassium': lambda x: x > 6.5,  # mEq/L
}

if any(condition(value) for condition, value in patient_data.items()):
    trigger_emergency_alert()
```

## 📝 NOTAS FINALES IMPORTANTES

1. **Este sistema es para APOYO a decisiones médicas, no reemplazo**
2. **Cada predicción debe ser validada por el equipo médico**
3. **Priorizar SIEMPRE la seguridad del paciente sobre la precisión**
4. **Documentar TODA decisión algorítmica para auditoría**
5. **El código debe ser robusto - la vida de mi padre depende de esto**

---

**CONSTRUYE ESTE SISTEMA COMO SI FUERA PARA TU PROPIO PADRE**

La situación es crítica, el tiempo es esencial, y cada patrón detectado, cada alerta temprana, puede ser la diferencia entre la vida y la muerte. No es solo código - es esperanza convertida en algoritmos, amor traducido a predicciones, y la determinación de una familia que no se rinde.

Mi papá es un guerrero. Este sistema será su escudo tecnológico.

**¡MANOS A LA OBRA! 💪**