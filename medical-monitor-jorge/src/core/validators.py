"""
Validadores y rangos de referencia para valores médicos.
Incluye rangos normales y ajustados para IRC.
"""

from typing import Dict, Tuple, Optional
from .models import AlertLevel


class MedicalValidator:
    """Validador de valores médicos con rangos de referencia"""

    # Rangos de referencia normales
    NORMAL_RANGES = {
        # Química básica
        'creatinine': (0.6, 1.3, 'mg/dL'),
        'urea': (10, 50, 'mg/dL'),
        'glucose': (70, 100, 'mg/dL'),
        'uric_acid': (3.5, 7.2, 'mg/dL'),

        # Electrolitos
        'sodium': (135, 145, 'mEq/L'),
        'potassium': (3.5, 5.1, 'mEq/L'),
        'chloride': (98, 107, 'mEq/L'),
        'calcium': (8.5, 10.5, 'mg/dL'),
        'phosphorus': (2.5, 4.5, 'mg/dL'),
        'magnesium': (1.6, 2.6, 'mg/dL'),

        # Perfil hepático
        'alt': (0, 40, 'U/L'),
        'ast': (0, 40, 'U/L'),
        'alkaline_phosphatase': (40, 130, 'U/L'),
        'gamma_gt': (0, 50, 'U/L'),
        'bilirubin_total': (0.3, 1.2, 'mg/dL'),
        'bilirubin_direct': (0, 0.3, 'mg/dL'),
        'albumin': (3.5, 5.0, 'g/dL'),

        # Hemograma
        'hemoglobin_male': (13.5, 17.5, 'g/dL'),
        'hemoglobin_female': (12.0, 15.5, 'g/dL'),
        'hematocrit_male': (40, 54, '%'),
        'hematocrit_female': (36, 48, '%'),
        'platelets': (150000, 450000, '/mm³'),
        'wbc': (4000, 11000, '/mm³'),

        # Lípidos
        'cholesterol_total': (0, 200, 'mg/dL'),
        'cholesterol_ldl': (0, 130, 'mg/dL'),
        'cholesterol_hdl': (40, 999, 'mg/dL'),
        'triglycerides': (0, 150, 'mg/dL'),

        # Hormonas tiroideas
        'tsh': (0.4, 4.2, 'mIU/L'),
        't4_free': (0.9, 1.7, 'ng/dL'),
        't3': (0.8, 2.0, 'ng/mL'),

        # Otros
        'pth': (15, 65, 'pg/mL'),
        'ferritin_male': (30, 400, 'ng/mL'),
        'ferritin_female': (15, 200, 'ng/mL'),
        'b12': (200, 900, 'pg/mL'),
        'folate': (3, 17, 'ng/mL'),
    }

    # Rangos ajustados para IRC
    IRC_RANGES = {
        'hemoglobin': (10.0, 11.5, 'g/dL'),  # Objetivo en IRC
        'potassium': (3.5, 5.5, 'mEq/L'),  # Ligeramente más alto tolerado
        'phosphorus': (3.5, 5.5, 'mg/dL'),  # Más alto en IRC
        'pth': (150, 300, 'pg/mL'),  # 2-9x el límite superior normal
        'calcium': (8.4, 9.5, 'mg/dL'),  # Ligeramente más bajo
        'albumin': (3.5, 4.0, 'g/dL'),  # Puede estar más bajo
    }

    # Valores críticos que requieren acción inmediata
    CRITICAL_VALUES = {
        'potassium': (2.5, 6.5, 'Arritmia cardíaca'),
        'sodium': (120, 160, 'Alteración neurológica'),
        'glucose': (50, 400, 'Hipoglicemia/Cetoacidosis'),
        'calcium': (6.5, 13.0, 'Tetania/Arritmia'),
        'hemoglobin': (7.0, 20.0, 'Transfusión/Policitemia'),
        'platelets': (20000, 1000000, 'Sangrado/Trombosis'),
        'tsh': (0.01, 100, 'Crisis tiroidea'),
        'creatinine': (0, 10, 'Falla renal aguda'),
    }

    @classmethod
    def validate_value(cls, test_name: str, value: float,
                       has_irc: bool = False, is_male: bool = True) -> Dict:
        """
        Valida un valor de laboratorio contra rangos de referencia.

        Args:
            test_name: Nombre del test
            value: Valor a validar
            has_irc: Si el paciente tiene IRC
            is_male: Sexo del paciente

        Returns:
            Dict con validación y nivel de alerta
        """
        # Ajustar nombre del test según sexo si aplica
        if test_name == 'hemoglobin':
            test_key = 'hemoglobin_male' if is_male else 'hemoglobin_female'
        elif test_name == 'hematocrit':
            test_key = 'hematocrit_male' if is_male else 'hematocrit_female'
        elif test_name == 'ferritin':
            test_key = 'ferritin_male' if is_male else 'ferritin_female'
        else:
            test_key = test_name

        # Obtener rangos
        if has_irc and test_name in cls.IRC_RANGES:
            min_val, max_val, unit = cls.IRC_RANGES[test_name]
            range_type = 'IRC'
        elif test_key in cls.NORMAL_RANGES:
            min_val, max_val, unit = cls.NORMAL_RANGES[test_key]
            range_type = 'Normal'
        else:
            return {
                'valid': True,
                'alert_level': AlertLevel.NORMAL,
                'message': 'Sin rango de referencia disponible'
            }

        # Verificar valores críticos primero
        if test_name in cls.CRITICAL_VALUES:
            crit_min, crit_max, consequence = cls.CRITICAL_VALUES[test_name]
            if value < crit_min or value > crit_max:
                return {
                    'valid': False,
                    'alert_level': AlertLevel.CRITICO,
                    'message': f'CRÍTICO: {consequence}',
                    'range': f'{min_val}-{max_val} {unit}',
                    'range_type': range_type,
                    'value': value,
                    'unit': unit
                }

        # Validar contra rangos normales/IRC
        if value < min_val:
            percent_diff = abs((value - min_val) / min_val * 100)
            if percent_diff > 50:
                alert = AlertLevel.ALERTA
            elif percent_diff > 20:
                alert = AlertLevel.ATENCION
            else:
                alert = AlertLevel.ATENCION
            message = f'Bajo ({value:.2f} < {min_val} {unit})'
        elif value > max_val:
            percent_diff = abs((value - max_val) / max_val * 100)
            if percent_diff > 50:
                alert = AlertLevel.ALERTA
            elif percent_diff > 20:
                alert = AlertLevel.ATENCION
            else:
                alert = AlertLevel.ATENCION
            message = f'Alto ({value:.2f} > {max_val} {unit})'
        else:
            alert = AlertLevel.NORMAL
            message = f'Normal ({min_val}-{max_val} {unit})'

        return {
            'valid': alert != AlertLevel.CRITICO,
            'alert_level': alert,
            'message': message,
            'range': f'{min_val}-{max_val} {unit}',
            'range_type': range_type,
            'value': value,
            'unit': unit,
            'in_range': min_val <= value <= max_val
        }

    @classmethod
    def get_reference_range(cls, test_name: str, has_irc: bool = False,
                           is_male: bool = True) -> Optional[Tuple[float, float, str]]:
        """Obtiene el rango de referencia para un test"""
        # Ajustar según sexo
        if test_name == 'hemoglobin':
            test_key = 'hemoglobin_male' if is_male else 'hemoglobin_female'
        elif test_name == 'hematocrit':
            test_key = 'hematocrit_male' if is_male else 'hematocrit_female'
        elif test_name == 'ferritin':
            test_key = 'ferritin_male' if is_male else 'ferritin_female'
        else:
            test_key = test_name

        # Priorizar rangos IRC si aplica
        if has_irc and test_name in cls.IRC_RANGES:
            return cls.IRC_RANGES[test_name]
        elif test_key in cls.NORMAL_RANGES:
            return cls.NORMAL_RANGES[test_key]

        return None

    @classmethod
    def suggest_tests_for_condition(cls, condition: str) -> Dict[str, str]:
        """Sugiere tests relevantes para una condición"""
        suggestions = {
            'irc': {
                'creatinine': 'Función renal',
                'urea': 'Productos de desecho',
                'potassium': 'Riesgo arritmia',
                'phosphorus': 'Balance mineral',
                'calcium': 'Metabolismo óseo',
                'pth': 'Hiperparatiroidismo secundario',
                'hemoglobin': 'Anemia de enfermedad crónica',
                'albumin': 'Estado nutricional'
            },
            'thyroid': {
                'tsh': 'Hormona estimulante de tiroides',
                't4_free': 'Hormona tiroidea libre',
                't3': 'Hormona tiroidea activa'
            },
            'diabetes': {
                'glucose': 'Glucemia',
                'hba1c': 'Control glucémico (3 meses)',
                'creatinine': 'Nefropatía diabética',
                'albumin_urine': 'Microalbuminuria'
            },
            'liver': {
                'alt': 'Daño hepatocelular',
                'ast': 'Daño hepático',
                'alkaline_phosphatase': 'Colestasis',
                'bilirubin_total': 'Función hepática',
                'albumin': 'Síntesis hepática',
                'inr': 'Coagulación'
            }
        }

        return suggestions.get(condition.lower(), {})