from django.shortcuts import render
from django.http import HttpResponse
import qrcode
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def index(request):
    if request.method == 'POST':
        wifiName = request.POST.get('ssid')
        wifiPassword = request.POST.get('password')
        file_name = request.POST.get('file_name', 'wifi_qr_code')
        pdf_file = generate_qr(wifiName, wifiPassword, file_name)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
        return response
    else:
        return render(request, 'index.html')

def generate_qr(wifiName, wifiPassword, file_name):
    wifi_config = f"WIFI:T:WPA;S:{wifiName};P:{wifiPassword};;"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=5,
    )
    qr.add_data(wifi_config)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to an in-memory file in PNG format
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # Use ImageReader to handle the BytesIO object directly
    image_reader = ImageReader(img_buffer)

    # Create a PDF file
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Get page size
    page_width, page_height = letter

    # Size of the QR code
    qr_code_size = 630

    # Calculate position to center the QR code
    x = (page_width - qr_code_size) / 2
    y = (page_height - qr_code_size) / 2

    # Draw the QR code on the PDF
    pdf.drawImage(image_reader, x, y, qr_code_size, qr_code_size)  # Position and size of the QR code on the PDF
    pdf.save()

    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
