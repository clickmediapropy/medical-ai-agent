"""
Módulo de base de datos para el sistema de monitoreo médico.
"""

import duckdb
from datetime import datetime
from typing import Optional
from src.core.models import PatientData, LabResult, ConditionType, AlertLevel


def init_database(db_path: str = "medical_data.db") -> duckdb.DuckDBPyConnection:
    """
    Inicializa la base de datos y crea las tablas si no existen.

    Args:
        db_path: Ruta a la base de datos

    Returns:
        Conexión a la base de datos
    """
    conn = duckdb.connect(db_path)

    # Crear secuencia para IDs
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS lab_results_seq START 1
    """)

    # Crear tabla de resultados de laboratorio
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

    # Crear tabla de condiciones médicas
    conn.execute("""
        CREATE TABLE IF NOT EXISTS medical_conditions (
            condition VARCHAR PRIMARY KEY,
            active BOOLEAN,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Crear tabla de medicaciones
    conn.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            dose VARCHAR,
            frequency VARCHAR,
            start_date DATE,
            end_date DATE,
            active BOOLEAN,
            notes VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    return conn


def load_existing_data(conn: duckdb.DuckDBPyConnection, patient_data: PatientData):
    """
    Carga datos existentes de la base de datos al objeto PatientData.

    Args:
        conn: Conexión a la base de datos
        patient_data: Objeto PatientData a llenar
    """
    # Cargar resultados de laboratorio
    try:
        results = conn.execute("""
            SELECT test_name, value, unit, date, reference_min, reference_max, alert_level, notes
            FROM lab_results
            ORDER BY date DESC, test_name
        """).fetchall()

        for row in results:
            test_name, value, unit, date, ref_min, ref_max, alert_level, notes = row

            # Convertir alert_level string a enum
            alert_enum = AlertLevel.NORMAL
            if alert_level == "critico":
                alert_enum = AlertLevel.CRITICO
            elif alert_level == "alerta":
                alert_enum = AlertLevel.ALERTA
            elif alert_level == "atencion":
                alert_enum = AlertLevel.ATENCION

            # Convertir date a datetime si es necesario
            from datetime import datetime, date as date_type
            if isinstance(date, date_type) and not isinstance(date, datetime):
                date = datetime.combine(date, datetime.min.time())

            lab_result = LabResult(
                test_name=test_name,
                value=value,
                unit=unit,
                date=date,
                reference_min=ref_min if ref_min else None,
                reference_max=ref_max if ref_max else None,
                alert_level=alert_enum,
                notes=notes if notes else None
            )
            patient_data.lab_results.append(lab_result)
    except Exception as e:
        print(f"Error cargando resultados de laboratorio: {e}")

    # Cargar condiciones médicas
    try:
        conditions = conn.execute("""
            SELECT condition, active
            FROM medical_conditions
            WHERE active = TRUE
        """).fetchall()

        for row in conditions:
            condition, active = row
            # Mapear condiciones a ConditionType
            condition_map = {
                "Insuficiencia Renal Crónica": ConditionType.IRC_TERMINAL,
                "Hipotiroidismo": ConditionType.HIPOTIROIDISMO,
                "Hiperparatiroidismo Secundario": ConditionType.HIPERPARATIROIDISMO,
                "Anemia": ConditionType.ANEMIA,
                "Hipertensión": ConditionType.HIPERTENSION,
                "Diabetes": ConditionType.DIABETES,
                "Enfermedad Cardíaca": ConditionType.ENFERMEDAD_CARDIACA
            }

            if condition in condition_map:
                patient_data.conditions.append(condition_map[condition])
    except Exception as e:
        print(f"Error cargando condiciones médicas: {e}")


def save_lab_result(conn: duckdb.DuckDBPyConnection, lab_result: LabResult):
    """
    Guarda un resultado de laboratorio en la base de datos.

    Args:
        conn: Conexión a la base de datos
        lab_result: Resultado de laboratorio a guardar
    """
    conn.execute("""
        INSERT INTO lab_results
        (test_name, value, unit, date, reference_min, reference_max, alert_level, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        lab_result.test_name,
        lab_result.value,
        lab_result.unit,
        lab_result.date,
        lab_result.reference_min,
        lab_result.reference_max,
        lab_result.alert_level.value,
        lab_result.notes
    ])
    conn.commit()


def save_conditions(conn: duckdb.DuckDBPyConnection, conditions: list):
    """
    Actualiza las condiciones médicas en la base de datos.

    Args:
        conn: Conexión a la base de datos
        conditions: Lista de condiciones activas
    """
    # Primero desactivar todas
    conn.execute("UPDATE medical_conditions SET active = FALSE")

    # Activar las seleccionadas
    for condition in conditions:
        condition_name = {
            ConditionType.IRC_TERMINAL: "Insuficiencia Renal Crónica",
            ConditionType.HIPOTIROIDISMO: "Hipotiroidismo",
            ConditionType.HIPERPARATIROIDISMO: "Hiperparatiroidismo Secundario",
            ConditionType.ANEMIA: "Anemia",
            ConditionType.HIPERTENSION: "Hipertensión",
            ConditionType.DIABETES: "Diabetes",
            ConditionType.ENFERMEDAD_CARDIACA: "Enfermedad Cardíaca"
        }.get(condition)

        if condition_name:
            conn.execute("""
                INSERT INTO medical_conditions (condition, active)
                VALUES (?, TRUE)
                ON CONFLICT (condition) DO UPDATE SET
                active = TRUE,
                updated_at = CURRENT_TIMESTAMP
            """, [condition_name])

    conn.commit()