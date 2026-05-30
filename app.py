from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    search_query = request.args.get('search')
    
    if not search_query:
        return jsonify({"error": "No search query provided"}), 400
        
    if search_query == "ping":
        return jsonify({"status": "Server is alive and awake!"}), 200

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                audio_url = info['entries'][0]['url']
                return jsonify({"stream_url": audio_url})
            else:
                return jsonify({"error": "No video found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
                       
