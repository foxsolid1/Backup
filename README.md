# Backup
Proyecto de backup en Python 
Proyecto de Respaldo Automático en Python
Este proyecto es una aplicación de respaldo automático desarrollada en Python. Permite a los usuarios seleccionar una carpeta fuente y una carpeta de destino, programar copias de seguridad para una hora específica y realizar copias de seguridad manuales. La aplicación comprime la carpeta fuente en un archivo ZIP, registra cada respaldo en un historial que se muestra en la interfaz gráfica y envía notificaciones al usuario sobre el estado del respaldo.
Características Principales
Selección de Carpetas: Escoge la carpeta fuente y la carpeta de destino mediante una interfaz gráfica intuitiva.
Respaldo Manual: Realiza un respaldo inmediato con un solo clic.
Programación de Respaldos: Agenda respaldos automáticos para una hora específica del día.
Barra de Progreso: Muestra el avance de la compresión durante el proceso de respaldo.
Historial de Respaldos: Registra cada respaldo en un archivo CSV y muestra el historial en la interfaz.
Notificaciones: Envía notificaciones al usuario cuando un respaldo se completa o falla.
Configuración Persistente: Guarda las rutas de las carpetas y la hora programada en un archivo JSON para reutilizarlas en futuras ejecuciones.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Requisitos Previos
Para ejecutar este proyecto, necesitas lo siguiente:
Python 3.x: La aplicación requiere una versión 3.x de Python.
Bibliotecas de Python:
tkinter: Para la interfaz gráfica (generalmente incluida con Python).
schedule: Para programar tareas.
plyer: Para enviar notificaciones.
json y csv: Para manejar archivos de configuración y registro (incluidas en la biblioteca estándar).
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Instalación
Sigue estos pasos para instalar y preparar el proyecto:
Clonar el Repositorio:
git clone https://github.com/foxsolid1/proyecto-backup-python.git
cd proyecto-backup-python
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Instalar Dependencias:
Instala las bibliotecas necesarias usando pip:
bash
pip install plyer schedule
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Nota: tkinter suele venir incluido con Python. Si no está disponible, consulta la documentación de tu sistema operativo para instalarlo.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Uso
Ejecutar la Aplicación:
Inicia la aplicación ejecutando el siguiente comando en la terminal:
bash
python backup.py
Interfaz Gráfica:
Seleccionar Carpetas:
Haz clic en "Seleccionar" junto a "Carpeta Fuente" para elegir la carpeta a respaldar.
Haz clic en "Seleccionar" junto a "Carpeta Destino" para elegir dónde se guardarán los archivos ZIP.
Realizar Respaldo Manual:
Haz clic en "Realizar Backup Ahora" para iniciar un respaldo inmediato. La barra de progreso mostrará el avance.
Programar Respaldo:
Ingresa la hora en formato HH:MM (24 horas) en el campo "Hora de Backup".
Haz clic en "Programar" para agendar el respaldo automático.
Historial de Respaldos:
El historial de respaldos se muestra en la parte inferior de la interfaz, con la fecha, la ruta del archivo y el estado.
Notificaciones:
Recibirás una notificación al completar o fallar un respaldo, informándote del resultado.
Archivos Generados
backup_log.csv: Registra el historial de respaldos con la fecha, ruta del archivo ZIP y estado.
config.json: Almacena las rutas de las carpetas y la hora programada para reutilizarlas.
Contribuciones
¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, envía una solicitud de extracción (pull request). Algunas ideas para mejoras incluyen:
Implementar respaldos incrementales.
Permitir múltiples programaciones de respaldo.
Añadir opciones para personalizar el nivel de compresión.
Problemas Conocidos
Los respaldos programados ocurren diariamente a la hora especificada. Para intervalos distintos, modifica el código.
La aplicación no elimina automáticamente respaldos antiguos; debes gestionarlos manualmente en la carpeta de destino.
Licencia
Este proyecto está licenciado bajo la Licencia MIT (LICENSE).
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
