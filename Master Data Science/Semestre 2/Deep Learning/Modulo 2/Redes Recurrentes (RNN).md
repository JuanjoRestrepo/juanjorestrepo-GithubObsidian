

![[Pasted image 20250608111441.png]]

- Se aplican para datos secuenciales (Uno detrás de otro), como
	- Audio
	- Video
	- Texto
	- Series de tiempo
- Cualquier tipo de dato secuencial, debe ser trabajado diferentemente
- Las **capas ocultas tienen recurrencias**, es decir, información anterior una tras de otra
- Los módulos $h_n$ guarda información desde el final hasta el inicio


## Que es una RNN?

![[Pasted image 20250608112330.png]]


- Se puede entender como un modelo basado en un perceptron multicapa (basado en neuronas)
- La diferencia es que $h_n$ ya no solo depende de $X_n$ sino también de $h_{n-1}$ , es decir, depende tanto del modulo oculto anterior, tanto de su entrada **$X$
	- Ejemplo: $h_2$ depende tanto del modulo oculto $h_1$ y de $X_2$ 
- Estos modelos **son mas grandes, porque tienen mas parámetros**


#### Se pueden hacer modelos Recurrentes con mas capas ocultas?

Si!, son conocidas como **Redes Recurrentes Profundas (RDNN)** 

![[Pasted image 20250608112838.png]]

Sin embargo, normalmente estos modelos no suelen ser muy profundos porque **tienen un costo computacional muy alto**, al tener muchos **parámetros, son muy pesados**


### Matemáticamente, se trabaja igual que el Perceptron Multicapa


![[Pasted image 20250608113118.png]]

### NOTA: 
- SI EL PROBLEMA ES NO LINEAL, SE APLICA FUNCION DE ACTIVACION


## Variaciones de las Redes Recurrentes

**![[Pasted image 20250608113223.png]]**

- En la primera, es una reseña, un comentario sobre una película
- La entrada, que es un **texto, debe ser codificada**


### Los tipo de Arquitecturas

#### 1. Many to One
- La primera de la izquierda, porque **tiene muchas entradas y solo hay una salida**
#### 2. One to Many
- La de la derecha, porque **tiene una sola entrada y muchas salidas**


![[Pasted image 20250608113606.png]]

#### 1. Many to Many
- La primera de la izquierda, porque **tiene muchas entradas y muchas salidas**
- En el ejemplo, tenemos una oración, y podríamos hacer que nos **identifique/clasifique si el texto (la entrada) es un nombre propio**
- Da salidas directas (Hay una **correlación uno a uno**)
- 
#### 2. Many to Many 2.0
- En la derecha, tenemos un variación en donde **la entrada no nos da una salida directa**
- **No hay una correlación uno a uno**
- Una posible **aplicación** de este caso, es en **la traducción, cuando entra un texto y sale otro texto**
	- Por ejemplo, si la entrada es en español **tiene 20 palabras (entradas), las salidas no necesariamente serán 20 palabras**
	- Al día de hoy, todos los traductores están basados en **transformers**


## Unidades Recurrentes con Compuerta (GRU)

![[Pasted image 20250608114331.png]]

- Es una evolución de las RNN
- Tiene compuertas (Lo moradito)
	- Son operaciones matemáticas y funciones de activación
	- Permiten pasar información inmediata o actual. Le da prioridad a la información que viene
	- Puede que $X_t$ entregue mas información a la secuencialidad que $h_{t-1}$

![[Pasted image 20250608115410.png]]


![[Pasted image 20250608115506.png]]

![[Pasted image 20250608115514.png]]

## Calculo final (ht ^ es el candidato)

![[Pasted image 20250608115527.png]]

![[Pasted image 20250608115553.png]]

## Long Short-Term Memory (LSTM)

![[Pasted image 20250608120009.png]]

- Tiene 3 entradas y 2 salidas
- Hay mas compuertas

![[Pasted image 20250608120217.png]]

![[Pasted image 20250608120230.png]]

![[Pasted image 20250608120325.png]]

![[Pasted image 20250608120331.png]]

