# QR Code Generator

## Project Description
This project is a web application built with Streamlit that generates QR codes based on user-provided data. Users can customize the QR code by optionally embedding a logo and selecting a color. The application also provides the functionality to download the generated QR code as a PNG or PDF file.

## Features
- **Custom Color Selection**: Users can choose any color for the QR code to enhance visibility and aesthetics.
- **Logo Embedding**: Users can embed a logo in the center of the QR code, making it more branded and recognizable.
- **Downloadable Outputs**: The generated QR code can be downloaded in PNG or PDF formats, suitable for various applications like marketing, event management, and personal use.
- **User-Friendly Interface**: With Streamlit, the application offers a clean and interactive interface that is easy to navigate.

## Installation
To set up this project, you'll need Python and pip installed on your machine. Follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/nishantjoshi-007/qrcodeGEN.git
   cd qr_code_generator
   ```

2. **Install Dependencies**
   - Ensure you have Python 3.11 or newer.
   - Install the required Python packages using pip:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Usage
1. **Start the Application**: Run the command `streamlit run app.py`. This will open the application in your default web browser.
2. **Input URL**: Enter the URL or data you want to convert into a QR code.
3. **Customization**:
   - **Color**: Pick a color for the QR code using the color picker.
   - **Logo**: If you want to include a logo, select 'Yes' for the logo option and upload an image file.
4. **Generate QR Code**: Click on 'Generate QR Code' to see the result.
5. **Download**: Choose your preferred format (PNG or PDF) and download the generated QR code.

## Code Overview
### Main Functions

- **`generate_qr_code(data, logo_image=None, color='black')`**:
  - **Parameters**:
    - `data`: The information to encode in the QR code.
    - `logo_image`: An optional image object to embed in the center of the QR code.
    - `color`: Color for the QR code (default is black).
  - **Returns**: An image object containing the generated QR code.
  - **Description**: This function creates a QR code from the provided data. If a logo is provided, it embeds the logo at the center. The QR code is colored based on the user's choice.

- **`create_pdf_with_image(image)`**:
  - **Parameter**:
    - `image`: An image object of the QR code.
  - **Returns**: A byte stream containing the PDF file.
  - **Description**: Converts the given QR code image into a PDF file and returns the PDF file as a byte stream.

### Styles
- The application uses custom CSS for styling, defined in a multi-line string passed to `st.markdown()`. It styles the container, buttons, and hover effects to improve the user interface.

## Requirements
- Python 3.11
- Streamlit
- Pillow (for image handling)
- qrcode[pil] (for QR code generation)
- reportlab (for PDF generation)

## Author
- [Nishant Joshi](https://yourwebsite.com)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
