from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

app = Flask(__name__)

def cek_snbp(nomor_pendaftaran, hari, bulan, tahun):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # **Tambahkan path Chromium di Render**
        options.binary_location = "/usr/bin/chromium-browser"

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Masuk ke website SNBP
        driver.get("https://pengumuman-snbp.snpmb.id/")

        # Isi form input
        driver.find_element(By.ID, "index-form-registration-number").send_keys(nomor_pendaftaran)
        driver.find_element(By.ID, "index-form-birthday-day").send_keys(hari)
        driver.find_element(By.ID, "index-form-birthday-month").send_keys(bulan)
        driver.find_element(By.ID, "index-form-birthday-year").send_keys(tahun)

        # Klik tombol cek hasil
        driver.find_element(By.ID, "index-form-submit").click()

        driver.implicitly_wait(2)

        current_url = driver.current_url
        if "accepted.html" in current_url:
            hasil = "Selamat! Kamu diterima."
        else:
            idspan = "index-rejected-name"
            hasil = driver.find_element(By.ID, idspan).text

        driver.quit()
        return hasil

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/cek', methods=['GET'])
def cek():
    nomor_pendaftaran = request.args.get('nomor_pendaftaran')
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')

    if not nomor_pendaftaran or not day or not month or not year:
        return jsonify({"error": "Nomor pendaftaran dan tanggal lahir wajib diisi"}), 400

    hasil = cek_snbp(nomor_pendaftaran, day, month, year)
    return jsonify({"hasil": hasil})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Sesuai dengan Render
    app.run(host="0.0.0.0", port=port, debug=True)
