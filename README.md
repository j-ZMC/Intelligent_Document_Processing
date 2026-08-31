# Intelligent_Document_Processing

****Proyecto y Justificación:****

  

En el mundo profesional, las grandes empresas de tecnología que manejan grandes cantidades datos y archivos no están estructurados, se encuentran dispersos en distintos formatos, por ejemplo: archivos PDF, imágenes escaneadas, contratos firmados a mano, estados de cuenta bancarios, facturas físicas y correos electrónicos.

  

Gran parte del flujo de archivos que reciben las empresas se dividen de esta forma, un proveedor envía un archivo, luego un empleado lo recibe, manualmente copia los datos, finalmente los pone en una base de datos.

  

Mi propuesta es hacer un traductor universal de documentos a distintos tipos de bases de datos ya sea (JSON, CSV, SQL). Este proyecto se va hacer con librerías como fastapi, uvicorn, pytorch, openai, etc.

  

El flujo de trabajo está pensado para que el uso de Inteligencia Artificial de distintos tipos sea necesario para poder separar y ordenar los datos en distintos archivos.

  

La necesidad de este tipo de programa radica en el costo operativo que las empresas enfrentan al usar personal capacitado para tareas de este estilo e igualmente la capacidad de un humano de escalar esto cuando se alcanzan miles de páginas es bastante pobre.


##  Pseudocódigo:

**Entradas**
*• documento — archivo (PDF o Imagen)
• campos_a_extraer — lista de texto (Ej. total, fecha)*

**Proceso**
*1. Inicio
2. PEDIR documento y campos_a_extraer al usuario.
3. Extracción Rápida (OCR Local)
3.1. EXTRAER texto del documento con un motor de OCR local.
3.2. BUSCAR los campos_a_extraer usando reglas y expresiones regulares.
3.3. GUARDAR los datos encontrados en resultado.
4. Decisión de Routing
4.1. SI se encontraron TODOS los campos_a_extraer ENTONCES
4.1.1. DEFINIR origen = "OCR_LOCAL"
4.1.2. IR A paso 6.
5. Rescate con IA (VLM / LLM)
5.1. ENVIAR documento y los campos faltantes a la API del modelo de lenguaje.
5.2. COMPLETAR el resultado con los datos devueltos por el modelo.
5.3. DEFINIR origen = "LLM_RESCATE"
6. Formateo y Salida
6.1. CONVERTIR resultado al formato final (JSON, CSV o SQL).
6.2. MOSTRAR origen y resultado.
7. Fin*
**Salidas**
*• origen — texto ("OCR_LOCAL" o "LLM_RESCATE")
• resultado — archivo/texto (JSON, CSV o SQL)*
