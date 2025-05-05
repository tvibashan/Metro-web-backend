import qrcode
from io import BytesIO
from PIL import Image,ImageDraw
from django.core.files import File

    # def save(self,*args, **kwargs):
    #     qr_image = qrcode.make(self.product_title)
    #     file_name=f"{self.user.email}-{self.booking_id}-qr.png"
    #     stream=BytesIO()
    #     qr_image.save(stream,'PNG')
    #     self.qr_code.save(file_name,File(stream),save=False)
    #     super().save(*args, **kwargs)

def generate_qr_code(booking):
    qr_image = qrcode.make(booking.product_title)
    file_name=f"{booking.user.email}-{booking.booking_id}-qr.png"
    stream=BytesIO()
    qr_code=qr_image.save(stream,'PNG')
    return qr_code
