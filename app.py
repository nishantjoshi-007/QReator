import streamlit as st
import qrcode
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import tempfile
import os

def generate_qr_code(data, logo_image=None, color='black'):
    # Create QR code
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img_qr = qr.make_image(fill_color=color, back_color='white').convert("RGBA")

    if logo_image:
        # Convert the logo to RGBA
        logo = logo_image.convert("RGBA")

        # Define the maximum size for the logo (20% of the QR code size)
        max_logo_size = img_qr.size[0] * 0.20

        # Calculate the new size maintaining the aspect ratio
        aspect_ratio = logo.width / logo.height
        new_logo_width = int(min(max_logo_size, max_logo_size * aspect_ratio))
        new_logo_height = int(min(max_logo_size / aspect_ratio, max_logo_size))

        # Resize the logo
        logo.thumbnail((new_logo_width, new_logo_height))

        # Calculate coordinates to place the logo at the center of QR code
        logo_position = ((img_qr.size[0] - new_logo_width) // 2, (img_qr.size[1] - new_logo_height) // 2)

        # Place the logo in the QR code
        img_qr.paste(logo, (logo_position[0], logo_position[1]), logo)

    return img_qr

def create_pdf_with_image(image):
    # Create a temporary file for the image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_temp:
        image.save(img_temp, format='PNG')
        img_temp_path = img_temp.name

    # Create the PDF using the path to the temporary image file
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawImage(img_temp_path, x=100, y=400, width=image.width, height=image.height)  # Adjust positioning and size as needed
    c.showPage()
    c.save()
    buffer.seek(0)

    # Clean up the temporary image file
    os.remove(img_temp_path)

    return buffer

# Custom CSS to improve interface
st.markdown("""
    <style>
    .reportview-container {
        background-color: #F0F2F6;
        color: #333;
    }
    .reportview-container .main .block-container {
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stButton > button {
        width: 100%;
        color: white;
        border: none;
        border-radius: 5px;
        background-color: #FF4B4B;
        transition: background-color 0.3s, color 0.3s;
    }
    .stButton > button:hover {
        background-color: #E04343; /* Darker shade for hover */
        color: #FFF;
    }
    .css-2trqyj {
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)


st.title('QR Code Generator')
logo_option = st.radio("Do you want to include a logo in your QR code?", ("No", "Yes"))
uploaded_logo = None

if logo_option == "Yes":
    color = st.color_picker("Pick the color for your QR code", '#000000')
    uploaded_logo = st.file_uploader("Upload your logo (required for QR code with logo):", type=['jpg', 'jpeg', 'png'])
    data = st.text_input("Enter the URL that needs to be converted to QR code:", key="data_input_with_logo")
elif logo_option == "No":
    color = st.color_picker("Pick the color for your QR code", '#000000')
    data = st.text_input("Enter the URL that needs to be converted to QR code:", key="data_input_without_logo")

picked_color = color
generate_clicked = st.button('Generate QR Code', key='generate_qr_button')

if 'qr_code_image' not in st.session_state:
    st.session_state['qr_code_image'] = None

if generate_clicked and data:
    with st.spinner('Generating QR Code...'):
        logo_image = Image.open(uploaded_logo) if uploaded_logo and logo_option == "Yes" else None
        st.session_state['qr_code_image'] = generate_qr_code(data, logo_image, picked_color)

if st.session_state['qr_code_image'] is not None:
    st.image(st.session_state['qr_code_image'], caption='Your QR Code', use_column_width=True)
    file_format = st.radio("Select the download format:", ('PNG', 'PDF'))

    if file_format == 'PNG':
        img_buffer = io.BytesIO()
        st.session_state['qr_code_image'].save(img_buffer, format='PNG')
        img_buffer.seek(0)
        st.download_button(label="Download QR Code as PNG",
                           data=img_buffer, 
                           file_name="qr_code.png",
                           mime="image/png")
    elif file_format == 'PDF':
        pdf_buffer = create_pdf_with_image(st.session_state['qr_code_image'])
        st.download_button(label="Download QR Code as PDF",
                           data=pdf_buffer,
                           file_name="qr_code.pdf",
                           mime="application/pdf")