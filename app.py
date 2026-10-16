# import streamlit as st
# from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
# from ultralytics import YOLO
# import av
# import cv2

# st.set_page_config(page_title="Mining Safety PPE Detector", layout="wide")
# st.title("⛑️ Mining Safety - PPE Detection")
# st.markdown("Live detection of helmet, vest, and boot compliance.")

# model = YOLO("ppe_model.pt")

# CLASS_COLORS = {
#     "helmet": (0, 255, 0), "vest": (0, 255, 0), "boot": (0, 255, 0),
#     "no-helmet": (0, 0, 255), "no-vest": (0, 0, 255), "no-boot": (0, 0, 255),
#     "undefined": (255, 255, 0),
# }

# class PPEProcessor(VideoProcessorBase):
#     def __init__(self):
#         self.conf_threshold = 0.5

#     def recv(self, frame):
#         img = frame.to_ndarray(format="bgr24")

#         results = model.predict(img, conf=self.conf_threshold, verbose=False)[0]
#         detected_classes = [model.names[int(box.cls)] for box in results.boxes]

#         for box in results.boxes:
#             cls_name = model.names[int(box.cls)]
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             color = CLASS_COLORS.get(cls_name, (255, 255, 0))
#             cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
#             cv2.putText(img, cls_name, (x1, y1 - 8),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#         violations = [c for c in detected_classes if c.startswith("no-")]
#         status = "VIOLATION DETECTED" if violations else "PPE COMPLIANT"
#         banner_color = (0, 0, 255) if violations else (0, 200, 0)
#         cv2.rectangle(img, (0, 0), (img.shape[1], 40), banner_color, -1)
#         cv2.putText(img, status, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

#         return av.VideoFrame.from_ndarray(img, format="bgr24")


# col1, col2 = st.columns([3, 1])

# with col1:
#     ctx = webrtc_streamer(
#         key="ppe-detection",
#         video_processor_factory=PPEProcessor,
#         media_stream_constraints={"video": True, "audio": False},
#     )

# with col2:
#     st.subheader("Settings")
#     if ctx.video_processor:
#         conf = st.slider("Confidence threshold", 0.1, 1.0, 0.5, 0.05)
#         ctx.video_processor.conf_threshold = conf

#     st.subheader("Classes")
#     st.markdown("🟢 helmet, vest, boot")
#     st.markdown("🔴 no-helmet, no-vest, no-boot")
















import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
from ultralytics import YOLO
import av
import cv2

st.set_page_config(page_title="Mining Safety PPE Detector", layout="wide")
st.title("⛑️ Mining Safety - PPE Detection")
st.markdown("Live detection of helmet, vest, and boot compliance.")

# Cache the model so it only loads once, not on every interaction/rerun
@st.cache_resource
def load_model():
    return YOLO("ppe_model.pt")

with st.spinner("Loading model..."):
    try:
        model = load_model()
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        st.stop()

CLASS_COLORS = {
    "helmet": (0, 255, 0), "vest": (0, 255, 0), "boot": (0, 255, 0),
    "no-helmet": (0, 0, 255), "no-vest": (0, 0, 255), "no-boot": (0, 0, 255),
    "undefined": (255, 255, 0),
}

# STUN server so WebRTC can connect once deployed (not needed on localhost, but required in the cloud)
# RTC_CONFIGURATION = RTCConfiguration(
#     {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
# )

# RTC_CONFIGURATION = RTCConfiguration(
#     {
#         "iceServers": [
#             {"urls": ["stun:stun.relay.metered.ca:80"]},
#             {
#                 "urls": ["turn:global.relay.metered.ca:80"],
#                 "username": "openrelayproject",
#                 "credential": "openrelayproject",
#             },
#             {
#                 "urls": ["turn:global.relay.metered.ca:443"],
#                 "username": "openrelayproject",
#                 "credential": "openrelayproject",
#             },
#         ]
#     }
# )




RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": ["turn:global.relay.metered.ca:80?transport=tcp"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
            {
                "urls": ["turn:global.relay.metered.ca:443?transport=tcp"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
            {
                "urls": ["turns:global.relay.metered.ca:443?transport=tcp"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
        ]
    }
)




class PPEProcessor(VideoProcessorBase):
    def __init__(self):
        self.conf_threshold = 0.5

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        results = model.predict(img, conf=self.conf_threshold, verbose=False)[0]
        detected_classes = [model.names[int(box.cls)] for box in results.boxes]

        for box in results.boxes:
            cls_name = model.names[int(box.cls)]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = CLASS_COLORS.get(cls_name, (255, 255, 0))
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, cls_name, (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        violations = [c for c in detected_classes if c.startswith("no-")]
        status = "VIOLATION DETECTED" if violations else "PPE COMPLIANT"
        banner_color = (0, 0, 255) if violations else (0, 200, 0)
        cv2.rectangle(img, (0, 0), (img.shape[1], 40), banner_color, -1)
        cv2.putText(img, status, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


col1, col2 = st.columns([3, 1])

with col1:
    ctx = webrtc_streamer(
        key="ppe-detection",
        video_processor_factory=PPEProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
    )

with col2:
    st.subheader("Settings")
    if ctx.video_processor:
        conf = st.slider("Confidence threshold", 0.1, 1.0, 0.5, 0.05)
        ctx.video_processor.conf_threshold = conf

    st.subheader("Classes")
    st.markdown("🟢 helmet, vest, boot")
    st.markdown("🔴 no-helmet, no-vest, no-boot")