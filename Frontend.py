import streamlit as st
import requests
import plotly.graph_objects as go

# __App configuration: what it renders in the browser tab__
st.set_page_config(page_title="Methanol Synthesis Yield Predictor", page_icon="🏭",layout="centered")

st.markdown(
    """
    <h1 style="text-align:center; color:#1f77b4; font-weight:bold; margin-bottom: 0.5rem;">
        Methanol Synthesis Yield Predictor
    </h1>
    """, unsafe_allow_html=True
)

    
st.markdown("""
    <div style="
        background-color:#d7e9f7; 
        padding: 1.2rem 1.5rem; 
        border-radius: 12px; 
        margin-bottom: 2rem;
        font-size: 1.1rem;
        line-height: 1.5;
        color: #1a3e72; 
        font-weight: 500;
    ">
        <h3 style="margin-bottom: 0.3rem;">
            This app uses reaction conditions to predict the yield of an industrial methanol synthesis process.
        </h3>
        <h5>
  <em>
    The plant operates a double-pass Plug Flow Reactor with 90% methanol removal after the first pass. <br>
    <br>
    <strong>Standard operating ranges:</strong><br>
    • Temperature: 473–573 K<br>
    • Pressure: 50–150 bar<br>
    • Residence Time: 1–30 s<br>
    <br>
    Note: Predictions may be less reliable for inputs outside these standard ranges.<br>
    Note: The maximum achievable methanol yield in this setup is approximately 75%, based on thermodynamic and process constraints.<br><br>
    Please enter your preferred reaction conditions below to obtain the yield prediction ⬇
  </em>
</h5>
""", unsafe_allow_html=True)



# __Input Section__
st.markdown("""
    <h2 style='color:#1f77b4;'>Input Reaction Conditions</h2>
""", unsafe_allow_html=True)

with st.form(key="input_form"):
    col1, col2 = st.columns(2)

    with col1:
        temperature = st.number_input(
            "Temperature (K)", min_value=0.0, step=1.0,
            format="%.1f",
            help="Temperature in Kelvin"
        )
        residence_time_1 = st.number_input(
            "Residence Time 1 (s)", min_value=0.0, step=0.1,
            format="%.2f",
            help="Time spent in first reactor pass"
        )

    with col2:
        pressure = st.number_input(
            "Pressure (bar)", min_value=0.0, step=1.0,
            format="%.1f",
            help="Operating pressure in bars"
        )
        residence_time_2 = st.number_input(
            "Residence Time 2 (s)", min_value=0.0, step=0.1,
            format="%.2f",
            help="Time spent in second reactor pass"
        )

    submit_button = st.form_submit_button(label="🔍 Predict Yield")

# Custom button styling in blue tones
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.6rem 1.2rem;
        font-size: 1.1rem;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #155d8b;
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

def writeup_for_value(value, medium, good):
    if value < medium:
        color = "red"
        msg = "⚠️ Below optimal range — needs adjustment."
    elif value < good:
        color = "orange"
        msg = "🔶 Moderate range — could improve."
    else:
        color = "green"
        msg = "✅ Optimal range — good condition."
    return msg, color

def display_static_gauge(
    value, max_val, medium, good,
    title="Gauge", 
    gauge_height=350,
    gauge_width=350
):
    msg, color = writeup_for_value(value, medium, good)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 18}},
        gauge={
            'axis': {'range': [0, max_val]},
            'bar': {'color': "#457b9d", 'thickness': 0.1},
            'steps': [
                {'range': [0, medium], 'color': "#f28e8e"},
                {'range': [medium, good], 'color': "#f2d388"},
                {'range': [good, max_val], 'color': "#a8ddb5"},
            ],
        }
    ))

    fig.update_layout(height=gauge_height, width=gauge_width)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"<p style='text-align:center;color:{color}; font-size:16px; margin-top:0;'>{msg}</p>", unsafe_allow_html=True)
# --API request
if submit_button:
    if temperature == 0 or pressure == 0 or residence_time_1 == 0 or residence_time_2 == 0:
        st.error("All fields must be non-zero. Please fill in every input.")
    else:
        is_out_of_range = (temperature < 473 or temperature > 573 or pressure < 50 or pressure > 150 or
                           residence_time_1 < 1 or residence_time_1 > 30 or residence_time_2 < 1 or residence_time_2 > 30)
        if is_out_of_range:
            st.warning("Inputs outside standard PFR ranges (Temp 473–573 K, Pressure 50–150 bar, Times 1–30 s). Results may be less reliable.")
    payload = {
        "Temperature (K)": temperature,
        "Pressure (bar)": pressure,
        "Residence Time (s)_1": residence_time_1,
        "Residence Time (s)_2": residence_time_2
    }

    with st.spinner("Sending request to prediction model..."):
        try:
            response = requests.post(
                "https://methanol-yield-prediction.onrender.com/predict",
                json=payload,
                timeout=15
            )
            if response.status_code==200:
                result = response.json()
                predicted_yield = (result["Predicted Percentage yield"])[:-1]
                predicted_yield = float(predicted_yield)

                if predicted_yield >= 65:
                    st.success(
                        f"""
                            🟢 High Yield: {predicted_yield:.2f}% — Excellent synthesis conditions.
                        """)
                elif predicted_yield >= 50:
                    st.warning(
                        f"""
                            🟡 Manageable Yield: {predicted_yield:.2f}% — There’s room for optimization.
                        """)
                else:
                    st.error(
                        f"""
                            🔴 Low Yield: {predicted_yield:.2f}% — Consider adjusting process parameters.
                        """)

                display_static_gauge(predicted_yield, 100, 50, 65, title="Methanol Yield (%)")

                col1, col2 = st.columns(2)

                with col1:
                    display_static_gauge(temperature, 700, 470, 548, title="Temperature (K)")
                with col2:
                    display_static_gauge(pressure, 150, 40, 60, title="Pressure (bar)")

                col3, col4 = st.columns(2)

                with col3:
                    display_static_gauge(residence_time_1, 30, 10, 18, title="Residence Time 1 (s)")
                with col4:
                    display_static_gauge(residence_time_2, 30, 5, 10, title="Residence Time 2 (s)")

            elif response.status_code==400:
                st.error("All fields are required. Kindly fill in every input.")

            else:    
                st.error(f"❌ Prediction failed. Server returned status code {response.status_code}.")
        except requests.exceptions.ReadTimeout:
            st.warning("⏳ The server took too long to respond — likely waking up. Please try again in a few seconds.")

st.markdown("""
<div style='
    background-color:#f0f4f8;
    border-left: 5px solid #1f77b4;
    padding: 1rem;
    margin-top: 2rem;
    font-size: 0.95rem;
    color: #1a3e72;
'>
<strong>Note:</strong> This model was trained on a synthetically generated dataset simulating a double-pass Plug Flow Reactor (PFR) with 90% methanol removal after the first pass. The dataset contains 5000 samples, generated using a kinetic model based on the <em>Langmuir–Hinshelwood rate law</em>, ensuring realistic prediction of methanol yield under industrial conditions.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='
    background-color:#f0f4f8;
    border-left: 5px solid #1f77b4;
    padding: 1rem;
    margin-top: 2rem;
    font-size: 0.95rem;
    color: #1a3e72;'>
    <strong>Model Performance:</strong><br>
    • Algorithm: Random Forest Regressor<br>
    • R² Score: 0.9872<br>
    • RMSE: 0.0060<br>
    • Training Data: 5000 simulated data points<br>
    • Kinetic Model: Based on Langmuir–Hinshelwood mechanism (as noted above)<br><br>
    This indicates that the model explains 98.72% the variance in yield predictions, with very low error.
    The small RMSE value confirms that the model's predicted yields closely match the actual (simulated) values.
</div>
""", unsafe_allow_html=True) 