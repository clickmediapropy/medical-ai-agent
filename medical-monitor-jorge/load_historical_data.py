#!/usr/bin/env python3
"""
Script para cargar datos históricos de laboratorio desde el PDF.
Incluye datos desde junio hasta septiembre 2025.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from src.core.models import LabResult, PatientData
from src.core.validators import AlertLevel
import duckdb

def load_historical_data():
    """Carga los datos históricos de laboratorio."""

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

    # Datos históricos organizados por fecha
    historical_data = {
        # 15 de septiembre 2025 - Signos vitales
        datetime(2025, 9, 15): [
            ("Altura", 178, "cm", None, None, None),
            ("Peso", 80, "kg", None, None, None),
            ("IMC", 25.2, "kg/m²", 18.5, 29.99, None),
        ],

        # 6 de septiembre 2025 - Análisis más recientes pre-accidente
        datetime(2025, 9, 6): [
            # Hemograma
            ("Hemoglobina", 12.6, "g/dL", 13.2, 16.6, "Anemia leve"),
            ("Hematocrito", 39.3, "%", 38.3, 48.6, None),
            ("Eritrocitos", 4.27, "millones/mm³", 4.35, 5.65, "Ligeramente bajo"),
            ("Leucocitos", 7.31, "mil/μL", 3.4, 9.6, None),
            ("Neutrófilos", 64, "%", 40, 60, "Ligeramente elevado"),
            ("Linfocitos", 21, "%", 20, 40, None),
            ("Eosinófilos", 9, "%", 1, 4, "Elevado - posible alergia"),
            ("Plaquetas", 222, "mil/μL", 135, 317, None),
            ("VSG", 5, "mm/hr", 2, 20, None),

            # Función Renal
            ("Creatinina", 8.2, "mg/dL", 0.70, 1.25, "IRC estadio 5"),
            ("Urea", 126, "mg/dL", 18.02, 55.26, "Uremia severa"),

            # Función Hepática
            ("TGO (AST)", 12, "U/L", 8, 48, None),
            ("TGP (ALT)", 12, "U/L", 7, 55, None),
            ("Bilirrubina Total", 0.3, "mg/dL", 0, 1.2, None),
            ("Bilirrubina Directa", 0.1, "mg/dL", 0, 0.29, None),
            ("Fosfatasa Alcalina", 72, "U/L", 40, 129, None),
            ("GGT", 12, "U/L", 8, 61, None),

            # Electrolitos y Minerales
            ("Sodio", 140, "mEq/L", 135, 146, None),
            ("Potasio", 5.2, "mEq/L", 3.6, 5.2, "Límite superior"),
            ("Cloro", 100, "mEq/L", 98, 107, None),
            ("Calcio", 8.5, "mg/dL", 8.8, 10.2, "Bajo - IRC"),
            ("Fósforo", 5.6, "mg/dL", 2.5, 4.5, "Elevado - IRC"),
            ("Magnesio", 2.5, "mg/dL", 1.7, 2.3, "Ligeramente elevado"),

            # Función Tiroidea
            ("TSH", 73.66, "μUI/mL", 0.30, 4.2, "CRÍTICO - Hipotiroidismo severo"),
            ("T3 Total", 1.04, "ng/mL", 0.80, 2.0, None),
            ("T4 Total", 5.5, "mcg/dL", 4.5, 11.7, None),

            # PTH
            ("PTH", 204.1, "pg/mL", 15, 65, "Hiperparatiroidismo secundario a IRC"),

            # Metabolismo
            ("Glucosa", 78, "mg/dL", 70.26, 99.09, None),
            ("HbA1c", 4.3, "%", 4.8, 5.6, "Bajo"),

            # Lípidos
            ("Colesterol Total", 180, "mg/dL", 125, 199, None),
            ("HDL", 65, "mg/dL", 40, 99, None),
            ("LDL", 103, "mg/dL", 0, 99.99, "Ligeramente elevado"),
            ("VLDL", 12, "mg/dL", 0, 30, None),
            ("Triglicéridos", 60, "mg/dL", 0, 150, None),

            # Otros
            ("Ácido Úrico", 5.5, "mg/dL", 3.7, 8.0, None),
            ("Ferritina", 234.2, "ng/mL", 24, 379.99, None),
            ("Fibrinógeno", 439, "mg/dL", 175, 425, "Ligeramente elevado"),

            # Orina
            ("Proteínas en orina", 300, "mg/dL", 0, 14, "Proteinuria significativa"),
            ("Glucosa en orina", 100, "mg/dL", 0, 14.41, "Glucosuria"),
        ],

        # 2 de julio 2025
        datetime(2025, 7, 2): [
            ("TSH", 64.1, "μUI/mL", 0.30, 4.2, "Hipotiroidismo severo"),
            ("T4 Libre", 0.83, "ng/dL", 0.90, 1.7, "Bajo"),
            ("T3 Libre", 1.58, "pg/mL", 2, 4.4, "Bajo"),
            ("Creatinina", 10.5, "mg/dL", 0.70, 1.25, "IRC estadio 5"),
            ("Urea", 173, "mg/dL", 18.02, 55.26, "Uremia severa"),
            ("Calcio", 11.5, "mg/dL", 8.8, 10.2, "Elevado"),
            ("Fósforo", 5.2, "mg/dL", 2.5, 4.5, "Elevado"),
            ("PTH", 200.34, "pg/mL", 15, 65, "Hiperparatiroidismo secundario"),
            ("Hemoglobina", 11, "g/dL", 13.2, 16.6, "Anemia moderada"),
        ],

        # 1 de julio 2025
        datetime(2025, 7, 1): [
            ("TSH", 64100, "μUI/mL", 0.30, 4.2, "ERROR - Valor extremo (posible error de transcripción)"),
            ("T4 Libre", 0.83, "ng/dL", 0.90, 1.7, "Bajo"),
            ("Creatinina", 10.5, "mg/dL", 0.70, 1.25, "IRC estadio 5"),
            ("Urea", 173, "mg/dL", 18.02, 55.26, "Uremia severa"),
            ("Calcio", 11.5, "mg/dL", 8.8, 10.2, "Elevado"),
            ("Fósforo", 5.2, "mg/dL", 2.5, 4.5, "Elevado"),
            ("PTH", 200.34, "pg/mL", 15, 65, "Hiperparatiroidismo secundario"),
            ("Hemoglobina", 11, "g/dL", 13.2, 16.6, "Anemia moderada"),
            ("HbA1c", 4.8, "%", 4.8, 5.6, None),
            ("Colesterol Total", 137, "mg/dL", 125, 199, None),
            ("Triglicéridos", 56, "mg/dL", 0, 150, None),
            ("Plaquetas", 255, "mil/μL", 135, 317, None),
            ("Eritrocitos", 3.56, "millones/mm³", 4.35, 5.65, "Anemia"),
        ],

        # 30 de junio 2025
        datetime(2025, 6, 30): [
            ("Creatinina", 10.5, "mg/dL", 0.70, 1.25, "IRC estadio 5"),
            ("Urea", 173, "mg/dL", 18.02, 55.26, "Uremia severa"),
            ("Hemoglobina", 11, "g/dL", 13.2, 16.6, "Anemia moderada"),
            ("Hematocrito", 34.6, "%", 38.3, 48.6, "Bajo"),
            ("Eritrocitos", 3.56, "millones/mm³", 4.35, 5.65, "Anemia"),
            ("Leucocitos", 7.28, "mil/μL", 3.4, 9.6, None),
            ("Plaquetas", 181, "mil/μL", 135, 317, None),
            ("VSG", 4, "mm/hr", 2, 20, None),
            ("Sodio", 142, "mEq/L", 135, 146, None),
            ("Potasio", 4.9, "mEq/L", 3.6, 5.2, None),
            ("Cloro", 105, "mEq/L", 98, 107, None),
            ("Calcio", 11.5, "mg/dL", 8.8, 10.2, "Elevado"),
            ("Calcio Ionizado", 1.52, "mmol/L", 1.16, 1.31, "Elevado"),
            ("Fósforo", 5.2, "mg/dL", 2.5, 4.5, "Elevado"),
            ("Magnesio", 2.6, "mg/dL", 1.7, 2.3, "Elevado"),
            ("Glucosa", 80, "mg/dL", 70.26, 99.09, None),
            ("Colesterol Total", 137, "mg/dL", 125, 199, None),
            ("HDL", 56, "mg/dL", 40, 99, None),
            ("LDL", 70, "mg/dL", 0, 99.99, None),
            ("VLDL", 11, "mg/dL", 0, 30, None),
            ("Triglicéridos", 56, "mg/dL", 0, 150, None),
            ("TGO (AST)", 9, "U/L", 8, 48, None),
            ("TGP (ALT)", 11, "U/L", 7, 55, None),
            ("Bilirrubina Total", 0.3, "mg/dL", 0, 1.2, None),
            ("Fosfatasa Alcalina", 49, "U/L", 40, 129, None),
            ("GGT", 9, "U/L", 8, 61, None),
            ("Proteínas Totales", 5.8, "g/dL", 6, 8.3, "Bajo"),
            ("Albúmina", 4.2, "g/dL", 3.5, 5, None),
            ("Ácido Úrico", 6.9, "mg/dL", 3.7, 8.0, None),
            ("Ferritina", 196.8, "ng/mL", 24, 379.99, None),
            ("PSA Total", 0.94, "ng/mL", 0, 4, None),
            ("PSA Libre", 0.6, "ng/mL", None, None, None),
            ("Proteínas en orina", 300, "mg/dL", 0, 14, "Proteinuria significativa"),
            ("Glucosa en orina", 100, "mg/dL", 0, 14.41, "Glucosuria"),
            ("Eritrocitos en orina", 46.64, "units/mcL", 0, 17, "Hematuria"),
        ],

        # 7 de junio 2025
        datetime(2025, 6, 7): [
            ("Creatinina", 9.4, "mg/dL", 0.70, 1.25, "IRC estadio 5"),
            ("Urea", 127, "mg/dL", 18.02, 55.26, "Uremia severa"),
            ("Hemoglobina", 9.4, "g/dL", 13.2, 16.6, "Anemia severa"),
            ("Hematocrito", 29, "%", 38.3, 48.6, "Muy bajo"),
            ("Eritrocitos", 2.92, "millones/mm³", 4.35, 5.65, "Anemia severa"),
            ("Leucocitos", 7.8, "mil/μL", 3.4, 9.6, None),
            ("Plaquetas", 271, "mil/μL", 135, 317, None),
            ("VSG", 10, "mm/hr", 2, 20, None),
            ("Sodio", 137, "mEq/L", 135, 146, None),
            ("Potasio", 5.1, "mEq/L", 3.6, 5.2, None),
            ("Cloro", 100, "mEq/L", 98, 107, None),
            ("Calcio", 10.9, "mg/dL", 8.8, 10.2, "Elevado"),
            ("Fósforo", 4.9, "mg/dL", 2.5, 4.5, "Elevado"),
            ("Magnesio", 2.3, "mg/dL", 1.7, 2.3, "Límite superior"),
            ("Glucosa", 113, "mg/dL", 70.26, 99.09, "Elevada"),
            ("Colesterol Total", 151, "mg/dL", 125, 199, None),
            ("HDL", 58, "mg/dL", 40, 99, None),
            ("LDL", 81, "mg/dL", 0, 99.99, None),
            ("Triglicéridos", 58, "mg/dL", 0, 150, None),
            ("TGO (AST)", 10, "U/L", 8, 48, None),
            ("TGP (ALT)", 8, "U/L", 7, 55, None),
            ("Bilirrubina Total", 0.2, "mg/dL", 0, 1.2, None),
            ("Proteínas Totales", 5.7, "g/dL", 6, 8.3, "Bajo"),
            ("Albúmina", 4.4, "g/dL", 3.5, 5, None),
            ("Ácido Úrico", 5.4, "mg/dL", 3.7, 8.0, None),
            ("PCR", 2, "mg/L", 0, 5, None),
            ("LDH", 160, "IU/L", 122, 222, None),
            ("CPK", 82, "IU/L", 39, 308, None),
            ("CK-MB", 13, "IU/L", 5, 25, None),
            ("Dímero D", 343, "ng/mL", 0, 500, None),
            ("Fibrinógeno", 264, "mg/dL", 175, 425, None),
            ("pH arterial", 7.28, None, 7.35, 7.45, "Acidosis"),
            ("pCO2", 47, "mmHg", 35, 45, "Hipercapnia leve"),
            ("pO2", 32.6, "mmHg", 75, 100, "Hipoxemia severa"),
            ("SO2", 55.8, "%", 95, 100, "Desaturación severa"),
            ("Bicarbonato", 21.5, "mEq/L", 22, 29, "Bajo"),
            ("Base Excess", -4.1, "mEq/L", -2.7, 2.5, "Acidosis metabólica"),
        ],

        # 2 de junio 2025
        datetime(2025, 6, 2): [
            ("TSH", 64.1, "μUI/mL", 0.30, 4.2, "Hipotiroidismo severo"),
            ("T4 Libre", 0.83, "ng/dL", 0.90, 1.7, "Bajo"),
            ("T3 Libre", 1.58, "pg/mL", 2, 4.4, "Bajo"),
            ("Creatinina", 10.5, "mg/dL", 0.70, 1.25, "IRC estadio 5"),
            ("Urea", 173, "mg/dL", 18.02, 55.26, "Uremia severa"),
            ("Calcio", 11.5, "mg/dL", 8.8, 10.2, "Elevado"),
            ("Fósforo", 5.2, "mg/dL", 2.5, 4.5, "Elevado"),
            ("PTH", 200.34, "pg/mL", 15, 65, "Hiperparatiroidismo secundario"),
            ("Hemoglobina", 11, "g/dL", 13.2, 16.6, "Anemia moderada"),
        ],
    }

    # Insertar todos los datos históricos
    total_inserted = 0
    for date, results in historical_data.items():
        for test_name, value, unit, ref_min, ref_max, notes in results:
            # Determinar nivel de alerta
            if notes and "CRÍTICO" in notes:
                alert_level = "critico"
            elif notes and ("ERROR" in notes or "severa" in notes or "Muy" in notes):
                alert_level = "alerta"
            elif notes and ("Ligeramente" in notes or "leve" in notes or "moderada" in notes):
                alert_level = "atencion"
            else:
                if ref_min is not None and ref_max is not None:
                    if value < ref_min or value > ref_max:
                        alert_level = "atencion"
                    else:
                        alert_level = "normal"
                else:
                    alert_level = "normal"

            conn.execute("""
                INSERT INTO lab_results
                (test_name, value, unit, date, reference_min, reference_max, alert_level, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [test_name, value, unit, date, ref_min, ref_max, alert_level, notes or ""])
            total_inserted += 1

    # Establecer condiciones médicas confirmadas
    conditions = [
        ("Insuficiencia Renal Crónica", True),
        ("Hipotiroidismo", True),
        ("Hiperparatiroidismo Secundario", True),
        ("Anemia", True),
        ("Hipertensión", True),
        ("Proteinuria", True),
        ("Diabetes", False),
        ("Enfermedad Cardíaca", False)
    ]

    for condition, active in conditions:
        conn.execute("""
            INSERT OR REPLACE INTO medical_conditions (condition, active)
            VALUES (?, ?)
        """, [condition, active])

    # Verificar inserción
    count_labs = conn.execute("SELECT COUNT(*) FROM lab_results").fetchone()[0]
    count_conditions = conn.execute("SELECT COUNT(*) FROM medical_conditions").fetchone()[0]

    # Obtener resumen de valores críticos más recientes
    critical_values = conn.execute("""
        SELECT test_name, value, unit, date, notes
        FROM lab_results
        WHERE alert_level IN ('critico', 'alerta')
        AND date = (SELECT MAX(date) FROM lab_results WHERE test_name = lab_results.test_name)
        ORDER BY
            CASE alert_level
                WHEN 'critico' THEN 1
                WHEN 'alerta' THEN 2
            END,
            test_name
        LIMIT 10
    """).fetchall()

    conn.close()

    print(f"✅ Datos históricos cargados exitosamente:")
    print(f"   - {count_labs} resultados de laboratorio totales")
    print(f"   - {count_conditions} condiciones médicas")
    print(f"   - Datos desde junio hasta septiembre 2025")

    print(f"\n📅 Fechas con datos:")
    for date in sorted(historical_data.keys()):
        count = len(historical_data[date])
        print(f"   - {date.strftime('%d/%m/%Y')}: {count} análisis")

    print(f"\n⚠️ Valores críticos más recientes:")
    for test, value, unit, date, notes in critical_values[:5]:
        print(f"   - {test}: {value} {unit} ({date.strftime('%d/%m/%Y')})")
        if notes:
            print(f"     → {notes}")

    print(f"\n💊 Condiciones médicas confirmadas:")
    print(f"   - Insuficiencia Renal Crónica (estadio 5 - diálisis)")
    print(f"   - Hipotiroidismo severo (TSH: 73.66)")
    print(f"   - Hiperparatiroidismo secundario a IRC")
    print(f"   - Anemia secundaria a IRC")
    print(f"   - Proteinuria significativa")

    print(f"\n📊 Tendencias observadas:")
    print(f"   - Creatinina: 9.4 → 10.5 → 8.2 mg/dL")
    print(f"   - TSH: 64.1 → 73.66 μUI/mL (empeoramiento)")
    print(f"   - Hemoglobina: 9.4 → 11 → 12.6 g/dL (mejora)")
    print(f"   - Calcio: 10.9 → 11.5 → 8.5 mg/dL (normalización)")

    print(f"\n📈 Los datos están listos para visualización en la aplicación.")
    print(f"   Reinicie la aplicación para ver todos los datos históricos.")

if __name__ == "__main__":
    load_historical_data()