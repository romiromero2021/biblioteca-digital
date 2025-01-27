import streamlit as st
import os
import io
from PyPDF2 import PdfReader
from docx import Document

# Configuración de la página
st.set_page_config(
    page_title="Biblioteca Digital",
    page_icon="📚",
    layout="wide"
)

# Estilos CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .upload-text {
        text-align: center;
        padding: 2rem;
        border: 2px dashed #cccccc;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("📚 Biblioteca Digital")
st.markdown("---")

# Inicializar el estado de la sesión si no existe
if 'biblioteca' not in st.session_state:
    st.session_state.biblioteca = []

# Función para extraer texto de PDF
def extraer_texto_pdf(archivo):
    pdf_reader = PdfReader(archivo)
    texto = ""
    for pagina in pdf_reader.pages:
        texto += pagina.extract_text()
    return texto

# Función para extraer texto de DOCX
def extraer_texto_docx(archivo):
    doc = Document(archivo)
    texto = ""
    for parrafo in doc.paragraphs:
        texto += parrafo.text + "\n"
    return texto

# Sección de carga de archivos
st.header("📤 Subir Documento")
archivo = st.file_uploader("Arrastra o selecciona un archivo (PDF o DOCX)", 
                          type=['pdf', 'docx'])

if archivo:
    # Procesar el archivo
    try:
        nombre = archivo.name
        tipo = archivo.type
        contenido = archivo.read()
        
        # Extraer texto según el tipo de archivo
        if tipo == "application/pdf":
            texto = extraer_texto_pdf(io.BytesIO(contenido))
        else:  # docx
            texto = extraer_texto_docx(io.BytesIO(contenido))
        
        # Guardar en la biblioteca
        documento = {
            "nombre": nombre,
            "tipo": tipo,
            "contenido": contenido,
            "texto": texto
        }
        
        if st.button("Guardar en Biblioteca"):
            st.session_state.biblioteca.append(documento)
            st.success(f"¡Documento '{nombre}' guardado con éxito!")
            
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")

# Mostrar biblioteca
st.header("📚 Mi Biblioteca")
if len(st.session_state.biblioteca) == 0:
    st.info("Tu biblioteca está vacía. ¡Sube algunos documentos!")
else:
    # Búsqueda
    busqueda = st.text_input("🔍 Buscar en documentos...")
    
    for i, doc in enumerate(st.session_state.biblioteca):
        # Filtrar por búsqueda si hay término de búsqueda
        if busqueda and busqueda.lower() not in doc["nombre"].lower() and busqueda.lower() not in doc["texto"].lower():
            continue
            
        with st.expander(f"📄 {doc['nombre']}"):
            # Mostrar extracto del texto
            st.text_area("Contenido:", doc["texto"][:500] + "...", height=150)
            
            # Botones de acción
            col1, col2 = st.columns(2)
            
            # Botón de descarga
            with col1:
                st.download_button(
                    "⬇️ Descargar",
                    doc["contenido"],
                    file_name=doc["nombre"],
                    mime=doc["tipo"]
                )
            
            # Botón de eliminar
            with col2:
                if st.button("🗑️ Eliminar", key=f"del_{i}"):
                    st.session_state.biblioteca.pop(i)
                    st.experimental_rerun()

# Pie de página
st.markdown("---")
st.markdown("### 📖 Características:")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("- Subida de PDF y DOCX")
with col2:
    st.markdown("- Búsqueda en documentos")
with col3:
    st.markdown("- Descarga y eliminación")
