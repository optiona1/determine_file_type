import magic
from flask import Flask, request

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    with open("./upload_file.pdf", "wb") as f:
        chunk_size = 2048
        in_times = 0
        while True:
            chunk = request.stream.read(chunk_size)
            in_times += 1
            if in_times == 1:
                chunk = chunk.split(b"\r\n\r\n")
                file_type = magic.from_buffer(chunk[1])
                filename = chunk[0].decode().split("\r\n")[1].split("; ")[2].split('="')[1].strip('"')
                print(filename)
                print(file_type)
                f.write(chunk[1])
                continue
            if len(chunk) == 0:
                break
            else:
                f.write(chunk)
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
