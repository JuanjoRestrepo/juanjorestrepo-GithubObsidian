

## Búsqueda Aleatoria - Random Search
[Random Search Tuning](https://machinelearningmastery.com/grid-search-hyperparameters-deep-learning-models-python-keras/)
## Búsqueda con Grilla - Grid Search
[Grid Search Tuning](https://machinelearningmastery.com/grid-search-hyperparameters-deep-learning-models-python-keras/)
Un poquito más costoso computacionalmente




# Ejemplos búsqueda hiperparámetros básico

Haremos uso de la API Sequential de Keras

```python
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.utils import plot_model
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from keras_tuner import RandomSearch
```
Se carga la base de datos y se divide en los conjunto de entrenamiento y prueba. Además, se divide el train en validation
```python
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size = 0.1)

# Print respectivamente
# x_train.shape, y_train.shape, x_val.shape, y_val.shape
# (54000, 28, 28) (54000,) (6000, 28, 28) (6000,)
```

Definimos el modelo con los hiperparámetros

```python
def build_model(hp):
	model = Sequential()
	model.add(Dense(units = hp.Choice('units1', [256, 512]), input_shape = (784, ), activation = hp.Choice('activation1', ['relu', 'sigmoid'])))
	
	model.add(Dense(units = hp.Choice('units2', [256, 512]), activation = hp.Choice('activation2', ['relu', 'sigmoid'])))
	
	model.add(Dense(10, activation = 'softmax'))
	
	optimizer = tf.keras.optimizers.SGD(hp.Choice('learning_rate', [0.01, 0.001]))
	model.compile(loss='sparse_categorical_crossentropy', optimizer = optimizer, metrics = ['accuracy'])
	return model
```
**Observaciones de la construcción del modelo:**
- `hp.choice:` Hiperparameter choice. 
- Tenemos un modelo con 2 capas ocultas y 1 de salida
- La de salida tiene 10 neuronas porque son 10 clases.
- Si es multiclase, la activacion es **softmax**
- En la capa de entrada, siempre entran las **caracteristicas/features**
- `hp.Choice('units1', [256, 512])`: los valores son potencias de base dos ($2^n$), pero no es obligatorio hacerlo en potencias de base $2^n$, pues son valores libres, 


```python
tuner = RandomSearch(build_model, objective = 'val_loss', max_trials = 10)

tuner.search(x_train_flat, y_train, epochs = epochs, validation_data = (x_val_flat, y_val), verbose=2)

best_model = tuner.get_best_models()[0]
```
**Observaciones pruebas de hiperparametros:**
- `max_trials` son las combinaciones máximas. Las combinaciones de prueba entre hiperparámetros
- `sparse_categorical_crossentropy`: es la función de activación. Cuando es multiclase, se usa categórica. La diferencia con `categorical_crossentropy` dependerá de la forma en como la **DB esté etiquetada** 
	En el caso esta base de datos, es de tipo `sparse` porque las etiquetas son de forma natural, es decir, son números. Son 60,000 datos de los cuales, las posibles clases son solo **10 números naturales**
	
     El etiquetado `One-Hot` convierte los valores *naturales/categóricos* en valores *binarios/booleanos*
- `binary_crossentropy` biclases

#### En conclusión:
- Si el etiquetado es ***natural***, se usa `sparse_categorical`
- Si el etiquetado es ***One Hot***, se usa `categorical`