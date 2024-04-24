from django.shortcuts import render
from django.http import HttpResponse
import qrcode

def index(request):
    if request.method == 'POST':
        wifiName = request.POST.get('ssid')
        wifiPassword = request.POST.get('password')
        file_name = request.POST.get('file_name')
        generate_qr(wifiName, wifiPassword, file_name)
        return HttpResponse("QR code generated successfully!")  # You can customize this response as needed
    else:
        return render(request, 'index.html')

def generate_qr(wifiName, wifiPassword, file_name):
    wifi_config = f"WIFI:T:WPA;S:{wifiName};P:{wifiPassword};;"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=40,
        border=5,
    )
    qr.add_data(wifi_config)
    qr.make(fit=True)

    # QR IMAGE COLOR DEFINE
    img = qr.make_image(fill_color="black", back_color="white")

    # file type and path
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=file_name)
    if file_path:
        img.save(file_path)
        messagebox.showinfo("QR Code Saved", f"The QR code has been saved as '{file_path}'.")
