import streamlit as st
import random
from PIL import Image

st.title("笑顔を作るアプリ 😊")

# ファイル名はジクさんの今の数字の名前に合わせました
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

# カメラ入力（Streamlit標準機能のみ使用）
img_file_buffer = st.camera_input("カメラに向かって笑ってね！")

if img_file_buffer is not None:
    # ここではAI判定を簡略化し、撮影するたびに「気まぐれ」で変わるようにします
    val = random.random()
    if val > 0.7:
        status = "laugh"
    elif val > 0.4:
        status = "smile"
    elif val < 0.2:
        status = "cry"
    else:
        status = "pout"
    
    st.session_state.last_status = status

# 赤ちゃんの画像を表示
try:
    image = Image.open(images[st.session_state.last_status])
    st.image(image, use_container_width=True)
except Exception as e:
    st.error(f"画像が見つかりません: {st.session_state.last_status}")

if st.session_state.last_status == "laugh":
    st.balloons()
    st.success("✨ ナイススマイル！ベストショットです ✨")
