# Pilla pilla
Paquete de ROS para jugar al pilla pilla con un robot móvil autónomo y visión artificial. 

## Video demo
https://youtube.com/shorts/ZLqL8G-TDak
-----------------------------------------------------------------------------------------------------------------------------------------------------------
  
## Funcionamiento del juego
1. Al ejecutar el programa, se hace una cuenta atrás de 3 segundos para que cada uno de los participantes se coloque en su puesto. Para poder jugar, es importante que las personas que quieran jugar lleven un distintivo de color azul en la pierna, a la altura de debajo de la rodilla aproximadamente.

2. Al acabar la cuenta atrás, el turtlebot empieza a moverse de forma arbitraria por el espacio. En este momento, va deambulando evitando los obstáculos del entorno.

3. Si detecta una persona, deja de deambular y su movimiento se dirige hacia ella. Si consigue acercarse mucho, gana un punto el turtlebot.

4. Si una persona se acerca antes al turtlebot y le toca el sensor del bumper, es la persona la que gana punto.

5. Cada vez que se gana un punto, aparece la puntuación en el terminal.

-----------------------------------------------------------------------------------------------------------------------------------------------------------
  
## Nodos de ROS
```bash
	detect.py: 
```
	Este nodo lee la información que detecta la cámara. Cuando la cámara detecta el color azul, publica en el topic /topic_posicion los mensajes con la información de la región de interés.
	
	follow.py: Este nodo está suscrito al sensor láser para que el robot pueda moverse, al bumper para detectar si el humano ha ganado punto, y a la cámara para saber donde está el humano. Inicialmente va deambulando hasta que el otro nodo le envía la información de que se ha detectado una zona de color azul. Es entonces cuando cambia su rumbo a esa dirección.

-----------------------------------------------------------------------------------------------------------------------------------------------------------
  
## Autores
Álvaro Martínez Martínez y Marina Villanueva Pelayo
Universidad de Alicante 2023
