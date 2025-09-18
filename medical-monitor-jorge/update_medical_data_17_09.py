#!/usr/bin/env python3
"""
Script para actualizar datos médicos del 17/09/2025.
Incluye signos vitales, medicamentos y nuevos eventos.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import duckdb

def update_medical_data():
    """Actualiza los datos médicos con información del 17/09/2025."""

    # Conectar a la base de datos
    conn = duckdb.connect('medical_data.db')

    # Crear secuencias si no existen
    conn.execute("CREATE SEQUENCE IF NOT EXISTS medications_seq START 1")
    conn.execute("CREATE SEQUENCE IF NOT EXISTS vital_signs_seq START 1")
    conn.execute("CREATE SEQUENCE IF NOT EXISTS medical_events_seq START 1")

    # Crear tabla de medicamentos si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY DEFAULT nextval('medications_seq'),
            medication_name VARCHAR,
            type VARCHAR,
            dose VARCHAR,
            frequency VARCHAR,
            route VARCHAR,
            start_date DATE,
            end_date DATE,
            active BOOLEAN,
            notes VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Crear tabla de signos vitales si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vital_signs (
            id INTEGER PRIMARY KEY DEFAULT nextval('vital_signs_seq'),
            date DATE,
            time VARCHAR,
            blood_pressure_systolic INTEGER,
            blood_pressure_diastolic INTEGER,
            heart_rate INTEGER,
            oxygen_saturation INTEGER,
            temperature DOUBLE,
            respiratory_rate INTEGER,
            notes VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Crear tabla de eventos médicos si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS medical_events (
            id INTEGER PRIMARY KEY DEFAULT nextval('medical_events_seq'),
            date DATE,
            time VARCHAR,
            type VARCHAR,
            title VARCHAR,
            description VARCHAR,
            urgency VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Fecha actual
    current_date = datetime(2025, 9, 17)

    # Obtener el siguiente ID para vital_signs
    max_id = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM vital_signs").fetchone()[0]

    # Insertar signos vitales del 17/09/2025
    conn.execute("""
        INSERT INTO vital_signs
        (id, date, time, blood_pressure_systolic, blood_pressure_diastolic,
         heart_rate, oxygen_saturation, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        max_id,
        current_date,
        "15:00",
        185,  # PA sistólica elevada
        98,   # PA diastólica elevada
        99,   # FC
        99,   # SatO2
        "PA elevada (MAP 126). Monitor SPACELABS Healthcare. Paciente en UCI con soporte respiratorio."
    ])

    # Limpiar medicamentos anteriores e insertar los actuales
    conn.execute("DELETE FROM medications")

    # Obtener el ID inicial para medicamentos
    med_id = 1

    # Medicamentos activos al 17/09/2025
    # Formato: (nombre, dosis, frecuencia, fecha_inicio, fecha_fin, activo, notas)
    medications = [
        ("Remifentanilo", "10 mL/h", "Infusión continua IV", current_date, None, True,
         "Analgésico opioide - Bomba TERUMO 10.00 mL/h (282.00 mL administrados)"),

        ("Omeprazol", "20 mg", "Cada 24 horas IV", current_date, None, True,
         "Gastroprotección en UCI"),

        ("Lacosamida", "5 mg", "Goteo continuo 24h IV", current_date, None, True,
         "Antiepiléptico - 3 ampollas para goteo continuo"),

        ("Ácido valproico", "500 mg", "Cada 12 horas IV", current_date, None, True,
         "Antiepiléptico - Control de convulsiones post-TCE"),

        ("Enalapril", "10 mg", "Según PA IV", current_date, None, True,
         "Antihipertensivo - Control de hipertensión arterial"),

        ("Levotiroxina", "150 mg", "Cada 24 horas SNG", current_date, None, True,
         "Hormona tiroidea - Hipotiroidismo"),

        ("Medicamento no identificado", "55 mL/h", "Infusión continua IV", current_date, None, True,
         "Bomba TERUMO 55.00 mL/h (98.90 mL administrados)")
    ]

    for med_data in medications:
        conn.execute("""
            INSERT INTO medications
            (id, name, dose, frequency, start_date, end_date, active, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [med_id] + list(med_data))
        med_id += 1

    # Obtener el siguiente ID para eventos médicos
    event_id = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM medical_events").fetchone()[0]

    # Insertar eventos médicos importantes
    events = [
        (current_date, "14:59", "Imagenología",
         "Tomografía Cerebral - Evolución favorable",
         """Resultado de tomografía cerebral muestra:
- Hematoma sin aumento, iniciando reabsorción
- Edema perilesional menor que en estudio previo
- Sin signos de compresión cerebral
- Recuperación neurológica lenta esperada por edad y enfermedad renal
Dr. Guido - Evaluación neurológica""",
         "No urgente"),

        (current_date, "15:00", "Observación clínica",
         "Monitoreo UCI - PA elevada",
         """Monitoreo continuo en UCI:
- PA: 185/98 mmHg (MAP 126) - ELEVADA
- FC: 99 lpm
- SatO2: 99%
- 3 bombas de infusión activas
- Soporte respiratorio con O2""",
         "Alta"),

        (current_date, "19:00", "Evolución clínica",
         "Informe consolidado del día",
         """Estado al 17/09/2025:
- Neurológico: recuperación lenta pero progresiva
- Respiratorio: traqueostomía permeable, ventilación espontánea con O2
- Renal: hemodiálisis regular con buena respuesta
- Hemodinámico: PA controlada con medicación
- Pronóstico: favorable para absorción del hematoma""",
         "Media"),

        (datetime(2025, 9, 30), "10:00", "Documentación",
         "Certificado médico UCI - Sanatorio La Costa",
         """Diagnósticos actualizados:
1. Encefalopatía + Drenaje HSA agudo lado izquierdo
2. Hematoma temporal lado izquierdo
3. ERC en hemodiálisis trisemanal M/S
4. HTA
5. Hipoparatiroidismo (paratiroidectomía total)
6. Hipotiroidismo
Médicos: Dra. Cecilia Colabrese Díaz, Dr. Rubén Deporte Salcedo""",
         "No urgente")
    ]

    for event_data in events:
        conn.execute("""
            INSERT INTO medical_events
            (id, date, time, type, title, description, urgency)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [event_id] + list(event_data))
        event_id += 1

    # Actualizar condiciones médicas
    conn.execute("""
        UPDATE medical_conditions
        SET active = TRUE, updated_at = CURRENT_TIMESTAMP
        WHERE condition = 'Hipertensión'
    """)

    # Agregar nuevas condiciones si no existen
    new_conditions = [
        ("Traumatismo Craneoencefálico", True),
        ("Hematoma Intracerebral", True),
        ("Traqueostomía", True),
        ("Encefalopatía", True)
    ]

    for condition, active in new_conditions:
        conn.execute("""
            INSERT OR REPLACE INTO medical_conditions (condition, active)
            VALUES (?, ?)
        """, [condition, active])

    # Agregar resultados de laboratorio del 16/09/2025
    lab_date_16 = datetime(2025, 9, 16)

    # Solo valores básicos visibles en imagen (hemoglobina y hematocrito corregidos)
    lab_results_16 = [
        ("Hemoglobina", 10.6, "g/dL", 13.0, 17.0, "Anemia moderada"),
        ("Hematocrito", 31.9, "%", 40.0, 50.0, "Bajo - anemia"),
        ("Leucocitos", 6090, "/μL", 4500, 11000, None),
    ]

    for test_name, value, unit, ref_min, ref_max, notes in lab_results_16:
        if value < ref_min:
            alert_level = "atencion" if (ref_min - value) / ref_min < 0.2 else "alerta"
        elif value > ref_max:
            alert_level = "atencion" if (value - ref_max) / ref_max < 0.2 else "alerta"
        else:
            alert_level = "normal"

        if notes and "moderada" in notes.lower():
            alert_level = "atencion"
        elif notes and ("severa" in notes.lower() or "crítico" in notes.lower()):
            alert_level = "critico"

        conn.execute("""
            INSERT INTO lab_results
            (test_name, value, unit, date, reference_min, reference_max, alert_level, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [test_name, value, unit, lab_date_16, ref_min, ref_max, alert_level, notes or ""])

    # Verificar inserción
    count_vitals = conn.execute("SELECT COUNT(*) FROM vital_signs WHERE date = ?", [current_date]).fetchone()[0]
    count_meds = conn.execute("SELECT COUNT(*) FROM medications WHERE active = TRUE").fetchone()[0]
    count_events = conn.execute("SELECT COUNT(*) FROM medical_events WHERE date >= ?", [current_date]).fetchone()[0]
    count_labs = conn.execute("SELECT COUNT(*) FROM lab_results WHERE date = ?", [lab_date_16]).fetchone()[0]

    conn.close()

    print(f"✅ Actualización completada exitosamente:")
    print(f"   - {count_vitals} registro(s) de signos vitales agregados")
    print(f"   - {count_meds} medicamentos activos")
    print(f"   - {count_events} eventos médicos registrados")
    print(f"   - {count_labs} resultados de laboratorio del 16/09")
    print(f"\n📅 Fecha de actualización: 17/09/2025")
    print(f"\n⚠️ Alertas importantes:")
    print(f"   - PA elevada: 185/98 mmHg (MAP 126)")
    print(f"   - Remifentanilo en infusión: 10 mL/h")
    print(f"   - 3 bombas de infusión activas")
    print(f"\n✅ Estado actual:")
    print(f"   - Tomografía muestra evolución favorable")
    print(f"   - Hematoma en reabsorción")
    print(f"   - Recuperación neurológica lenta pero progresiva")
    print(f"\n💊 Medicamentos activos:")
    print(f"   - Remifentanilo (analgesia)")
    print(f"   - Omeprazol (gastroprotección)")
    print(f"   - Lacosamida (antiepiléptico)")
    print(f"   - Ácido valproico (antiepiléptico)")
    print(f"   - Enalapril (antihipertensivo)")
    print(f"   - Levotiroxina (hormona tiroidea)")
    print(f"\n📊 Los datos ya están disponibles en la base de datos.")
    print(f"   Reinicie la aplicación para ver los cambios.")

if __name__ == "__main__":
    update_medical_data()