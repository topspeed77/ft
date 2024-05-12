import requests
import re
import time

# Buka file data.txt dan baca setiap baris
with open("data.txt", "r") as f:
    lines = f.readlines()

# Inisialisasi hitung dan total jumlah koneksi
counter = 0
total = len(lines)

# Buka file hasil.txt dan siapkan untuk menulis ke dalamnya
with open("hasil.txt", "w") as f:
    f.write("Result:\n")

# Iterate melalui setiap baris dan ekstrak URL, host, username, dan password
for line in lines:
    counter += 1

    # Ekstrak URL
    url = line.strip()

    # Inisialisasi ulang jumlah percobaan koneksi
    num_retries = 0

    while True:
        try:
            # Ambil respons teks dari URL
            response = requests.get(url)
            text = response.text

            # Buat pola regex untuk mencocokkan nilai "host", "username", dan "password"
            host_pattern = r'"host"\s*:\s*"([^"]*)"'
            host_pattern_alt = r'"host":\s+"([^"]+)"'
            username_pattern = r'"username"\s*:\s*"([^"]*)"'
            username_pattern_alt = r'"user":\s+"([^"]+)"'
            password_pattern = r'"password"\s*:\s*"([^"]*)"'
            password_pattern_alt = r'"password":\s+"([^"]+)"'
            port_pattern = r'"port"\s*:\s*(\d+)'
            port_pattern2 = r'"port":\s+"([^"]+)"'

            # Cocokkan pola dengan teks respons untuk mengambil nilai "host", "username", "port" dan "password"
            host_match = re.search(host_pattern, text) or re.search(host_pattern_alt, text)
            username_match = re.search(username_pattern, text) or re.search(username_pattern_alt, text)
            password_match = re.search(password_pattern, text) or re.search(password_pattern_alt, text)
            port_match = re.search(port_pattern, text)
            if not port_match:
                port_match = re.search(port_pattern2, text)
                if not port_match:
                    port = 21
                else:
                    port = port_match.group(1)
            else:
                port = port_match.group(1)

            # Uji kondisional untuk memeriksa apakah nilai "host", "username", dan "password" ditemukan
            if host_match and username_match and password_match:
                host = host_match.group(1)
                username = username_match.group(1)
                password = password_match.group(1)


                # Tulis hasil ke file hasil.txt
                with open("hasil.txt", "a") as f:
                 f.write("{}|{}|{}|{}|{}\n".format(url, host, port, username, password))


                # Tampilkan progress
                print("Memproses koneksi {} dari {}".format(counter, total))
                break

            # Jika tidak ditemukan nilai "host", "username", atau "password", lanjutkan ke URL berikutnya
            else:
                print("Tidak dapat menemukan nilai 'host', 'username', atau 'password'. Lanjutkan ke URL berikutnya.")
                break

        # Jika terjadi kesalahan koneksi, lewati koneksi ini
        except requests.exceptions.RequestException:
            num_retries += 1
            print("Koneksi {} dari {} gagal. Lewati koneksi ini.".format(counter, total))
            break

print("Pemrosesan selesai. Hasil tersimpan di hasil.txt")

