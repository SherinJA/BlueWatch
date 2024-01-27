from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for rendering the upload page
@app.route('/upload', methods=['GET'])
def render_upload_page():
    return render_template('upload.html')

allowed = ['mp4']
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

# Route for handling video upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return 'No video selected'
    
    video = request.files['video']

    if video.filename == "":
        return 'No video file selected'

    if video and allowed_file(video.filename):
        # Create the directory if it doesn't exist
        upload_dir = 'data/'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Save the uploaded video file
        video_path = os.path.join(upload_dir, video.filename)
        video.save(video_path)

        # Redirect to route that serves the uploaded video
        return redirect(url_for('serve_video', filename=video.filename))

    return 'Error uploading video'

# Route for serving the uploaded video
@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run(debug=True)
