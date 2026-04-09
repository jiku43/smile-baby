import streamlit as st
import random
from PIL import Image
import numpy as np
import mediapipe as mp

st.title("笑顔を作るアプリ 😊 (顔認識AI版)")

# キャラクター選択
char_choice = st.radio("誰を笑わせる？", ["赤ちゃん", "柴犬"], horizontal=True)

# 画像データの定義（ファイル名は今のまま）
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
        "cry": "17734676373 (1).png",
        "pout": "17734676373 (2).png",
        "confused": "17734676373 (3).png",
        "smile": "17734676373 (4).png",
        "laugh": "17734676373 (5).png",
        "silly": "17734676373 (6).png"
    }

if 'last_status' not in st.session_state:
    st.session_state.last_status = "pout"
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = ""

# --- MediaPipe 顔認識セットアップ ---
mp_face_mesh = mp.solutions.face_mesh
# 笑顔判定に使う口元の特徴点の番号 (MediaPipe Face Mesh)
MOUTH_CORNER_LEFT = 61
MOUTH_CORNER_RIGHT = 291
MOUTH_TOP = 0
MOUTH_BOTTOM = 17

@st.cache_resource
def load_face_mesh():
    return mp_face_mesh.FaceMesh(
        static_image_mode=True, # ボタンを押した時だけ解析
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    )

face_mesh = load_face_mesh()

# 判定関数
def classify_emotion_mediapipe(img_file_buffer, face_mesh):
    # 画像をMediaPipeが扱える形式(numpy array)に変換
    img = Image.open(img_file_buffer)
    img_array = np.array(img)
    
    # 顔認識を実行
    results = face_mesh.process(img_array)
    
    if not results.multi_face_landmarks:
        st.session_state.debug_info = "顔が認識できませんでした。"
        return "confused" # 顔がない場合は困惑
    
    # 最初の顔の特徴点を取得
    face_landmarks = results.multi_face_landmarks[0].landmark
    
    # --- 笑顔判定ロジック（簡易版） ---
    # 口の両端の距離と、上下の距離を比較して、口が横に広がっているか(笑顔か)を判定
    def get_dist(p1, p2):
        return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    width = get_dist(face_landmarks[MOUTH_CORNER_LEFT], face_landmarks[MOUTH_CORNER_RIGHT])
    height = get_dist(face_landmarks[MOUTH_TOP], face_landmarks[MOUTH_BOTTOM])
    
    # 笑顔度（比率）を計算。口が横に長いほど数値が上がる。
    # 通常は2.0〜3.0くらい。3.0を超えると笑顔の可能性が高い。
    smile_score = width / (height + 1e-6) # 0除算防止
    
    # デバッグ情報の更新
    st.session_state.debug_info = f"笑顔スコア: {smile_score:.2f} (幅:{width:.3f}, 高:{height:.3f})"
    
    # 判定（閾値は要調整）
    if smile_score > 3.2:
        return "laugh" # 大笑い
    elif smile_score > 2.6:
        return "smile" # 笑顔
    elif smile_score < 2.0:
        return "cry" # 口が縦に開いている＝泣き顔
    else:
        # 変顔リアクション（確率）
        if random.random() < 0.2:
            return "silly"
        else:
            return "pout"

# --- アプリ本体 ---
# カメラ入力
img_file_buffer = st.camera_input("カメラに向かって笑ってね！")

if img_file_buffer is not None:
    # ボタンが押されたら解析を実行
    with st.spinner("AIが顔の特徴を解析中..."):
        status = classify_emotion_mediapipe(img_file_buffer, face_mesh)
        st.session_state.last_status = status

# 選択されたキャラクターの画像を表示
try:
    image = Image.open(images[st.session_state.last_status])
    st.image(image, use_container_width=True)
except Exception as e:
    st.error(f"画像が見つかりません。")

# デバッグ情報の表示（開発中のみ）
st.write(st.session_state.debug_info)

if st.session_state.last_status == "laugh":
    st.balloons()
    st.success(f"✨ AIが最高の笑顔を検知！{char_choice}も大喜び！ ✨")
elif st.session_state.last_status == "smile":
    st.info(f"😊 笑顔ですね！{char_choice}も嬉しそう。")
elif st.session_state.last_status == "silly":
    st.warning(f"🤪 あれ？変な顔？{char_choice}がびっくりしています。")
