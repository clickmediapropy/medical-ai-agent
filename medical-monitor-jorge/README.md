# 🏥 Sistema de Monitoreo Médico - Jorge Agustín

Sistema de apoyo familiar para monitoreo médico. Diseñado para ayudar a familiares no médicos a entender y seguir la evolución de valores de laboratorio y condiciones médicas.

## 🎯 Características

- **Entrada flexible de datos**: Ingrese cualquier tipo de resultado de laboratorio
- **Validación automática**: Detecta valores fuera de rango y críticos
- **Calculadoras médicas**: eGFR, riesgo de crisis tiroidea, análisis de anemia
- **Visualización de tendencias**: Gráficos interactivos de evolución
- **Preguntas sugeridas**: Genera preguntas relevantes para el equipo médico
- **Educación integrada**: Explicaciones simples de valores y condiciones

## 🚀 Instalación

### Requisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. Clone o descargue este repositorio
2. Navegue al directorio del proyecto:
```bash
cd medical-monitor-jorge
```

3. Cree un entorno virtual:
```bash
python3 -m venv venv
```

4. Active el entorno virtual:
- En macOS/Linux:
```bash
source venv/bin/activate
```
- En Windows:
```bash
venv\Scripts\activate
```

5. Instale las dependencias:
```bash
pip install -r requirements.txt
```

## 🖥️ Uso

1. Inicie la aplicación:
```bash
streamlit run app.py
```

2. Se abrirá automáticamente en su navegador en `http://localhost:8501`

3. Comience por:
   - Registrar las condiciones médicas del paciente
   - Ingresar resultados de laboratorio recientes
   - Explorar las calculadoras médicas
   - Revisar las preguntas sugeridas para médicos

## 📊 Funcionalidades principales

### Dashboard
- Vista general de valores más recientes
- Alertas de valores críticos
- Resumen del estado del paciente

### Entrada de datos
- Formulario simple para laboratorios
- Registro de medicaciones
- Condiciones médicas
- Signos vitales

### Calculadoras
- **eGFR (CKD-EPI 2021)**: Función renal estimada
- **Riesgo Mixedematoso**: Evalúa riesgo de crisis tiroidea
- **Análisis Calcio-PTH**: Balance mineral
- **Evaluación de Anemia**: Severidad y recomendaciones

### Visualizaciones
- Tendencias temporales de cualquier valor
- Comparación con rangos normales
- Identificación de valores críticos

## ⚠️ Importante

**Este sistema es una herramienta educativa y de apoyo familiar.**

- NO es un dispositivo médico certificado
- NO debe usarse para tomar decisiones médicas
- SIEMPRE consulte con el equipo médico tratante
- Los cálculos y recomendaciones son solo orientativos

## 🔒 Privacidad

- Todos los datos se almacenan localmente en su computadora
- No se envía información a servidores externos
- Los datos persisten solo durante la sesión activa

## 📝 Valores de referencia

El sistema incluye rangos de referencia para:
- Valores normales estándar
- Valores ajustados para IRC (Insuficiencia Renal Crónica)
- Detección de valores críticos que requieren atención inmediata

## 🆘 Soporte

Si encuentra algún problema o tiene sugerencias, por favor:
1. Verifique que todos los valores ingresados sean correctos
2. Reinicie la aplicación si es necesario
3. Consulte con el equipo médico para interpretaciones

## 📚 Recursos adicionales

El sistema incluye información educativa sobre:
- Insuficiencia Renal Crónica
- Hipotiroidismo
- Interpretación de valores de laboratorio
- Preguntas frecuentes

---

**Desarrollado con ❤️ para el cuidado de Jorge Agustín**

*Versión 1.0.0 - Septiembre 2025*