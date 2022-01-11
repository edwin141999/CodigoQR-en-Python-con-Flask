from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def enviar():
    if request.method == "POST":
        link = request.form.get("link")
        imglogo = request.form.get("logo")
        im = request.files['logo']
        urlimg = "./static/images/myOwnCodeQR.jpg"
        if imglogo != '' != None and im.filename != '':
            logo = Image.open(request.files['logo'])
            basewidth = 120
            wpercent = basewidth / float(logo.size[0])
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
            qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
            data = link
            qr_big.add_data(data)
            qr_big.make()
            img_qr_big = qr_big.make_image(
                fill_color="black", back_color="white"
            ).convert("RGB")
            pos = (
                (img_qr_big.size[0] - logo.size[0]) // 2,
                (img_qr_big.size[1] - logo.size[1]) // 2,
            )
            img_qr_big.paste(logo, pos)
            img_qr_big.save(urlimg)
            name = urlimg
            return send_file(name, as_attachment=True)
        else:
            qr = qrcode.QRCode(version=1, box_size=15, border=5)
            data = link
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            img.save(urlimg)
            name = urlimg
            return send_file(name, as_attachment=True)
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
