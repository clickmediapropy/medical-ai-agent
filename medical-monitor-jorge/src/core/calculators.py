"""
Calculadoras médicas para el sistema de monitoreo.
Basadas en evidencia médica actual y guías clínicas.
"""

from typing import Dict, Optional, Tuple
import math


class MedicalCalculator:
    """Calculadoras médicas especializadas"""

    @staticmethod
    def egfr_ckdepi_2021(creatinine: float, age: int, is_female: bool) -> Dict:
        """
        Calcula la Tasa de Filtración Glomerular estimada usando CKD-EPI 2021.
        Esta es la fórmula sin factor racial, recomendada por NKF/ASN.

        Args:
            creatinine: Creatinina sérica en mg/dL
            age: Edad en años
            is_female: True si es mujer

        Returns:
            Dict con eGFR y clasificación
        """
        if creatinine <= 0 or age <= 0:
            return {'error': 'Valores inválidos'}

        # Constantes según sexo
        if is_female:
            k = 0.7
            alpha = -0.241
            factor = 1.012
        else:
            k = 0.9
            alpha = -0.302
            factor = 1.0

        # Cálculo CKD-EPI 2021
        min_cr_k = min(creatinine / k, 1)
        max_cr_k = max(creatinine / k, 1)

        egfr = 142 * (min_cr_k ** alpha) * (max_cr_k ** -1.200) * (0.9938 ** age) * factor
        egfr = round(egfr, 1)

        # Clasificación de ERC
        if egfr >= 90:
            stage = "G1 - Normal o alta"
            color = "green"
        elif egfr >= 60:
            stage = "G2 - Levemente disminuida"
            color = "yellow"
        elif egfr >= 45:
            stage = "G3a - Moderadamente disminuida"
            color = "orange"
        elif egfr >= 30:
            stage = "G3b - Moderadamente a severamente disminuida"
            color = "orange"
        elif egfr >= 15:
            stage = "G4 - Severamente disminuida"
            color = "red"
        else:
            stage = "G5 - Falla renal (requiere diálisis)"
            color = "red"

        return {
            'egfr': egfr,
            'stage': stage,
            'color': color,
            'unit': 'mL/min/1.73m²',
            'interpretation': f"TFGe de {egfr} mL/min/1.73m² indica {stage}",
            'requires_dialysis': egfr < 15
        }

    @staticmethod
    def sofa_score(data: Dict) -> Dict:
        """
        Calcula el Sequential Organ Failure Assessment (SOFA) Score.
        Predictor de mortalidad en UCI.

        Args:
            data: Dict con parámetros clínicos

        Returns:
            Dict con score y componentes
        """
        score = 0
        components = {}

        # Sistema respiratorio (PaO2/FiO2)
        if 'pao2_fio2' in data:
            ratio = data['pao2_fio2']
            if ratio < 100:
                components['respiratory'] = 4
            elif ratio < 200:
                components['respiratory'] = 3
            elif ratio < 300:
                components['respiratory'] = 2
            elif ratio < 400:
                components['respiratory'] = 1
            else:
                components['respiratory'] = 0
            score += components['respiratory']

        # Sistema renal (creatinina)
        if 'creatinine' in data:
            cr = data['creatinine']
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
            score += components['renal']

        # Coagulación (plaquetas)
        if 'platelets' in data:
            plt = data['platelets'] / 1000  # convertir a x10^3/mm3
            if plt < 20:
                components['coagulation'] = 4
            elif plt < 50:
                components['coagulation'] = 3
            elif plt < 100:
                components['coagulation'] = 2
            elif plt < 150:
                components['coagulation'] = 1
            else:
                components['coagulation'] = 0
            score += components['coagulation']

        # Hepático (bilirrubina)
        if 'bilirubin' in data:
            bil = data['bilirubin']
            if bil >= 12.0:
                components['hepatic'] = 4
            elif bil >= 6.0:
                components['hepatic'] = 3
            elif bil >= 2.0:
                components['hepatic'] = 2
            elif bil >= 1.2:
                components['hepatic'] = 1
            else:
                components['hepatic'] = 0
            score += components['hepatic']

        # Cardiovascular (hipotensión)
        if 'map' in data:  # Mean Arterial Pressure
            map_val = data['map']
            if map_val < 70:
                components['cardiovascular'] = 1
            else:
                components['cardiovascular'] = 0
            score += components['cardiovascular']

        # Neurológico (Glasgow)
        if 'glasgow' in data:
            gcs = data['glasgow']
            if gcs < 6:
                components['neurological'] = 4
            elif gcs < 10:
                components['neurological'] = 3
            elif gcs < 13:
                components['neurological'] = 2
            elif gcs < 15:
                components['neurological'] = 1
            else:
                components['neurological'] = 0
            score += components['neurological']

        # Interpretación
        if score >= 15:
            mortality = ">80%"
            risk = "Muy Alto"
        elif score >= 11:
            mortality = "40-50%"
            risk = "Alto"
        elif score >= 7:
            mortality = "15-20%"
            risk = "Moderado"
        elif score >= 3:
            mortality = "10%"
            risk = "Bajo"
        else:
            mortality = "<10%"
            risk = "Muy Bajo"

        return {
            'total_score': score,
            'components': components,
            'mortality_risk': mortality,
            'risk_level': risk,
            'interpretation': f"SOFA Score de {score} indica riesgo {risk.lower()} con mortalidad estimada {mortality}"
        }

    @staticmethod
    def thyroid_crisis_risk(tsh: float, t4_libre: Optional[float] = None,
                           temperature: Optional[float] = None,
                           mental_status: Optional[str] = None) -> Dict:
        """
        Evalúa el riesgo de crisis mixedematosa.

        Args:
            tsh: Valor de TSH en mIU/L
            t4_libre: T4 libre en ng/dL
            temperature: Temperatura en °C
            mental_status: Estado mental ('normal', 'confuso', 'somnoliento', 'estuporoso')

        Returns:
            Dict con evaluación de riesgo
        """
        risk_score = 0
        risk_factors = []
        recommendations = []

        # TSH extremadamente elevado (valores corregidos para rangos clínicos reales)
        # Normal: 0.4-4.0 mIU/L
        if tsh > 50:  # Extremadamente elevado
            risk_score += 60
            risk_factors.append(f'TSH CRÍTICO: {tsh:.1f} mIU/L (>50)')
            recommendations.append('URGENTE: Consultar endocrinólogo inmediatamente')
            recommendations.append('Considerar levotiroxina IV')
        elif tsh > 20:  # Muy elevado
            risk_score += 40
            risk_factors.append(f'TSH muy elevado: {tsh:.1f} mIU/L')
            recommendations.append('Ajuste urgente de levotiroxina')
        elif tsh > 10:  # Elevado
            risk_score += 20
            risk_factors.append(f'TSH elevado: {tsh:.1f} mIU/L')
            recommendations.append('Aumentar dosis de levotiroxina')

        # T4 libre bajo
        if t4_libre is not None:
            if t4_libre < 0.5:
                risk_score += 30
                risk_factors.append(f'T4 libre muy bajo: {t4_libre} ng/dL')
            elif t4_libre < 0.9:
                risk_score += 20
                risk_factors.append(f'T4 libre bajo: {t4_libre} ng/dL')

        # Hipotermia
        if temperature is not None:
            if temperature < 35:
                risk_score += 30
                risk_factors.append(f'Hipotermia: {temperature}°C')
            elif temperature < 36:
                risk_score += 15
                risk_factors.append(f'Temperatura baja: {temperature}°C')

        # Estado mental
        if mental_status:
            if mental_status in ['estuporoso', 'comatoso']:
                risk_score += 40
                risk_factors.append('Alteración severa del estado mental')
            elif mental_status in ['confuso', 'somnoliento']:
                risk_score += 20
                risk_factors.append('Alteración moderada del estado mental')

        # Factores adicionales en contexto UCI/TCE
        if mental_status in ['estuporoso', 'comatoso'] and tsh > 50:
            risk_score += 10  # Puntos adicionales por combinación crítica
            risk_factors.append('COMBINACIÓN CRÍTICA: Estado mental alterado + TSH muy elevado')
            recommendations.append('⚠️ ALTO RIESGO: TCE + Hipotiroidismo severo')

        # Evaluación final
        if risk_score >= 70:
            level = 'CRÍTICO'
            color = 'red'
            recommendations.extend([
                'Iniciar protocolo de crisis mixedematosa',
                'Hidrocortisona 100mg IV ANTES del reemplazo tiroideo',
                'Levotiroxina 200-400mcg IV de carga (o aumentar dosis SNG)',
                'Monitoreo continuo en UCI',
                'PRECAUCIÓN: El edema cerebral puede empeorar con tratamiento rápido'
            ])
        elif risk_score >= 40:
            level = 'ALTO'
            color = 'orange'
            recommendations.extend([
                'Evaluación endocrinológica urgente',
                'Considerar inicio de tratamiento',
                'Monitoreo estrecho'
            ])
        elif risk_score >= 20:
            level = 'MODERADO'
            color = 'yellow'
            recommendations.append('Seguimiento endocrinológico cercano')
        else:
            level = 'BAJO'
            color = 'green'

        return {
            'risk_level': level,
            'risk_score': risk_score,
            'color': color,
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'requires_urgent_action': risk_score >= 70
        }

    @staticmethod
    def calcium_pth_analysis(calcium: float, pth: float, phosphorus: Optional[float] = None,
                            has_irc: bool = False) -> Dict:
        """
        Analiza la relación Calcio-PTH-Fósforo.

        Args:
            calcium: Calcio sérico en mg/dL
            pth: PTH en pg/mL
            phosphorus: Fósforo en mg/dL
            has_irc: Si tiene IRC

        Returns:
            Dict con análisis
        """
        findings = []
        interpretation = ""

        # Rangos normales
        ca_normal = (8.5, 10.5)
        pth_normal = (15, 65) if not has_irc else (15, 300)  # Más alto en IRC
        p_normal = (2.5, 4.5) if not has_irc else (3.5, 5.5)  # Más alto en IRC

        # Análisis de calcio
        if calcium > ca_normal[1]:
            if pth > pth_normal[1]:
                findings.append("Hipercalcemia con PTH elevada")
                interpretation = "Posible hiperparatiroidismo primario o terciario"
            else:
                findings.append("Hipercalcemia con PTH normal/baja")
                interpretation = "Investigar otras causas de hipercalcemia"
        elif calcium < ca_normal[0]:
            if pth > pth_normal[1]:
                findings.append("Hipocalcemia con PTH elevada")
                interpretation = "Hiperparatiroidismo secundario (esperado en IRC)"
            else:
                findings.append("Hipocalcemia con PTH inadecuadamente baja")
                interpretation = "Posible hipoparatiroidismo"
        else:
            findings.append("Calcio normal")

        # Análisis de fósforo si está disponible
        if phosphorus is not None:
            if phosphorus > p_normal[1]:
                findings.append("Hiperfosfatemia")
                if has_irc:
                    interpretation += ". Esperado en IRC - considerar quelantes de fósforo"
            elif phosphorus < p_normal[0]:
                findings.append("Hipofosfatemia")

        # Producto calcio-fósforo
        if phosphorus is not None:
            ca_p_product = calcium * phosphorus
            if ca_p_product > 55:
                findings.append(f"Producto Ca×P elevado: {ca_p_product:.1f}")
                interpretation += ". Riesgo de calcificación vascular"

        return {
            'findings': findings,
            'interpretation': interpretation,
            'calcium_status': 'alto' if calcium > ca_normal[1] else 'bajo' if calcium < ca_normal[0] else 'normal',
            'pth_status': 'alto' if pth > pth_normal[1] else 'bajo' if pth < pth_normal[0] else 'normal',
            'requires_treatment': calcium > 11 or (phosphorus and phosphorus > 6.5)
        }

    @staticmethod
    def anemia_evaluation(hemoglobin: float, is_male: bool, has_irc: bool = False) -> Dict:
        """
        Evalúa el grado de anemia.

        Args:
            hemoglobin: Hemoglobina en g/dL
            is_male: True si es hombre
            has_irc: Si tiene IRC (afecta rangos objetivo)

        Returns:
            Dict con evaluación
        """
        # Rangos normales
        if is_male:
            normal_min = 13.5
        else:
            normal_min = 12.0

        # En IRC, objetivo es diferente
        if has_irc:
            target_min = 10.0
            target_max = 11.5

        # Clasificación
        if hemoglobin < 7:
            severity = "Severa"
            color = "red"
            recommendation = "Evaluar necesidad de transfusión"
        elif hemoglobin < 10:
            severity = "Moderada"
            color = "orange"
            recommendation = "Evaluar causas y considerar eritropoyetina si IRC"
        elif hemoglobin < normal_min:
            severity = "Leve"
            color = "yellow"
            recommendation = "Seguimiento y suplementación si indicado"
        else:
            severity = "Sin anemia"
            color = "green"
            recommendation = "Valores normales"

        # Ajuste para IRC
        if has_irc and 10 <= hemoglobin <= 11.5:
            severity = "Objetivo para IRC"
            color = "green"
            recommendation = "En rango objetivo para paciente con IRC"

        return {
            'severity': severity,
            'color': color,
            'value': hemoglobin,
            'recommendation': recommendation,
            'requires_urgent_eval': hemoglobin < 7
        }

    @staticmethod
    def dialysis_adequacy(kt_v: Optional[float] = None, urr: Optional[float] = None) -> Dict:
        """
        Evalúa la adecuación de diálisis.

        Args:
            kt_v: Kt/V (objetivo >1.2)
            urr: Tasa de reducción de urea en % (objetivo >65%)

        Returns:
            Dict con evaluación
        """
        adequacy = "No evaluable"
        color = "gray"
        recommendations = []

        if kt_v is not None:
            if kt_v >= 1.4:
                adequacy = "Excelente"
                color = "green"
            elif kt_v >= 1.2:
                adequacy = "Adecuada"
                color = "green"
            else:
                adequacy = "Inadecuada"
                color = "red"
                recommendations.append("Aumentar tiempo o frecuencia de diálisis")

        elif urr is not None:
            if urr >= 70:
                adequacy = "Excelente"
                color = "green"
            elif urr >= 65:
                adequacy = "Adecuada"
                color = "green"
            else:
                adequacy = "Inadecuada"
                color = "red"
                recommendations.append("Revisar prescripción de diálisis")

        return {
            'adequacy': adequacy,
            'color': color,
            'kt_v': kt_v,
            'urr': urr,
            'recommendations': recommendations
        }