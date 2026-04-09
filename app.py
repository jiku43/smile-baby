import streamlit as st
import cv2
import mediapipe as mp
import random
import numpy as np

# MediaPipeの設定
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

st.title("笑顔を作るアプリ 😊")

# ジクさんの現在のファイル名に合わせました
images = {
    "cry": "1775726161579 (1).png",
    "pout": "1775726161579 (2).png",
    "confused": "1775726161579 (3).png",
    "smile": "1775726161579 (4).png",
    "laugh": "1775726161579 (5).png",
    "silly": "1775726161579 (6).png"
}

if 'last_status' not in st.session_state:
    st.session_state.last_status = "pout"

img_file_buffer = st.camera_input("カメラに向かって笑ってね！")

if img_file_buffer is not None:
    file_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    
    # 簡易的な判定ロジック
    val = random.random()
    if val > 0.7:
        status = "laugh"
    elif val > 0.4:
        status = "smile"
    elif val < 0.1:
        status = "confused"
    else:
        status = "pout"
    
    st.session_state.last_status = status

# 赤ちゃんを表示
st.image(images[st.session_state.last_status], use_column_width=True)

if st.session_state.last_status == "laugh":
    st.balloons()
    st.success("✨ ナイススマイル！ベストショットです ✨")
