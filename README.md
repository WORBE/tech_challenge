# Tech Challenge

## Datos del candidato
- Nombre Completo: Wilson Alberto Orbe Diaz
- Titulo: Ingeniero de Sistemas e Informática
- DNI: 45658770
- Correo Electrónico: wilson.orbe@gmail.com


## 1) Coding Challenge

Ruta: /1.CodingChallenge

### A) Code
- Clonar el repositorio (Main).
- Dirigirse a la ruta : /1.CodingChallenge/Code
- Estructura: widget/, host/, backoffice/.
	* Code/
	* └────→ widget/
	* └────→ host/
	* └────→ backoffice/
	
#### BackOffice	
- Configuraremos el BackOffice de la siguiente manera:

	* **Paso 1:** Instalar Python for windows: 
		* Ruta Recomendable: <a href="https://www.python.org/ftp/python/3.14.2/python-3.14.2-amd64.exe" target="_blank">Python3.14.2</a>
		
		* Aqui otras Opciones: <a href="https://www.python.org/downloads/" target="_blank">Python Descargas</a>

	* **Paso 2:** Dirigirse a la carpeta .../1.CodingChallenge/Code/backoffice, y abrir el CMD en esa ruta.
	
	* **Paso 3:** Habilitar el ambiente virtual, ejecutar los siguientes comandos en el siguiente orden:
		- python -m venv venv
		- .\venv\Scripts\activate
	
	* **Paso 4:** Instalar Django, ejecutar el siguiente comando: 
		- pip install django

	* **Paso 5:** Instalar las dependencias que se utilizaron para el proyecto:
		- Django Crispy 				-> pip install django-crispy-forms
		- Crispy-bootstrap5 			-> pip install crispy-bootstrap5
		- Librería para habilitar Cors 	-> pip install django-cors-headers
	 
	* **Paso 5:** Habilitar la aplicación del BackOffice.
		- python manage.py runserver
			
	* **Resultados:**
		- Ruta que se habilitó para ver la aplicación: http://localhost:8000
		- Ruta que se habilitó para el API que validara los cupones: http://localhost:8000/api/validate/, se enviará en formato json los siguientes parametros:
			- order_id: Identificador de la operación
            - order_value: Valor de la operación
            - voucher_code: Cupón
            - secret_code: Código del cupón
	
	* Tambien se habilitó un usuario para la administración de Django:
		- Ruta		-> http://localhost:8000/admin
		- Usuario	-> admin
		- Clave		-> admin
			
#### Widget

- Configuraremos el Widget de la siguiente manera:

	* **Paso 1:** Dirigirse a la carpeta .../1.CodingChallenge/Code/widget, y abrir el archivo  'widget.js'.
	
	* **Paso 2:** Configuramos la constante: **API_VALIDATE** con el valor del api de validar los cupones 'http://localhost:8000/api/validate/'
		- const API_VALIDATE = "http://localhost:8000/api/validate/";
	
	* **Resultados:**
		- Se ingresará el Cupón en el input: <input id="sp_voucher" ...
		- Se ingresará el Código en el input: <input id="sp_code" ...
 	  
#### Host

- Indicaciones para el Host:
	* **Paso 1:** Dirigirse a la carpeta .../1.CodingChallenge/Code/host, y abrir el archivo  'host.html' a modo de edición.
	
	* **Referencia el Widget:** <script src="../widget/widget.js"></script>
	
	* **Se genera un order_id de la siguiente manera:** 'ORDER-' + Date.now()
	
	* **Se genera un order_value aleatorio de 0 a 200:** (Math.random() * (200 - 10) + 10).toFixed(2)
	
	* **Finalmente:** Dirigirse a la carpeta .../1.CodingChallenge/Code/host, y abrir el archivo 'host.html' en un navegador de su preferencia que lea HTML5 .
	
### B) Wireframe

* **Archivo Fisico:** Dirigirse a la carpeta ../1.CodingChallenge/Demo/, y abrir el archivo  'Test_challenge.fig' en el <a href="https://www.figma.com/" target="_blank">Figma</a>.
* **Archivo Digital:** Figma (Web)-> <a href="https://www.figma.com/design/nmodnk9E94e3AHUWjjMkY2/Test_challenge?node-id=1-2&m=dev&t=7MPYM1q2HvmzhtPg-1" target="_blank">Ver Archivo</a>.

### C) Demo

* **Archivo:** Aqui el video con la configuración y explicación del Coding Challenge: <a href="https://drive.google.com/file/d/16Sdsj39etKdcr0IzuK5Xu3rAyg1CE5kI/view?usp=drive_link" target="_blank">Ver Demo</a>.




## 2) Design Challenge

* **Documento de Diseño:** Dirigirse a la carpeta .../2.DesignChallenge, y abrir el archivo  'DesignChallenge.docx' o directamente en el link <a href="https://github.com/WORBE/tech_challenge/blob/main/2.DesignChallenge/DesignChallenge.docx" target="_blank">Ver Archivo</a>.

* **Diagrama de la Arquitectura (DrawIo):** Dirigirse a la carpeta .../2.DesignChallenge, y abrir el archivo  'SuperPayment_Arquitectura.drawio' en <a href="https://www.drawio.com/" target="_blank">DrawIo</a>.

* **Diagrama de la Arquitectura (Png):** Dirigirse a la carpeta .../2.DesignChallenge, y abrir el archivo  'SuperPayment_Arquitectura.drawio.png' o directamente en el link <a href="https://github.com/WORBE/tech_challenge/blob/main/2.DesignChallenge/SuperPayment_Arquitectura.drawio.png" target="_blank">Ver Archivo</a>.