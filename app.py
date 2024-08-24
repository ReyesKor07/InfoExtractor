# Se importa el módulo "re" para utilizar expresiones regulares
import re
# Se importa el módulo "tkinter" para crear la interfaz gráfica de usuario
import tkinter as tk
# Se importa el módulo "ttk" de "tkinter" para crear widgets más modernos y personalizables
from tkinter import ttk
# Se importa la función "filedialog" del módulo "tkinter" para permitir al usuario seleccionar un archivo
from tkinter import filedialog, messagebox
# Se importa la función "convert_from_path" del módulo "pdf2image" para convertir páginas de un archivo PDF en imágenes
from pdf2image import convert_from_path
# Se importa la función "image_to_string" del módulo "pytesseract" para extraer texto de una imagen
from pytesseract import image_to_string
# Se importa la clase "Image" y la función "ImageTk" del módulo "PIL" para trabajar con imágenes en la interfaz gráfica de usuario.
from PIL import Image, ImageTk # py -m pip install PIL

# La función browse_file se utiliza para mostrar un cuadro de diálogo para que el usuario seleccione un archivo PDF.
def browse_file():
    # Se utiliza la función askopenfilename del módulo filedialog para que el usuario seleccione el archivo PDF.
    # Se define que sólo se mostrarán archivos PDF.
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    
    # Si el usuario seleccionó un archivo, se llama a la función extract_text_from_pdf con el camino del archivo seleccionado como argumento.
    if file_path:
          extract_text_from_pdf(file_path)

# La función show_loading_message se utiliza para mostrar una ventana emergente con un mensaje y una animación de carga.
def show_loading_message(loading_type="Espera"):
    # Crear una nueva ventana emergente
    loading_window = tk.Toplevel(app)
    loading_window.title("Espere por favor")
    loading_window.configure(bg="#1B2631")

    # Cargar imagen del icono correspondiente
    if loading_type == "Espera":
        message = "El programa está obteniendo la información del archivo PDF...\nEste proceso puede tomar unos segundos..."
        icon_path = "loading.png"
    icon_image = Image.open(icon_path).resize((70, 70))
    icon_photo = ImageTk.PhotoImage(icon_image)

    # Crear una etiqueta en la ventana emergente para mostrar el icono y el mensaje
    icon_label = tk.Label(loading_window, image=icon_photo, bg="#1B2631")
    icon_label.pack(padx=20, pady=20)
    message_label = tk.Label(loading_window, text=message, font=("Times New Roman", 16), justify="center", fg="#FFFFFF", bg="#1B2631")
    message_label.pack(padx=20, pady=10)

    # Actualizar la ventana principal
    app.update()

    # Programar la llamada a la función de cierre después de 4 segundos
    loading_window.after(4000, loading_window.destroy)

# Esta función extrae el texto de un archivo PDF seleccionado y lo muestra en la interfaz de usuario.
def extract_text_from_pdf(file_path):
    # Mostrar el mensaje de espera
    show_loading_message()
    # Se define la variable global extracted_text
    global extracted_text
    # Se convierten las imágenes del archivo PDF a texto
    images = convert_from_path(file_path)
    extracted_text = ""
    # Se recorre cada imagen y se agrega su texto a la variable extracted_text
    for image in images:
        extracted_text += image_to_string(image)

    # Se borra el contenido anterior del cuadro de texto y se inserta el nuevo texto extraído
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, extracted_text)

    # Se busca la cantidad en el texto extraído usando una expresión regular
    cantidad_match = re.findall(r'CANTIDAD\s?:\s?([\d,.]+)', extracted_text)
    if cantidad_match:
        # Si se encuentra la cantidad, se asigna a la variable cantidad
        cantidad = cantidad_match[0]
    else:
        # Si no se encuentra la cantidad, se asigna un mensaje de error a la variable cantidad
        cantidad = 'No se encontró la cantidad'

    # Extraer información usando expresiones regulares
    global info
    info = {
        'Datos Básicos Generales': {
            '---Datos Básicos Generales---\n'
            '\nNombre de la obra\n:': re.findall(r'DATOS BASICOS GENERALES(.*?)ESTADO:', extracted_text, re.DOTALL)[0].strip() if re.findall(r'DATOS BASICOS GENERALES(.*?)ESTADO:', extracted_text, re.DOTALL) else 'No se encontró el nombre de la obra',
            '\nEstado': re.findall(r'ESTADO: (.+?)MUNICIPIO:', extracted_text)[0].strip() if re.findall(r'ESTADO: (.+?)MUNICIPIO:', extracted_text) else 'No se encontró el estado',
            '\nMunicipio': re.findall(r'MUNICIPIO: (.+?)LOCALIDAD :', extracted_text)[0].strip() if re.findall(r'MUNICIPIO: (.+?)LOCALIDAD :', extracted_text) else 'No se encontró el municipio',
            '\nLocalidad': None,
            '\nFECHA INICIO DE CONTRATO': re.findall(r'FECHA INICIO DE CONTRATO: (.+?)FECHA REAL DE INICIO:', extracted_text)[0].strip() if re.findall(r'FECHA INICIO DE CONTRATO: (.+?)FECHA REAL DE INICIO:', extracted_text) else 'No se encontró la fecha de inicio de contrato',
            '\nFECHA REAL DE INICIO': ' '.join(re.findall(r'FECHA REAL DE INICIO: (.+?)(\d{4})', extracted_text)[0]) if re.findall(r'FECHA REAL DE INICIO: (.+?)(\d{4})', extracted_text) else 'No se encontró la fecha real de inicio',
            '\nFECHA TERMINO CONTRATO': re.findall(r'FECHA TERMINO CONTRATO: (.+?)FECHA REAL DE TERMINO:', extracted_text)[0].strip() if re.findall(r'FECHA TERMINO CONTRATO: (.+?)FECHA REAL DE TERMINO:', extracted_text) else 'No se encontró la fecha de término de contrato',
            '\nFECHA REAL DE TERMINO': ' '.join(re.findall(r'FECHA REAL DE TERMINO: (.+?)(\d{4})', extracted_text)[0]) if re.findall(r'FECHA REAL DE TERMINO: (.+?)(\d{4})', extracted_text) else 'No se encontró la fecha real de término',
            '\nContrato No.': re.findall(r'CONTRATO No\. : (.*?)CONTRATISTA', extracted_text, re.DOTALL),
            '\nContratista': re.findall(r'CONTRATISTA : (.*?)FIANZA DE ANTICIPO', extracted_text, re.DOTALL),
            '\nFIANZA DE ANTICIPO': re.findall(r'FIANZA DE ANTICIPO No. : (.+?)FIANZA DE CUMPLIMIENTO', extracted_text),
            '\nFIANZA DE CUMPLIMIENTO': re.findall(r'FIANZA DE CUMPLIMIENTO No. : (.+)', extracted_text)

        },
        'Inversión': {
            'Aprobada': re.findall(r'APROBADA\s+?EJERCIDA\s+?(\$[\d,]+?\.\d{2})', extracted_text),
            'Ejercida': re.findall(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})', extracted_text)[1]
        },
        'Metas': {
            'Aprobadas': {
                'Cantidad': re.findall(r'CANTIDAD: (.+?)\sU\. DE MEDIDAD :', extracted_text)[0] if re.findall(r'CANTIDAD: (.+?)\sU\. DE MEDIDAD :', extracted_text) else 'No se encontró la cantidad',
                'Unidad de medida': re.findall(r'U\. DE MEDIDAD : (.+?)\sCANTIDAD:', extracted_text)[0] if re.findall(r'U\. DE MEDIDAD : (.+?)\sCANTIDAD:', extracted_text) else 'No se encontró la unidad de medida'
            },
            'Alcanzadas': {
                'Cantidad': re.findall(r'CANTIDAD: .+?U\. DE MEDIDAD : .+?CANTIDAD: (.+?)U\. DE MEDIDAD', extracted_text)[0] if re.findall(r'CANTIDAD: .+?U\. DE MEDIDAD : .+?CANTIDAD: (.+?)U\. DE MEDIDAD', extracted_text) else 'No se encontró la cantidad',
                'Unidad de medida': re.findall(r'CANTIDAD: .+?U\. DE MEDIDAD : .+?CANTIDAD: .+?U\. DE MEDIDAD : (.+)', extracted_text)[0] if re.findall(r'CANTIDAD: .+?U\. DE MEDIDAD : .+?CANTIDAD: .+?U\. DE MEDIDAD : (.+)', extracted_text) else 'No se encontró la unidad de medida'
            }
        },
        'Descripción del Proyecto': re.findall(r'IV\. DESCRIPCION DEL PROYECTO(.*?)V\. SITUACION DE LA OBRA', extracted_text, re.DOTALL)[0].strip()
    }

    # Asignar el valor de "Municipio" a "Localidad"
    info['Datos Básicos Generales']['Localidad'] = info['Datos Básicos Generales']['Municipio']

# Esta función guarda el contenido del PDF en un archivo de texto
def save_text():
    # Se utiliza la función asksaveasfilename del módulo filedialog para que el usuario seleccione un archivo de texto donde guardar el contenido.
    # Se define que sólo se mostrarán archivos de texto.
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    # Si el usuario seleccionó un archivo, se guarda el contenido del panel principal en el archivo de texto.
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_box.get("1.0", tk.END))
        # Se muestra una ventana emergente para informar al usuario que el archivo ha sido guardado con éxito.
        messagebox.showinfo(title="Archivo guardado", message="El archivo ha sido guardado con éxito.", icon="info", parent=app)

# Función para mostrar el contenido del PDF
def display_pdf_content():
    global extracted_text
    # Borrar el contenido del cuadro de texto
    text_box.delete(1.0, tk.END)
    # Insertar el texto extraído del PDF en el cuadro de texto
    text_box.insert(tk.END, extracted_text)

# Función para buscar información en el PDF
def search_info():
    # Obtener la opción seleccionada en el menú desplegable
    selected_option = combo_box.get()
    # Borrar el contenido del cuadro de texto
    text_box.delete(1.0, tk.END)
    
    # Mostrar información específica en el cuadro de texto según la opción seleccionada
    if selected_option == "Metas":
        text_box.insert(tk.END, f"Aprobadas: Cantidad: ${info['Metas']['Aprobadas']['Cantidad']}, Unidad de medida: {info['Metas']['Aprobadas']['Unidad de medida']}\n")
        text_box.insert(tk.END, f"Alcanzadas: Cantidad: ${info['Metas']['Alcanzadas']['Cantidad'][0]}, Unidad de medida: {info['Metas']['Alcanzadas']['Unidad de medida'][0]}\n")
    elif selected_option == "Inversión":
        text_box.insert(tk.END, f"Aprobada: {info['Inversión']['Aprobada'][0]}\n")
        text_box.insert(tk.END, f"Ejercida: {info['Inversión']['Ejercida']}\n")
    elif selected_option == "Descripción del Proyecto":
        text_box.insert(tk.END, info['Descripción del Proyecto'])
    else:
        for key, value in info[selected_option].items():
            # Extraer el valor si es una lista y tiene elementos
            if isinstance(value, list) and len(value) > 0:
                value = value[0]
            # Insertar el nombre de la clave y su valor correspondiente en el cuadro de texto
            text_box.insert(tk.END, f"{key}: {value}\n")

# Crear una nueva ventana
app = tk.Tk()
app.title("Aplicación de Extracción de Información")
app.configure(bg="#1B2631")

# Obtener la resolución de la pantalla del usuario
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Establecer la geometría de la ventana en función de la resolución de pantalla
app.geometry(f"{screen_width}x{screen_height}")
app.minsize(400, 300)

# Crear un marco para la selección de PDF y la sección
pdf_frame = tk.Frame(app, bg="#1B2631")
pdf_frame.pack(pady=20, padx=20, fill=tk.X)

# Crear un botón para seleccionar un archivo PDF
select_pdf_button = tk.Button(pdf_frame, text="Seleccionar archivo PDF", command=browse_file, bg="#27AE60", fg="#FFFFFF", font=("Times New Roman", 14), width=30)
select_pdf_button.pack(side=tk.LEFT)

# Crear un cuadro de selección
section_label = tk.Label(pdf_frame, text="Selecciona una sección del PDF:", font=("Times New Roman", 16, "bold"), fg="#FFFFFF", bg="#1B2631")
section_label.pack(side=tk.LEFT, padx=20, pady=10)

# Crear una lista de opciones para el cuadro de selección
section_options = ["Datos Básicos Generales", "Inversión", "Metas", "Descripción del Proyecto"]
combo_box = ttk.Combobox(pdf_frame, values=section_options, font=("Times New Roman", 14), width=30)
combo_box.pack(side=tk.LEFT, padx=10, pady=10)

# Cargar una imagen de un icono para el botón y ajustar su tamaño
section_icon = Image.open("section.png").resize((40, 40))
section_photo = ImageTk.PhotoImage(section_icon)
section_button = tk.Button(pdf_frame, image=section_photo, bg="#1B2631", bd=0, command=lambda: combo_box.focus())
section_button.pack(side=tk.LEFT, padx=10, pady=10)

# Crear un marco para los botones de visualización y búsqueda
button_frame = tk.Frame(app, bg="#1B2631")
button_frame.pack(pady=20, padx=20, fill=tk.X)

# Crear un botón para mostrar el contenido del PDF
display_button = tk.Button(button_frame, text="Ver contenido del PDF", command=display_pdf_content, bg="#27AE60", fg="#FFFFFF", font=("Times New Roman", 14), width=30)
display_button.pack(side=tk.LEFT)

# Crear un botón para buscar información específica en el PDF
search_button = tk.Button(button_frame, text="Buscar información", command=search_info, bg="#27AE60", fg="#FFFFFF", font=("Times New Roman", 14), width=30)
search_button.pack(side=tk.LEFT, padx=(150,0))

# Crear un botón para guardar el contenido del PDF en un archivo de texto
save_button = tk.Button(button_frame, text="Guardar como archivo de texto", command=save_text, bg="#27AE60", fg="#FFFFFF", font=("Times New Roman", 14), width=30)
save_button.pack(side=tk.RIGHT)

# Crear un marco para el cuadro de texto y la barra de desplazamiento
text_box_frame = tk.Frame(app, bg="#1B2631")
text_box_frame.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)

# Crear un cuadro de texto para mostrar el contenido o la información del PDF
text_box = tk.Text(text_box_frame, font=("Times New Roman", 14),height=20, bg="#FFFFFF", fg="#1B2631", wrap="word")
text_box.pack(side=tk.LEFT,fill=tk.BOTH, padx=10, pady=10, expand=True)

# Crear una barra de desplazamiento para el cuadro de texto
scrollbar = tk.Scrollbar(text_box_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Asociar la barra de desplazamiento con el cuadro de texto
text_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_box.yview)

# Ejecutar la aplicación
app.mainloop()