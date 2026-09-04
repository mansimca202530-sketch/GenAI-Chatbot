import os

from flask import Flask, render_template, request, jsonify

from main import ask_llama, ask_deepseek, ask_pdf


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        query = data.get("message", "").strip()
        model = data.get("model", "llama")
        pdf_path = data.get("pdf_path")


        if not query:

            return jsonify({
                "success": False,
                "error": "Please enter a message."
            }), 400


        if model == "llama":

            answer = ask_llama(query)


        elif model == "deepseek":

            answer = ask_deepseek(query)


        elif model == "pdf":

            if not pdf_path:

                return jsonify({
                    "success": False,
                    "error": "Please upload a PDF first."
                }), 400


            if not os.path.exists(pdf_path):

                return jsonify({
                    "success": False,
                    "error": "PDF file not found."
                }), 400


            answer = ask_pdf(query, pdf_path)


        else:

            return jsonify({
                "success": False,
                "error": "Invalid model selected."
            }), 400


        return jsonify({
            "success": True,
            "answer": answer,
            "model": model
        })


    except Exception as e:

        print("CHAT ERROR:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/upload", methods=["POST"])
def upload_pdf():

    try:

        if "file" not in request.files:

            return jsonify({
                "success": False,
                "error": "No PDF selected."
            }), 400


        file = request.files["file"]


        if file.filename == "":

            return jsonify({
                "success": False,
                "error": "No PDF selected."
            }), 400


        if not file.filename.lower().endswith(".pdf"):

            return jsonify({
                "success": False,
                "error": "Only PDF files are allowed."
            }), 400


        os.makedirs("uploads", exist_ok=True)


        filepath = os.path.join(
            "uploads",
            file.filename
        )


        file.save(filepath)


        return jsonify({
            "success": True,
            "filename": file.filename,
            "path": filepath
        })


    except Exception as e:

        print("UPLOAD ERROR:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )