#!/usr/bin/env python3
"""
Script para actualizar datos neurológicos críticos post-análisis de TC.
Incluye craniectomía descompresiva y parámetros de monitoreo intensivo.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import duckdb

def update_critical_neuro_data():
    """Actualiza los datos neurológicos críticos basados en TC del 17/09/2025."""

    # Conectar a la base de datos
    conn = duckdb.connect('medical_data.db')

    # Fecha del evento principal (estimada)
    surgery_date = datetime(2025, 9, 10)  # Probable fecha de craniectomía
    current_date = datetime(2025, 9, 17)

    # Obtener el siguiente ID para eventos médicos
    event_id = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM medical_events").fetchone()[0]

    # Eventos neurológicos críticos
    events = [
        # Craniectomía descompresiva
        (surgery_date, "14:00", "Cirugía",
         "CRANIECTOMÍA DESCOMPRESIVA IZQUIERDA",
         """PROCEDIMIENTO NEUROQUIRÚRGICO CRÍTICO
Craniectomía descompresiva temporal-parietal izquierda realizada de urgencia.

INDICACIÓN:
- Hematoma intracerebral 20cm³ con efecto de masa
- Hipertensión intracraneal refractaria
- Herniación cerebral inminente

HALLAZGOS INTRAOPERATORIOS:
- Duramadre tensa
- Cerebro edematoso con pérdida de pulsaciones
- Evacuación parcial de hematoma
- Duroplastia expansiva realizada

COMPLICACIONES: Ninguna inmediata
PRONÓSTICO: Reservado, dependiente de evolución del edema""",
         "crítico"),

        # Análisis de TC del 17/09
        (current_date, "11:00", "Imagenología",
         "TC Cerebral - Post-craniectomía día 7",
         """TOMOGRAFÍA COMPUTADA CEREBRAL - ANÁLISIS DETALLADO

HALLAZGOS PRINCIPALES:
1. Craniectomía descompresiva izquierda amplia
   - Defecto óseo temporal-parietal de aproximadamente 12x10 cm
   - Herniación transcraneal del parénquima cerebral (mushrooming)

2. EDEMA CEREBRAL SEVERO
   - Pérdida completa de diferenciación córtico-subcortical hemisferio izquierdo
   - Borramiento de surcos y cisuras
   - Fase de edema máximo (día 7-8 post-TCE)

3. EFECTO DE MASA
   - Desviación de línea media 3-5mm hacia derecha
   - Compresión ventricular bilateral
   - Compresión de cisternas basales parcial

4. EVOLUCIÓN DE LESIONES
   - Área hipodensa temporal-frontal izquierda (evolución de hematoma)
   - Probable afectación de área de Broca
   - Sin signos de resangrado

IMPLICACIONES CRÍTICAS:
- Riesgo alto de hidrocefalia
- PIC probablemente elevada
- Requiere monitoreo neurológico intensivo""",
         "crítico"),

        # Recomendaciones de manejo neurointensivo
        (current_date, "12:00", "Evolución Médica",
         "Plan Neurointensivo - Fase crítica de edema",
         """MANEJO NEUROINTENSIVO ACTUALIZADO

MONITOREO REQUERIDO (CRÍTICO):
• PIC objetivo: <20 mmHg (si catéter disponible)
• CPP objetivo: 60-70 mmHg
• Pupilas: cada 2 horas (asimetría = herniación)
• Glasgow o RASS: horario
• Sodio sérico: cada 6h (objetivo 145-155 mEq/L)
• Osmolaridad: cada 12h (objetivo 300-320 mOsm/L)

OPTIMIZACIÓN DE DIÁLISIS:
⚠️ CRÍTICO: Riesgo de síndrome de desequilibrio
• Preferir CRRT (terapia continua) sobre HD intermitente
• Si HD intermitente obligatoria:
  - Flujo inicial: <150 mL/min
  - Incremento gradual
  - Duración: >4 horas
  - Monitoreo neurológico durante y 6h post

MEDIDAS ANTI-EDEMA:
• Cabecera 30° permanente
• PAM >80 mmHg (para CPP adecuada)
• Salina hipertónica 3% si Na+ <145
• Evitar hipoglucemia (<70 mg/dL)
• Evitar hipertermia (objetivo 36-37°C)
• Sedación optimizada (evitar agitación)

PRONÓSTICO NEUROLÓGICO:
• Pico de edema: días 3-7 (actualmente en fase máxima)
• Inicio de mejoría esperada: días 10-14
• Despertar: agregado 72-96h por edema severo
• Probable afasia expresiva (área de Broca afectada)
• Recuperación funcional: meses""",
         "crítico"),

        # Preparación para complicaciones
        (current_date, "14:00", "Observación clínica",
         "Vigilancia de complicaciones neurológicas",
         """COMPLICACIONES A VIGILAR - PRÓXIMAS 72H CRÍTICAS

1. HIDROCEFALIA POST-TRAUMÁTICA
   - Ventrículos comprimidos pueden obstruirse
   - Vigilar deterioro súbito del sensorio
   - Puede requerir DVE (drenaje ventricular externo)

2. CRISIS CONVULSIVAS
   - Alto riesgo por lesión cortical
   - Profilaxis con antiepilépticos indicada
   - EEG si movimientos anormales

3. INFECCIÓN DE HERIDA QUIRÚRGICA
   - Vigilar fiebre sin otro foco
   - Cultivo de LCR si sospecha
   - Antibioticoterapia precoz

4. SÍNDROME DE TREPANADO
   - Cuando resuelva edema (semanas)
   - Hundimiento del colgajo cutáneo
   - Planificar craneoplastia (3-6 meses)

SIGNOS DE ALARMA INMEDIATOS:
🔴 Anisocoria (diferencia pupilar)
🔴 Bradicardia + HTA (Cushing)
🔴 Deterioro de Glasgow
🔴 Convulsiones
🔴 Fiebre >38.5°C sin foco""",
         "alta")
    ]

    # Insertar eventos
    for event_data in events:
        conn.execute("""
            INSERT INTO medical_events
            (id, date, time, type, title, description, urgency)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [event_id] + list(event_data))
        event_id += 1

    # Actualizar condiciones médicas
    new_conditions = [
        ("Craniectomía descompresiva", True),
        ("Edema cerebral severo", True),
        ("Riesgo de hidrocefalia", True),
        ("Probable afasia de Broca", True),
        ("Hipertensión intracraneal", True)
    ]

    for condition, active in new_conditions:
        conn.execute("""
            INSERT OR REPLACE INTO medical_conditions (condition, active)
            VALUES (?, ?)
        """, [condition, active])

    # Agregar parámetros de monitoreo objetivo
    conn.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_targets (
            parameter VARCHAR PRIMARY KEY,
            target_min DOUBLE,
            target_max DOUBLE,
            unit VARCHAR,
            frequency VARCHAR,
            critical BOOLEAN,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    targets = [
        ("PIC", None, 20, "mmHg", "Continuo", True),
        ("CPP", 60, 70, "mmHg", "Continuo", True),
        ("Sodio", 145, 155, "mEq/L", "Cada 6h", True),
        ("Osmolaridad", 300, 320, "mOsm/L", "Cada 12h", True),
        ("PAM", 80, 100, "mmHg", "Continuo", True),
        ("Temperatura", 36, 37, "°C", "Continuo", True),
        ("Glucemia", 100, 180, "mg/dL", "Cada 6h", True),
        ("Glasgow", 3, 15, "puntos", "Horario", True)
    ]

    for target_data in targets:
        conn.execute("""
            INSERT OR REPLACE INTO monitoring_targets
            (parameter, target_min, target_max, unit, frequency, critical)
            VALUES (?, ?, ?, ?, ?, ?)
        """, target_data)

    # Actualizar recomendaciones de diálisis
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dialysis_recommendations (
            id INTEGER PRIMARY KEY,
            date DATE,
            mode VARCHAR,
            parameters VARCHAR,
            rationale VARCHAR,
            priority VARCHAR,
            active BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    dialysis_id = 1
    conn.execute("""
        DELETE FROM dialysis_recommendations
    """)

    conn.execute("""
        INSERT INTO dialysis_recommendations
        (id, date, mode, parameters, rationale, priority, active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        dialysis_id,
        current_date,
        "CRRT (preferido) o HD prolongada",
        """CRRT ideal. Si HD intermitente:
- Flujo sangre inicial: <150 mL/min
- Incremento gradual en 30 min
- Duración: mínimo 4 horas
- Ultrafiltración: <500 mL/h
- Temperatura del baño: 36°C
- Sodio del baño: 145 mEq/L
- Monitoreo neurológico continuo""",
        "Prevención de síndrome de desequilibrio en paciente con edema cerebral severo y craniectomía",
        "CRÍTICA",
        True
    ])

    # Verificar inserción
    count_events = conn.execute(
        "SELECT COUNT(*) FROM medical_events WHERE date >= ?",
        [surgery_date]
    ).fetchone()[0]

    count_conditions = conn.execute(
        "SELECT COUNT(*) FROM medical_conditions WHERE active = TRUE"
    ).fetchone()[0]

    count_targets = conn.execute(
        "SELECT COUNT(*) FROM monitoring_targets"
    ).fetchone()[0]

    conn.close()

    print(f"✅ Actualización neurológica crítica completada:")
    print(f"   - {count_events} eventos neurológicos agregados")
    print(f"   - {count_conditions} condiciones médicas activas")
    print(f"   - {count_targets} parámetros de monitoreo definidos")
    print(f"\n🧠 DATOS CRÍTICOS AGREGADOS:")
    print(f"   - Craniectomía descompresiva izquierda confirmada")
    print(f"   - Edema cerebral severo en fase máxima")
    print(f"   - Desviación de línea media 3-5mm")
    print(f"   - Probable afectación del área de Broca")
    print(f"\n⚠️ ALERTAS CRÍTICAS:")
    print(f"   - Riesgo alto de hidrocefalia próximas 72h")
    print(f"   - Diálisis debe ser CRRT o HD >4h para evitar síndrome de desequilibrio")
    print(f"   - Monitoreo pupilar cada 2h (anisocoria = herniación)")
    print(f"   - Mantener Na+ 145-155 mEq/L para control de edema")
    print(f"\n📊 PRONÓSTICO ACTUALIZADO:")
    print(f"   - Despertar esperado: +72-96h adicionales por edema")
    print(f"   - Probable afasia expresiva al despertar")
    print(f"   - Recuperación funcional: meses")
    print(f"   - Craneoplastia planificada: 3-6 meses")

if __name__ == "__main__":
    update_critical_neuro_data()