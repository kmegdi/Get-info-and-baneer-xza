from flask import Flask, request, jsonify, send_file
import requests
import re
import io

app = Flask(__name__)

API_KEY = "XZA1"

def is_valid_uid(uid):
    return re.match(r"^\d{5,20}$", uid)

@app.route("/get-player-info", methods=["GET"])
def get_player_info():
    uid = request.args.get("uid")
    key = request.args.get("key")

    if key != API_KEY:
        return jsonify({"error": "❌ Invalid API Key"}), 401

    if not uid or not is_valid_uid(uid):
        return jsonify({"error": "❌ Invalid or missing UID"}), 400

    try:
        info_url = f"https://info-ch9ayfa.vercel.app/{uid}"
        info_response = requests.get(info_url)

        if info_response.status_code != 200:
            return jsonify({"error": "⚠️ Failed to fetch player data"}), 500

        info_data = info_response.json()

        if not info_data or 'nickname' not in info_data:
            return jsonify({"error": "⚠️ Player not found"}), 404

        banner_url = f"https://aditya-banner-v9op.onrender.com/banner-image?uid={uid}&region=sg"

        response = {
            "status": "✅ success",
            "uid": uid,
            "nickname": info_data.get("nickname", "N/A"),
            "all_data": info_data,
            "banner_image": banner_url
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "🔥 Internal Server Error", "details": str(e)}), 500

@app.route("/get-banner", methods=["GET"])
def get_banner():
    uid = request.args.get("uid")
    key = request.args.get("key")

    if key != API_KEY:
        return jsonify({"error": "❌ Invalid API Key"}), 401

    if not uid or not is_valid_uid(uid):
        return jsonify({"error": "❌ Invalid or missing UID"}), 400

    try:
        banner_url = f"https://aditya-banner-v9op.onrender.com/banner-image?uid={uid}&region=sg"
        img_response = requests.get(banner_url)
        if img_response.status_code != 200:
            return jsonify({"error": "⚠️ Failed to fetch banner image"}), 500

        return send_file(
            io.BytesIO(img_response.content),
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='Banner.jpg'
        )

    except Exception as e:
        return jsonify({"error": "🔥 Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
