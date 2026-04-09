import streamlit as st
import random
from PIL import Image

st.title("笑顔を作るアプリ 😊")

# キャラクター選択
char_choice = st.radio("誰を笑わせる？", ["赤ちゃん", "柴犬"], horizontal=True)

# 画像データの定義
if char_choice == "赤ちゃん":
    images = {
        "cry": "1775726161579 (1).png",
        "pout": "1775726161579 (2).png",
        "confused": "1775726161579 (3).png",
        "smile": "1775726161579 (4).png",
        "laugh": "1775726161579 (5).png",
        "silly": "1775726161579 (6).png"
    }
else:  # 柴犬
    images = {
        "cry": "1775734676373 (1).png",
        "pout": "1775734676373 (2).png",
        "confused": "1775734676373 (3).png",
        "smile": "1775734676373 (4).png",
        "laugh": "1775734676373 (5).png",
        "silly": "1775734676373 (6).png"
    }

if 'last_status' not in st.session_state:
    st.session_state.last_status = "pout"

# カメラ入力
img_file_buffer = st.camera_input("カメラに向かって笑ってね！")

if img_file_buffer is not None:
    # 判定ロジック
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

# 選択されたキャラクターの画像を表示
try:
    image = Image.open(images[st.session_state.last_status])
    st.image(image, use_container_width=True)
except Exception as e:
    st.error(f"画像が見つかりません。ファイル名を確認してください。")

if st.session_state.last_status == "laugh":
    st.balloons()
    st.success(f"✨ ナイススマイル！{char_choice}も喜んでます ✨")
