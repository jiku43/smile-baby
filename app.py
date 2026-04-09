import streamlit as st
import cv2
import mediapipe as mp
import random
import time

# MediaPipeの設定（表情認識用）
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

st.title("笑顔を作るアプリ 😊")
st.write("カメラに向かって笑ったり、変顔をしてみよう！")

# 画像の読み込み（保存したファイル名に合わせてください）
images = {
    "cry": "baby_cry.jpg",
    "pout": "baby_pout.jpg",
    "confused": "baby_confused.jpg",
    "smile": "baby_smile.jpg",
    "laugh": "baby_laugh.jpg",
    "silly": "baby_silly.jpg"
}

# 状態管理（前回の表情を覚えておく）
if 'last_status' not in st.session_state:
    st.session_state.last_status = "pout"

# カメラ入力
img_file_buffer = st.camera_input("あなたの顔を映してね")

if img_file_buffer is not None:
    # 画像をOpenCV形式に変換
    import numpy as np
    file_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 表情分析
    results = face_mesh.process(rgb_frame)

    status = "pout" # デフォルト

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 簡易的な笑顔判定（口角の距離などで判定）
            # 本来は詳細な座標計算が必要ですが、ここでは「笑顔」「変顔」の分岐ロジックを優先
            
            # --- ここで表情判定ロジック（例） ---
            # 笑顔度が高い場合 -> status = "smile" または "laugh"
            # 怒り/無表情 -> status = "cry"
            # 変顔（大きく口を開けるなど） -> status = "random"
            
            # 今回はシミュレーションとしてランダム要素を強めに入れます
            val = random.random()
            if val > 0.8:
                status = "laugh"
            elif val > 0.5:
                status = "smile"
            elif val < 0.1:
                # 「変顔」への気まぐれリアクション
                status = random.choice(["laugh", "confused"])
            else:
                status = "pout"

    st.session_state.last_status = status

# 赤ちゃんの画像を表示
st.image(images[st.session_state.last_status], width=400)

# ベストショット判定（笑顔が最大の時）
if st.session_state.last_status == "laugh":
    st.success("✨ ベストショット！自動保存しました（想定） ✨")
    # ここに画像保存処理を追加可能
