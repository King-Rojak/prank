from flask import Flask, request, jsonify
from flask_cors import CORS
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

app = Flask(__name__)
CORS(app)  # Izinkan akses dari halaman web

def set_volume_to_max():
    """Set volume sistem ke 100% dan unmute."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Unmute jika perlu
    if volume.GetMute():
        volume.SetMute(0, None)
    
    # Set ke 100% (nilai 1.0 pada skala 0.0 - 1.0)
    volume.SetMasterVolumeLevelScalar(1.0, None)

@app.route('/trigger-prank', methods=['POST'])
def trigger_prank():
    try:
        set_volume_to_max()
        return jsonify({"status": "success", "message": "Volume dimaksimalkan!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)