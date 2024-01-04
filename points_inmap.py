import numpy as np
import os
import pandas as pd
import tensorflow as tf

# Función para generar datos de tiempo de espera de una sucursal
def tiempos_espera(num_datos=500000, media=15, desviacion=5):
    # Genera tiempos de espera utilizando una distribución normal
    tiempos = np.abs(np.random.normal(media, desviacion, size=num_datos))
    
    # Redondea los tiempos a números enteros
    tiempos = np.round(tiempos).astype(int)

    # Crea un DataFrame con los tiempos de espera
    df = pd.DataFrame({'tiempo_espera': tiempos})
    return df

# Genera datos de tiempo de espera para una sucursal
datos_sucursal = tiempos_espera(num_datos=200, media=20, desviacion=7)

# Dividir el conjunto de datos en entrenamiento, prueba y validación
train_end = int(0.6 * len(datos_sucursal))
test_start = int(0.8 * len(datos_sucursal))
X_train, y_train = datos_sucursal.index.values[:train_end], datos_sucursal['tiempo_espera'][:train_end].values
X_test, y_test = datos_sucursal.index.values[test_start:], datos_sucursal['tiempo_espera'][test_start:].values
X_val, y_val = datos_sucursal.index.values[train_end:test_start], datos_sucursal['tiempo_espera'][train_end:test_start].values

# Limpia cualquier modelo o capa previamente definida en TensorFlow
tf.keras.backend.clear_session()

# Define un modelo de red neuronal con capas densas
linear_model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=2, input_shape=[1], activation='relu', name='Dense_1_4'),
    tf.keras.layers.Dense(units=4, activation='relu', name='Dense_4_8'),
    tf.keras.layers.Dense(units=8, activation='relu', name='Dense_8_1'),
    tf.keras.layers.Dense(units=1, activation='linear', name='Output')
])

# Compila el modelo especificando el optimizador, la función de pérdida y las métricas
linear_model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mean_squared_error', metrics=['mae', 'mse'])

# Imprime un resumen del modelo, mostrando la arquitectura y el número de parámetros
print(linear_model.summary())

# Entrena el modelo con los conjuntos de entrenamiento y validación durante 300 épocas
linear_model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=300)

# Guarda el modelo entrenado en el directorio 'linear-model/1/'
export_path = 'wait-time-model/1/'  # Cambia el número del modelo si es necesario
tf.saved_model.save(linear_model, os.path.join('./', export_path))

