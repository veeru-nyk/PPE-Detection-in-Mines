# ⛑️ Mining Safety - PPE Detection

A real-time Personal Protective Equipment (PPE) detection app for mining safety. It uses a custom-trained **YOLO** model and a **Streamlit** web interface to check, from a live webcam feed, whether workers are wearing a helmet, vest and boots.

## Features

- Live webcam detection in the browser using WebRTC
- Detects both compliance and violations:
  - 🟢 `helmet`, `vest`, `boot`
  - 🔴 `no-helmet`, `no-vest`, `no-boot`
- Colour-coded bounding boxes with class labels
- Status banner on the video: green **PPE COMPLIANT** or red **VIOLATION DETECTED**
- Adjustable confidence threshold slider
- Model is cached so it loads only once

## Tech Stack

- Python 3.11
- [Streamlit](https://streamlit.io/)
- [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc)
- [Ultralytics YOLO](https://docs.ultralytics.com/)
- OpenCV
- PyAV

## Project Structure

```
PPE-Detection-in-Mines/
├── app.py            # Streamlit application
├── ppe_model.pt      # Trained YOLO model weights
├── requirements.txt  # Python dependencies
├── packages.txt      # System packages (for Streamlit Cloud deployment)
├── runtime.txt       # Python version (for deployment)
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 – 3.12
- A webcam
- Internet connection (used by the WebRTC TURN server)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/veeru-nyk/PPE-Detection-in-Mines.git
   cd PPE-Detection-in-Mines
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate it**
   - Windows (PowerShell): `venv\Scripts\activate`
   - Windows (CMD): `venv\Scripts\activate.bat`
   - Mac/Linux: `source venv/bin/activate`

   > On PowerShell, if you get a script execution error, run
   > `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Run the App

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**.

## How to Use

1. Click **START** in the video panel and allow camera access.
2. Stand in front of the camera. Detections and the status banner update live.
3. Use the **Confidence threshold** slider to make detection stricter or more lenient.

## How It Works

1. Each webcam frame is captured through `streamlit-webrtc`.
2. The frame is passed to the YOLO model (`ppe_model.pt`) for inference.
3. Detected objects are drawn on the frame with colour-coded boxes.
4. If any class starting with `no-` is detected, the banner shows **VIOLATION DETECTED**; otherwise it shows **PPE COMPLIANT**.

## Troubleshooting

| Problem | Fix |
|---|---|
| Video doesn't connect | Check your internet/firewall. On localhost only, you can remove the `rtc_configuration=RTC_CONFIGURATION` line in `app.py`. |
| Camera not working | Close other apps using the webcam (Zoom, Teams) and allow camera permission in the browser. |
| Laggy video | The model runs on CPU by default. Install the CUDA build of PyTorch if you have an NVIDIA GPU. |
| `pip install` fails on `av` | Upgrade pip: `python -m pip install --upgrade pip`, and use Python 3.10–3.12. |

## Deployment

The `packages.txt` and `runtime.txt` files are provided for deploying on **Streamlit Community Cloud**. Deployed apps need a working TURN server for WebRTC, which is already configured in `app.py`.

## Future Improvements

- Support for uploaded images and videos
- Alerts or logging when violations are detected
- Violation counts and a dashboard
- Additional PPE classes (gloves, goggles, masks)

## License

Add your preferred license here (e.g. MIT).

## Author

**Your Name**
GitHub: [@veeru-nyk](https://github.com/veeru-nyk)