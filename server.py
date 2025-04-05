from flask import Flask, request, jsonify, render_template, send_from_directory
from main import main
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('web.html')

@app.route('/generate', methods=['POST'])
def generate():
    print("Received request at /generate")  # Debugging statement
    data = request.get_json()
    link = data['link']
    is_reddit_thread = data['is_reddit_thread']
    print(f"Link: {link}, Is Reddit Thread: {is_reddit_thread}")  # Debugging statement

    # Process the link based on the is_reddit_thread value (True/False)
    if is_reddit_thread:
        main(link, llm=True)
    else:
        main(link)

    # Assuming the video is saved as 'subway.mp4' in the 'assets' directory
    video_filename = 'final.mp4'
    video_path = os.path.join('final', video_filename)
    if os.path.exists(video_path):
        print("Video generation successful")  # Debugging statement
        return jsonify({'video_url': f'/final/{video_filename}'})
    else:
        print("Video generation failed")  # Debugging statement
        return jsonify({'error': 'Video generation failed'}), 500

@app.route('/final/<path:filename>')
def serve_video(filename):
    return send_from_directory('final', filename)

if __name__ == "__main__":
    app.run(debug=True)