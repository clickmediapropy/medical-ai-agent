"""
Modelos de datos flexibles para el sistema de monitoreo médico.
NO contiene datos precargados - diseñado para recibir datos actualizados.
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum


class ConditionType(Enum):
    """Tipos de condiciones médicas"""
    IRC_TERMINAL = "Insuficiencia Renal Crónica Terminal"
    TCE_SEVERO = "Traumatismo Craneoencefálico Severo"
    HIPOTIROIDISMO = "Hipotiroidismo"
    HIPERPARATIROIDISMO = "Hiperparatiroidismo"
    POST_CRANIECTOMIA = "Post-Craniectomía"
    DIALISIS = "En Diálisis"
    ANEMIA = "Anemia"
    DIABETES = "Diabetes"
    HIPERTENSION = "Hipertensión"
    ENFERMEDAD_CARDIACA = "Enfermedad Cardíaca"
    OTRO = "Otra Condición"


class AlertLevel(Enum):
    """Niveles de alerta para valores críticos"""
    NORMAL = "normal"
    ATENCION = "atención"
    ALERTA = "alerta"
    CRITICO = "crítico"


@dataclass
class LabResult:
    """Resultado de laboratorio individual"""
    test_name: str
    value: float
    unit: str
    date: datetime
    reference_min: Optional[float] = None
    reference_max: Optional[float] = None
    reference_irc_min: Optional[float] = None
    reference_irc_max: Optional[float] = None
    alert_level: AlertLevel = AlertLevel.NORMAL
    notes: str = ""

    def is_critical(self, has_irc: bool = False) -> bool:
        """Determina si el valor es crítico"""
        if has_irc and self.reference_irc_min is not None:
            return self.value < self.reference_irc_min or self.value > self.reference_irc_max
        elif self.reference_min is not None:
            return self.value < self.reference_min or self.value > self.reference_max
        return False


@dataclass
class Medication:
    """Información de medicación"""
    name: str
    dose: float
    unit: str
    frequency: str
    route: str
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool = True
    adjusted_for_irc: bool = False
    notes: str = ""


@dataclass
class ClinicalEvent:
    """Evento clínico significativo"""
    event_type: str
    date: datetime
    description: str
    severity: str = "moderate"
    action_taken: str = ""
    outcome: str = ""


@dataclass
class VitalSigns:
    """Signos vitales"""
    date: datetime
    heart_rate: Optional[int] = None
    blood_pressure_sys: Optional[int] = None
    blood_pressure_dia: Optional[int] = None
    temperature: Optional[float] = None
    oxygen_saturation: Optional[int] = None
    respiratory_rate: Optional[int] = None
    glasgow_score: Optional[int] = None
    notes: str = ""


@dataclass
class PatientData:
    """
    Modelo principal del paciente.
    Flexible para recibir cualquier tipo de dato cuando esté disponible.
    """
    # Información básica
    name: str = "Jorge Agustín"
    age: int = 65
    weight: Optional[float] = None  # kg
    height: Optional[float] = None  # cm

    # Condiciones médicas (vacío inicialmente)
    conditions: List[ConditionType] = field(default_factory=list)

    # Datos clínicos (todos vacíos inicialmente)
    lab_results: List[LabResult] = field(default_factory=list)
    medications: List[Medication] = field(default_factory=list)
    clinical_events: List[ClinicalEvent] = field(default_factory=list)
    vital_signs: List[VitalSigns] = field(default_factory=list)

    # Metadatos
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def add_lab_result(self, result: LabResult) -> None:
        """Añade un resultado de laboratorio"""
        self.lab_results.append(result)
        self.last_updated = datetime.now()

    def get_latest_lab(self, test_name: str) -> Optional[LabResult]:
        """Obtiene el último valor de un test específico"""
        matching = [r for r in self.lab_results if r.test_name == test_name]
        if matching:
            return max(matching, key=lambda x: x.date)
        return None

    def get_lab_trend(self, test_name: str, days: int = 30) -> List[LabResult]:
        """Obtiene la tendencia de un test en los últimos días"""
        cutoff = datetime.now() - timedelta(days=days)

        matching = []
        for r in self.lab_results:
            # Manejar tanto datetime como date
            if isinstance(r.date, datetime):
                r_date = r.date
            elif isinstance(r.date, date):
                r_date = datetime.combine(r.date, datetime.min.time())
            else:
                r_date = r.date

            if r.test_name == test_name and r_date >= cutoff:
                matching.append(r)

        return sorted(matching, key=lambda x: x.date)

    def has_condition(self, condition: ConditionType) -> bool:
        """Verifica si el paciente tiene una condición específica"""
        return condition in self.conditions

    def get_active_medications(self) -> List[Medication]:
        """Obtiene medicaciones activas"""
        return [m for m in self.medications if m.is_active]

    def get_critical_values(self) -> List[LabResult]:
        """Obtiene todos los valores críticos actuales"""
        critical = []
        has_irc = self.has_condition(ConditionType.IRC_TERMINAL)

        # Obtener solo los últimos valores de cada test
        test_names = set(r.test_name for r in self.lab_results)
        for test in test_names:
            latest = self.get_latest_lab(test)
            if latest and latest.is_critical(has_irc):
                critical.append(latest)

        return critical

    def get_summary(self) -> Dict[str, Any]:
        """Genera un resumen del estado actual del paciente"""
        return {
            'name': self.name,
            'age': self.age,
            'conditions': [c.value for c in self.conditions],
            'total_labs': len(self.lab_results),
            'unique_tests': len(set(r.test_name for r in self.lab_results)),
            'active_medications': len(self.get_active_medications()),
            'critical_values': len(self.get_critical_values()),
            'latest_update': self.last_updated.strftime('%d/%m/%Y %H:%M')
        }


@dataclass
class MedicalQuestion:
    """Pregunta sugerida para el equipo médico"""
    question: str
    priority: str  # 'alta', 'media', 'baja'
    category: str
    context: str
    based_on: Optional[str] = None  # valor o condición que genera la pregunta