"""
Componentes de visualización y gráficos.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List
from src.core.models import LabResult


def create_trend_chart(results: List[LabResult], test_name: str):
    """
    Crea un gráfico de tendencia para un test específico.

    Args:
        results: Lista de resultados ordenados por fecha
        test_name: Nombre del test

    Returns:
        Figura de Plotly
    """
    dates = [r.date for r in results]
    values = [r.value for r in results]
    unit = results[0].unit if results else ""

    fig = go.Figure()

    # Línea de valores
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        name='Valor',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    ))

    # Añadir rangos de referencia si están disponibles
    if results[0].reference_min is not None and results[0].reference_max is not None:
        fig.add_hline(
            y=results[0].reference_min,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Mínimo normal ({results[0].reference_min})"
        )
        fig.add_hline(
            y=results[0].reference_max,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Máximo normal ({results[0].reference_max})"
        )

        # Área de rango normal
        fig.add_hrect(
            y0=results[0].reference_min,
            y1=results[0].reference_max,
            fillcolor="green",
            opacity=0.1,
            line_width=0
        )

    # Marcar valores críticos
    for i, result in enumerate(results):
        if result.alert_level.value in ['critico', 'alerta']:
            fig.add_annotation(
                x=dates[i],
                y=values[i],
                text="⚠️",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="red"
            )

    fig.update_layout(
        title=f"Tendencia de {test_name}",
        xaxis_title="Fecha",
        yaxis_title=f"Valor ({unit})",
        hovermode='x unified',
        showlegend=True,
        height=400
    )

    return fig


def create_comparison_chart(patient_data, test_names: List[str]):
    """
    Crea un gráfico comparativo de múltiples tests.

    Args:
        patient_data: Datos del paciente
        test_names: Lista de tests a comparar

    Returns:
        Figura de Plotly
    """
    fig = go.Figure()

    for test_name in test_names:
        results = patient_data.get_lab_trend(test_name, days=365)
        if results:
            dates = [r.date for r in results]
            values = [r.value for r in results]

            # Normalizar valores para comparación
            if len(values) > 0:
                max_val = max(values)
                normalized = [v/max_val * 100 for v in values]
            else:
                normalized = values

            fig.add_trace(go.Scatter(
                x=dates,
                y=normalized,
                mode='lines+markers',
                name=test_name
            ))

    fig.update_layout(
        title="Comparación de Tests (Valores Normalizados)",
        xaxis_title="Fecha",
        yaxis_title="Valor Normalizado (%)",
        hovermode='x unified',
        height=400
    )

    return fig


def create_gauge_chart(value: float, min_val: float, max_val: float,
                       title: str, unit: str = "", thresholds: dict = None):
    """
    Crea un gráfico de medidor (gauge).

    Args:
        value: Valor actual
        min_val: Valor mínimo
        max_val: Valor máximo
        title: Título del medidor
        unit: Unidad de medida
        thresholds: Dict con umbrales de colores

    Returns:
        Figura de Plotly
    """
    if thresholds is None:
        thresholds = {
            'low': min_val + (max_val - min_val) * 0.3,
            'medium': min_val + (max_val - min_val) * 0.6,
            'high': max_val
        }

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [min_val, thresholds['low']], 'color': "lightgray"},
                {'range': [thresholds['low'], thresholds['medium']], 'color': "yellow"},
                {'range': [thresholds['medium'], thresholds['high']], 'color': "orange"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_val * 0.9
            }
        }
    ))

    fig.update_layout(height=300)
    return fig


def create_heatmap_correlations(patient_data):
    """
    Crea un mapa de calor de correlaciones entre diferentes tests.

    Args:
        patient_data: Datos del paciente

    Returns:
        Figura de Plotly o None si no hay suficientes datos
    """
    import pandas as pd
    import numpy as np

    # Obtener todos los tests únicos
    test_names = list(set(r.test_name for r in patient_data.lab_results))

    if len(test_names) < 2:
        return None

    # Crear matriz de datos
    data = []
    for test in test_names:
        results = patient_data.get_lab_trend(test, days=365)
        if results:
            values = [r.value for r in results]
            data.append(values[:10])  # Limitar a 10 valores más recientes

    # Si no hay suficientes datos, retornar None
    if len(data) < 2:
        return None

    # Crear DataFrame y calcular correlaciones
    df = pd.DataFrame(data, index=test_names).T
    corr = df.corr()

    # Crear mapa de calor
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index,
        colorscale='RdBu',
        zmid=0,
        text=corr.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Correlación")
    ))

    fig.update_layout(
        title="Correlación entre Tests",
        height=400,
        xaxis={'side': 'bottom'},
        yaxis={'side': 'left'}
    )

    return fig