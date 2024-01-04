import streamlit as st
import requests

SERVER_URL = 'https://map-model-service-bryanvre.cloud.okteto.net/v1/models/wait-time-model:predict'

def make_prediction(inputs):
    predict_request = {'instances': [inputs]}
    response = requests.post(SERVER_URL, json=predict_request)
    
    if response.status_code == 200:
        prediction = response.json()
        return prediction
    else:
        st.error("Error al obtener predicciones. Por favor, verifica tus datos e intenta nuevamente.")
        return None

def display_predictions(prediction):
    result = prediction['predictions'][0]['dense_1']
    st.write(f"\nEl tiempo de espera estimado es: {result} minutos")

def main():
    st.title('Predictor de Tiempo de Espera')

    st.header('Ingresar Tiempo de Espera de Clientes Anteriores')

    cliente1 = st.text_input('Cliente 1 (minutos)', value='0')
    cliente2 = st.text_input('Cliente 2 (minutos)', value='0')

    if st.button('Predecir'):
        try:
            cliente1 = float(cliente1)
            cliente2 = float(cliente2)
        except ValueError:
            st.error("Por favor, ingresa tiempos de espera válidos en minutos.")
            return

        inputs = [cliente1, cliente2]
        prediction = make_prediction(inputs)

        if prediction:
            display_predictions(prediction)

if __name__ == '__main__':
    main()
