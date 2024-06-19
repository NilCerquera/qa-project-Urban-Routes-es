                           Proyecto Urban Routes.

Script 8 Automatización de pruebas de la aplicación web

1. Descripción del Proyecto
Este proyecto vamos a automatizar el paso a paso para pedir un taxi y completar los items requeridos por la página web para concluir con el pedido satisfactoriamente.

2. Documentación y requisitos antes de realizar la prueba:
Python: Requerimos usar Python para realizar las pruebas
Pytest: DNecesitamos descargar pytest para ejecutar las pruebas en el proyecto
Selenium WebDriver: Requerimos descargar Selenium y su controlador para realizar las pruebas correspondientes
Localizadores: en este caso requerimos los siguientes localizadores (ID - CLASS_NAME - XPATH - CSS_SELECTOR) para ubicar en la pagina web mediante la inspección de html usando Google e interactuar con los elementos

3. Tecnologías Utilizadas
Python: Usamos esta herramienta para poder efectuar las pruebas automatizadas correspondientes a la aplicación

PyCharm es un entorno de desarrollo integrado (IDE) utilizado en el lenguaje de la progrmación 

Selenium es un conjunto de herramientas y bibliotecas de software utilizado principalmente para la automatización de pruebas en aplicaciones web. 

Estructuración de pruebas automatizadas mediante POM.
Configuración y limpieza utilizando setup_class que genera el entorno de la prueba inicial, luego configurando el WebDriver y el comando teardown_class para finalizar las pruebas y limpiar el uso del controlador.

Inivio
Clonar el Repositorio de github

El primer paso es clonar el proyecto original y trabajar en local para realizar dichas pruebasm podemos utilizar el siguiente comando:

git clone git@github.com:NilCerquera/qa-project-Urban-Grocers-es.git "Para otro usuario, deberá modificar NilCerquera y dejar el usuario correspondiente"

Posterior a esto, configuramos pycharm y localizamos la carpeta donde se guaró nuestro proyecto, ahora bien, iniciamos el proyecto


4. Configurar Entorno de Pruebas

Inicialmente instalamos Pytest y selenium, ejecutamos los siguientes comandos:

pip install pytest
pip install selenium

5. Ejecutar el Proyecto

Antes de ejecutar las pruebas, debemos actualizar la URL ya que pierde su ubicacion y es necesario refrescar la URL

Actualizas la url copiandolo en data, modificas la variable urban_routes_url actualizando entre '', la nueva URL

Declaras los localizadores por acción que requerimos para el entorno, en resumen sería lo siguiente para seguir el proceso de las pruebas automatizadas

1) Localiza el cuadro de texto "Desde" 
2) Ingresa la dirección "desde"
3) Localiza el cuardo de texto " Hasta"
4) Ingresa la dirección "Hasta"
5) Localiza el botó pedir taxi
6) Click en el botó pedir taxi
7) Localiza la opción "Comfort"
8) Click en la opción comfort
9) Localiza el cuadro "Número de teléfono"
10) Click en el botón "Número de telefono
11) agrega el número de telefono
12) Localiza el bóton " Confirmar"
13) Presiona el boton "Confirmar
14) Localiza el botón "codigo"
15) Agrega el codigo enviado con la funcion otorgada en el proyecto inicial
16) Localiza el boton "Confirmar" 
17) Presiona el botón " Confirmar"
18) Localiza el objeto "Método de pago"
19) Selecciona el botón "Metodo de pago"
20) Localiza el cuadro "Agregar tarjeta"
21) Presiona el botón agregar tarjeta
22) Localiza el cuadro "Número de tarjeta"
23) Ingresa el número de tarjeta
24) Localiza el cuadro "Codigo tarjeta"
25) Ingresa el número de codigo
26) en este caso, debes hacer un click en el boton TAB en cada cuadro para que se active el boton agregar
27) Localiza el boton agregar
28) Presiona el botó agregar
29) Localiza el cuadro "X"
30) Presiona click en la x
31) Localiza el slider Mantas y pañuelos
32) oprimes el slider para activar la opción
33) Localiza la opcion helado
34) Agregas 2 helados al pedido
35) Localiza pedir el botón pedir taxi
36) Presiona el botón pedir taxi
37) Espera que se acabe el temporizador para conocer los detalles del pedido

Para comprobar las pruebas automatizadas, requerimos usar assert para comprobar los resultados esten acordes con lo requerido de las pruebas.

6. Ejecución de pruebas

pytest main.py
Asegúrate de revisar y actualizar los requisitos del proyecto.


Cordialmente

Nilton Cerquera
QA engineer
