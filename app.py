from flask import Flask, render_template, request, redirect, url_for, send_from_directory
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
    global video
    video = request.files['video']

    if video.filename == "":
        return 'No video file selected'

    if video and allowed_file(video.filename):
        # Create the directory if it doesn't exist
        upload_dir = 'data/'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        global video_path
        video_path = os.path.join(upload_dir, video.filename)
        video.save(video_path)

        # Redirect back to the upload page after upload
        return redirect(url_for('output', video_name=video.filename))
    
    return 'Error uploading video'

@app.route('/output')
def output():
    video_name = request.args.get('video_name')
    return render_template('output.html', video_name=video_name)

@app.route('/process', methods=['GET','POST'])
def process():
    # Add any processing logic here if needed
    # This route will be triggered when the form is submitted
    
    # Redirect to a different route after processing
    return redirect(url_for('success'))

@app.route('/success')
def success():
    # This is the route where the user will be redirected after processing
    return redirect(url_for('serve_video', filename=video.filename))

# Route for serving the uploaded video
@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run(debug=True)
