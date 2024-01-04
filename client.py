import streamlit as st
import requests

SERVER_URL = 'https://map-model-service-bryanvre.cloud.okteto.net/v1/models/map-model:predict'

import streamlit as st
import requests

SERVER_URL = 'https://map-model-service-bryanvre.cloud.okteto.net/v1/models/map-model:predict'

def make_prediction(inputs):
    predict_request = {'instances': inputs}
    response = requests.post(SERVER_URL, json=predict_request)
    
    if response.status_code == 200:
        prediction = response.json()
        return prediction
    else:
        st.error("Error al obtener predicciones. Por favor, verifica tus datos e intenta nuevamente.")
        return None

def display_predictions(predictions, location_name):
    st.write(f"\nPredicciones para {location_name}:")
    st.write(f"Mayor valor: {predictions[0]}")

def main():
    st.title('Predictor de Números')

    st.header('Ingresar 3 Números')

    num1 = st.text_input('Número 1', value='0.0')
    num2 = st.text_input('Número 2', value='0.0')
    num3 = st.text_input('Número 3', value='0.0')

    if st.button('Predecir'):
        try:
            num1 = float(num1)
            num2 = float(num2)
            num3 = float(num3)
        except ValueError:
            st.error("Por favor, ingresa números válidos.")
            return

        inputs = [
            [num1, num2, num3]
        ]
        predictions = make_prediction(inputs)

        if predictions:
            display_predictions(predictions['predictions'][0], "Resultados")

if __name__ == '__main__':
    main()
