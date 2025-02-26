import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import threading
import schedule
import time
import csv
import json
from plyer import notification  # Requiere instalación: pip install plyer

# Función para comprimir una carpeta con barra de progreso
def zip_folder(folder_path, output_path, progress_callback):
    """Comprime una carpeta en un archivo ZIP y actualiza el progreso."""
    try:
        total_files = sum([len(files) for _, _, files in os.walk(folder_path)])
        current_file = 0
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    if len(arcname) > 200:  # Truncar nombres largos
                        arcname = arcname[:200] + "_truncated"
                    zipf.write(file_path, arcname)
                    current_file += 1
                    progress_callback(current_file / total_files * 100)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo comprimir la carpeta: {str(e)}")
        return False

# Función para registrar el backup en un historial
def log_backup(output_path, success):
    """Registra los detalles del backup en un archivo CSV."""
    with open('backup_log.csv', 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'output_path', 'success']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:  # Escribir encabezados si el archivo está vacío
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'output_path': output_path,
            'success': success
        })
    update_history_display()

# Función para realizar el backup
def perform_backup():
    """Realiza el backup de la carpeta fuente al destino."""
    source_folder = source_var.get()
    destination_folder = destination_var.get()

    # Validar rutas
    if not source_folder or not destination_folder:
        messagebox.showwarning("Advertencia", "Selecciona tanto la carpeta fuente como la de destino.")
        return
    if not os.path.exists(source_folder):
        messagebox.showerror("Error", "La carpeta fuente no existe.")
        return
    if not os.path.exists(destination_folder):
        messagebox.showerror("Error", "La carpeta de destino no existe.")
        return

    # Crear nombre único para el archivo ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}.zip"
    output_path = os.path.join(destination_folder, backup_filename)

    # Configurar barra de progreso
    progress_bar['value'] = 0
    root.update_idletasks()

    def update_progress(percent):
        progress_bar['value'] = percent
        root.update_idletasks()

    # Realizar el backup
    success = zip_folder(source_folder, output_path, update_progress)
    log_backup(output_path, success)
    if success:
        messagebox.showinfo("Éxito", f"Backup completado: {output_path}")
        notify_user("Backup Completado", f"Se ha creado el backup en: {output_path}")
    else:
        notify_user("Error en Backup", "No se pudo completar el backup.")

# Funciones para seleccionar carpetas
def select_source():
    """Abre un diálogo para seleccionar la carpeta fuente."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        source_var.set(folder_selected)
        save_config()

def select_destination():
    """Abre un diálogo para seleccionar la carpeta de destino."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        destination_var.set(folder_selected)
        save_config()

# Función para programar el backup
def schedule_backup():
    """Programa el backup para una hora específica."""
    scheduled_time = time_var.get()
    if not scheduled_time:
        messagebox.showwarning("Advertencia", "Ingresa una hora válida (HH:MM).")
        return

    try:
        hour, minute = map(int, scheduled_time.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Hora inválida")
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(perform_backup_threaded)
        messagebox.showinfo("Éxito", f"Backup programado para las {scheduled_time}")
        save_config()
    except ValueError:
        messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM (24 horas).")

# Ejecutar backup en un hilo separado
def perform_backup_threaded():
    """Ejecuta el backup en un hilo separado para no bloquear la interfaz."""
    threading.Thread(target=perform_backup).start()

# Verificar tareas programadas
def run_scheduled_tasks():
    """Ejecuta las tareas programadas en un bucle."""
    while True:
        schedule.run_pending()
        time.sleep(1)

# Guardar configuración
def save_config():
    """Guarda las configuraciones en un archivo JSON."""
    config = {
        'source_folder': source_var.get(),
        'destination_folder': destination_var.get(),
        'scheduled_time': time_var.get()
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)

# Cargar configuración
def load_config():
    """Carga las configuraciones desde un archivo JSON."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            source_var.set(config.get('source_folder', ''))
            destination_var.set(config.get('destination_folder', ''))
            time_var.set(config.get('scheduled_time', ''))
    except FileNotFoundError:
        pass

# Actualizar historial en la interfaz
def update_history_display():
    """Muestra el historial de backups en la interfaz."""
    history_text.delete(1.0, tk.END)
    try:
        with open('backup_log.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                status = "Éxito" if row['success'] == 'True' else "Fallo"
                history_text.insert(tk.END, f"{row['timestamp']} - {row['output_path']} - {status}\n")
    except FileNotFoundError:
        history_text.insert(tk.END, "No hay historial de backups aún.\n")

# Enviar notificaciones
def notify_user(title, message):
    """Envía una notificación al usuario."""
    notification.notify(title=title, message=message, app_name='Backup App')

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Backup Automático")
root.geometry("600x500")

# Variables Tkinter
source_var = tk.StringVar()
destination_var = tk.StringVar()
time_var = tk.StringVar()

# Frame principal
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Selección de carpetas
ttk.Label(main_frame, text="Carpeta Fuente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(main_frame, textvariable=source_var, width=50).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(main_frame, text="Seleccionar", command=select_source).grid(row=0, column=2, padx=5, pady=5)

ttk.Label(main_frame, text="Carpeta Destino:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(main_frame, textvariable=destination_var, width=50).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(main_frame, text="Seleccionar", command=select_destination).grid(row=1, column=2, padx=5, pady=5)

# Programación de backup
ttk.Label(main_frame, text="Hora de Backup (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(main_frame, textvariable=time_var, width=10).grid(row=2, column=1, padx=5, pady=5, sticky="w")
ttk.Button(main_frame, text="Programar", command=schedule_backup).grid(row=2, column=2, padx=5, pady=5)

# Botón de backup manual
ttk.Button(main_frame, text="Realizar Backup Ahora", command=perform_backup).grid(row=3, column=0, columnspan=3, pady=10)

# Barra de progreso
progress_bar = ttk.Progressbar(main_frame, length=400, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=3, pady=10)

# Historial de backups
ttk.Label(main_frame, text="Historial de Backups:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
history_text = tk.Text(main_frame, height=10, width=70)
history_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# Cargar configuración inicial y actualizar historial
load_config()
update_history_display()

# Iniciar hilo para tareas programadas
threading.Thread(target=run_scheduled_tasks, daemon=True).start()

# Ejecutar aplicación
root.mainloop()