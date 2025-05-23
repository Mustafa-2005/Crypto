from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import numpy as np
import algorthem  # your cipher functions saved in algorthem.py


class CipherServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            with open("index.html", "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
            return

        if self.path.startswith("/cipher"):
            query = parse_qs(urlparse(self.path).query)
            text = query.get("text", [""])[0]
            cipher_type = query.get("type", ["caesar"])[0]
            mode = query.get("mode", ["1"])[0]
            key = query.get("key", [""])[0]

            try:
                result = "Invalid cipher type or parameters."

                if cipher_type == "caesar":
                    shift = int(key) if key.isdigit() else 3
                    result = algorthem.caesar_cipher(text, shift, mode)

                elif cipher_type == "vigenere":
                    result = algorthem.vigenere_cipher(text, key, mode)

                elif cipher_type == "mono":
                    # For monoalphabetic, key must be 26 letters substitution alphabet
                    key = key.upper()
                    if len(key) == 26:
                        if mode == "1":
                            result = algorthem.monoalphabetic_encrypt(text, key)
                        else:
                            result = algorthem.monoalphabetic_decrypt(text, key)
                    else:
                        result = "Monoalphabetic cipher key must be 26 letters."

                elif cipher_type == "playfair":
                    # Prepare Playfair matrix
                    key = key.upper().replace("J", "I")
                    matrix = algorthem.create_playfair_matrix(key)
                    if mode == "1":
                        result = algorthem.playfair_encrypt(text, matrix)
                    else:
                        result = algorthem.playfair_decrypt(text, matrix)

                elif cipher_type == "rail":
                    key_num = int(key) if key.isdigit() else 3
                    if mode == "1":
                        result = algorthem.rail_fence_encrypt(text, key_num)
                    else:
                        result = algorthem.rail_fence_decrypt(text, key_num)

                elif cipher_type == "columnar":
                    if key:
                        if mode == "1":
                            result = algorthem.columnar_transposition_encrypt(text, key)
                        else:
                            result = algorthem.columnar_transposition_decrypt(text, key)
                    else:
                        result = "Columnar Transposition requires a key."

                else:
                    result = "Unknown cipher type."

            except Exception as e:
                result = f"Error: {str(e)}"

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(result.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


def run(server_class=HTTPServer, handler_class=CipherServer, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
