import math
import streamlit as st

NutrientsToColor = {
    'Calorías': '#8d6e63',
    'Carbohidratos': '#4caf50',
    'Proteínas': '#e53935',
    'Grasas': '#fb8c00',
}
def GetProgressNutrient(
        CurrentValue,
        NutrientLabel,
        Size = 150,
    ):
    MaxValue = st.session_state['MaxNutrientsValues'][NutrientLabel]
    ProgressPercent = min(CurrentValue/MaxValue,1.0)
        
    Radius = 20
    Circumference = 2*math.pi*Radius

    Offset = Circumference-(ProgressPercent*Circumference)
    
    Color = NutrientsToColor[NutrientLabel]
    CircleHTML = f"""
    <div style="display: flex; flex-direction: column; align-items: center;">
        <div style="position: relative; width: {Size}px; height: {Size}px; align-items: center;">
            <svg width="{Size-Radius/2}" height="{Size-Radius/2}" viewBox="3 0 50 50">
                <circle cx="25" cy="25" r="{Radius}" fill="none" stroke="#e0e0e0" stroke-width="4" />
                <circle cx="25" cy="25" r="{Radius}" fill="none" stroke="{Color}" 
                        stroke-width="4" 
                        stroke-dasharray="{Circumference}" 
                        stroke-dashoffset="{Offset}" 
                        stroke-linecap="round"
                        transform="rotate(-90 25 25)" />
            </svg>
            <div style="position: absolute; top: 47%; left: 44%; transform: translate(-50%, -50%); 
                        text-align: center; font-size: 24px; font-weight: bold; color: #333;">
                {int(CurrentValue)}
            </div>
        </div>
    </div>
    """
    return CircleHTML , Color