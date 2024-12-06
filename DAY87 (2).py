import hashlib
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Function to generate the hash of a file
def generate_file_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Calculate and set the hash of the original movie (change this path)
original_movie_path ='WhatsApp Video 2024-12-06 at 22.38.53_bd381402.mp4'  # Change to your actual movie path
original_movie_hash = generate_file_hash(original_movie_path)
print(f"Original Movie Hash: {original_movie_hash}")

# Route to upload movie file
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['movie_file']
        if file:
            # Save the uploaded file temporarily
            file_path = os.path.join('uploads', file.filename)
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file.save(file_path)
            
            # Generate the file's hash
            uploaded_file_hash = generate_file_hash(file_path)
            print(f"Uploaded Movie Hash: {uploaded_file_hash}")

            # Compare with the original movie hash
            if uploaded_file_hash == original_movie_hash:
                return render_template_string(RESULT_HTML, message="Pirated content detected!")
            else:
                return render_template_string(RESULT_HTML, message="This is not pirated content.")
    return render_template_string(UPLOAD_HTML)

# HTML Template for Upload Page
UPLOAD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Piracy Checker</title>
</head>
<body>
    <h1>Upload a Movie File to Check for Piracy</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="movie_file" accept=".mp4, .mkv, .avi" required>
        <button type="submit">Check for Piracy</button>
    </form>
</body>
</html>
'''

# HTML Template for Result Page
RESULT_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Check Result</title>
</head>
<body>
    <h1>{{ message }}</h1>
    <a href="{{ url_for('index') }}">Upload Another File</a>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)