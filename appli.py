from flask import Flask, request, jsonify
import easyocr
#import io
# Initialiser l'application Flask
app = Flask(__name__)
reader = easyocr.Reader(['en', 'fr'], gpu=False)
def img2text(image_content):
    # Détecter le texte dans l'image en utilisant OCR
    detection_result = reader.detect(image_content, width_ths=0.7, mag_ratio=1.5)
    recognition_results = reader.recognize(image_content, horizontal_list=detection_result[0][0], free_list=detection_result[0][1])
    textList = []
    for result in recognition_results:
        textList.append(result[1])
    # Retourner la liste des textes extraits de l'image
    return " ".join(textList)
@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        if 'file' not in request.files:
            return jsonify(error="No file part"), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify(error="No selected file"), 400
        if file:
            # Lire le fichier image et extraire le texte
            image_content = file.read()
            extracted_text = img2text(image_content)
            return jsonify(text=extracted_text)
    except Exception as e:
        return jsonify(error=str(e)), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)





