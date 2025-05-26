# Methanol Synthesis Yield Predictor (Frontend)

## Overview
This repository contains the frontend code for the Methanol Synthesis Yield Predictor, a Streamlit-based web application. It allows users to input reaction conditions and receive real-time predictions of methanol yield, powered by a machine learning model hosted on a separate FastAPI backend.

## Features
- Interactive input fields for reaction conditions (Temperature, Pressure, Residence Times).
- Real-time yield predictions with visual feedback (gauges, success/warning/error messages).
- Warnings for inputs outside standard operating ranges.
- Customizable theme for a professional look.

--- 

## Important Note on Yield Limit

- The maximum achievable methanol yield in this process setup is approximately **75%**.
- This is based on thermodynamic and process constraints of the double-pass PFR with 90% methanol removal after the first pass.
- Predictions close to this value are expected under optimal conditions.

---

## Screenshots of app
**Picture 1**
![Output1](https://github.com/AsuquoAA/Methanol-Yield-Prediction_Frontend/blob/main/Screenshot%202025-05-26%20at%2020.50.46.png)

-

**Picture2**
![Output2](https://github.com/AsuquoAA/Methanol-Yield-Prediction_Frontend/blob/main/Screenshot%202025-05-26%20at%2020.51.18.png)

---
  
## **Setup Instructions**

```sh
pip install -r requirements.txt

```
### How to run this project
Clone the Repository:
git clone https://github.com/AsuquoAA/methanol-yield-frontend.git
cd Methanol_Yield_Prediction_Frontend

---

### **Run the Streamlit App**
```sh
streamlit run Frontend.py
```

### **Make Predictions**
- Enter sensor readings in the **Input Reaction Conditions** box.
- Click **Predict Yield**.
- View **Predicted Status & Visualizations**.

---


## Update API URL:  
API_URL = "https://methanol-yield-prediction.onrender.com"


## Deployment
Deployed on Streamlit Community Cloud.  
Connect your GitHub repository and select `Frontend.py` as the entry point.

## License
This project is licensed under the MIT License. The MIT License is a permissive open-source license that lets others use, modify, and share your code freely, as long as they include the original license and copyright notice. For a personal project like this, it means your work can be shared widely while still recognizing you as the creator.
