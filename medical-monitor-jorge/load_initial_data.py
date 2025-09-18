#!/usr/bin/env python3
"""
Script para cargar datos de laboratorio pre-accidente del 06/09/2025.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from src.core.models import LabResult, PatientData
from src.core.validators import AlertLevel
import duckdb
import json

def load_lab_data():
    """Carga los datos de laboratorio del 06/09/2025."""

    # Inicializar base de datos
    conn = duckdb.connect('medical_data.db')

    # Crear tablas si no existen
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS lab_results_seq START 1
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS lab_results (
            id INTEGER PRIMARY KEY DEFAULT nextval('lab_results_seq'),
            test_name VARCHAR,
            value DOUBLE,
            unit VARCHAR,
            date DATE,
            reference_min DOUBLE,
            reference_max DOUBLE,
            alert_level VARCHAR,
            notes VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS medical_conditions (
            condition VARCHAR PRIMARY KEY,
            active BOOLEAN,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Limpiar datos anteriores
    conn.execute("DELETE FROM lab_results")
    conn.execute("DELETE FROM medical_conditions")

    # Fecha de los análisis
    lab_date = datetime(2025, 9, 6)

    # Datos de laboratorio del 06/09/2025
    lab_results = [
        # Hemograma
        ("Hemoglobina", 12.6, "g/dL", 13.0, 17.0, "Anemia leve"),
        ("Hematocrito", 38.8, "%", 40.0, 50.0, "Ligeramente bajo"),
        ("Leucocitos", 8.2, "mil/μL", 4.5, 11.0, None),
        ("Neutrófilos", 74.0, "%", 40.0, 74.0, None),
        ("Linfocitos", 17.5, "%", 20.0, 40.0, "Ligeramente bajo"),
        ("Plaquetas", 250, "mil/μL", 150, 450, None),

        # Función Renal
        ("Creatinina", 8.2, "mg/dL", 0.7, 1.3, "IRC severa - requiere diálisis"),
        ("Urea", 126, "mg/dL", 15, 45, "Muy elevada - uremia"),
        ("BUN", 59, "mg/dL", 7, 21, "Muy elevado"),
        ("eGFR", 6.5, "mL/min/1.73m²", 90, 120, "IRC estadio 5 - falla renal"),

        # Electrolitos
        ("Sodio", 139, "mEq/L", 136, 145, None),
        ("Potasio", 5.2, "mEq/L", 3.5, 5.1, "Ligeramente elevado - riesgo de arritmia"),
        ("Cloro", 105, "mEq/L", 98, 107, None),

        # Función Tiroidea
        ("TSH", 73.66, "μUI/mL", 0.4, 4.0, "CRÍTICO - Hipotiroidismo severo"),
        ("T4 Libre", 0.72, "ng/dL", 0.9, 1.7, "Bajo - hipotiroidismo"),

        # Metabolismo Óseo-Mineral
        ("Calcio", 8.5, "mg/dL", 8.5, 10.5, "Límite inferior"),
        ("Fósforo", 5.6, "mg/dL", 2.5, 4.5, "Elevado - común en IRC"),
        ("PTH", 204.1, "pg/mL", 15, 65, "Hiperparatiroidismo secundario"),

        # Función Hepática
        ("TGO (AST)", 28, "U/L", 10, 40, None),
        ("TGP (ALT)", 35, "U/L", 10, 40, None),
        ("Bilirrubina Total", 0.7, "mg/dL", 0.2, 1.2, None),

        # Metabolismo
        ("Glucosa", 108, "mg/dL", 70, 110, None),
        ("Colesterol Total", 158, "mg/dL", 0, 200, None),
        ("Triglicéridos", 142, "mg/dL", 0, 150, None),
        ("HDL", 38, "mg/dL", 40, 60, "Bajo - riesgo cardiovascular"),
        ("LDL", 92, "mg/dL", 0, 130, None),

        # Proteínas
        ("Proteínas Totales", 6.8, "g/dL", 6.0, 8.0, None),
        ("Albúmina", 3.7, "g/dL", 3.5, 5.0, None),

        # Otros
        ("Ácido Úrico", 6.8, "mg/dL", 3.4, 7.0, None),
        ("PCR", 2.8, "mg/L", 0, 5, None),
    ]

    # Insertar resultados de laboratorio
    for test_name, value, unit, ref_min, ref_max, notes in lab_results:
        # Determinar nivel de alerta
        if notes and "CRÍTICO" in notes:
            alert_level = "critico"
        elif notes and ("Muy elevad" in notes or "Muy alto" in notes or "severa" in notes):
            alert_level = "alerta"
        elif notes and ("Ligeramente" in notes or "Levemente" in notes):
            alert_level = "atencion"
        else:
            if value < ref_min or value > ref_max:
                alert_level = "atencion"
            else:
                alert_level = "normal"

        conn.execute("""
            INSERT INTO lab_results
            (test_name, value, unit, date, reference_min, reference_max, alert_level, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [test_name, value, unit, lab_date, ref_min, ref_max, alert_level, notes or ""])

    # Establecer condiciones médicas conocidas
    conditions = [
        ("Insuficiencia Renal Crónica", True),
        ("Hipotiroidismo", True),
        ("Hiperparatiroidismo Secundario", True),
        ("Anemia", True),
        ("Hipertensión", True),
        ("Diabetes", False),
        ("Enfermedad Cardíaca", False)
    ]

    for condition, active in conditions:
        conn.execute("""
            INSERT INTO medical_conditions (condition, active)
            VALUES (?, ?)
        """, [condition, active])

    # Verificar inserción
    count_labs = conn.execute("SELECT COUNT(*) FROM lab_results").fetchone()[0]
    count_conditions = conn.execute("SELECT COUNT(*) FROM medical_conditions").fetchone()[0]

    conn.close()

    print(f"✅ Datos cargados exitosamente:")
    print(f"   - {count_labs} resultados de laboratorio")
    print(f"   - {count_conditions} condiciones médicas")
    print(f"\n📅 Fecha de los análisis: 06/09/2025")
    print(f"\n⚠️ Valores críticos detectados:")
    print(f"   - TSH: 73.66 μUI/mL (CRÍTICO - Hipotiroidismo severo)")
    print(f"   - Creatinina: 8.2 mg/dL (IRC estadio 5)")
    print(f"   - Urea: 126 mg/dL (Uremia)")
    print(f"   - PTH: 204.1 pg/mL (Hiperparatiroidismo secundario)")
    print(f"\n💊 Condiciones médicas activas:")
    print(f"   - Insuficiencia Renal Crónica (estadio 5)")
    print(f"   - Hipotiroidismo severo")
    print(f"   - Hiperparatiroidismo secundario")
    print(f"   - Anemia")
    print(f"   - Hipertensión")
    print(f"\n📊 Los datos ya están disponibles en la aplicación.")
    print(f"   Reinicie la aplicación para ver los cambios.")

if __name__ == "__main__":
    load_lab_data()