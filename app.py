import streamlit as st
import random
from PIL import Image, ImageStat
import numpy as np

st.title("笑顔を作るアプリ 😊 (AI判定版)")

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
        "cry": "1775734676373 (1).png",
        "pout": "1775734676373 (2).png",
        "confused": "1775734676373 (3).png",
        "smile": "1775734676373 (4).png",
        "laugh": "1775734676373 (5).png",
        "silly": "1775734676373 (6).png"
    }

if 'last_status' not in st.session_state:
    st.session_state.last_status = "pout"
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = ""

# カメラ入力
img_file_buffer = st.camera_input("カメラに向かって笑ってね！")

if img_file_buffer is not None:
    # --- 簡易表情判定ロジック ---
    # 1. 画像を読み込む
    img = Image.open(img_file_buffer)
    
    # 2. 画像の明るさの標準偏差（色のばらつき）を計算
    # 笑顔だと口や目が細くなり、画像全体の色のばらつきが少し変わる傾向を利用
    stat = ImageStat.Stat(img)
    std_dev = np.mean(stat.stddev)
    
    # デバッグ情報の更新（どのくらいの数値が出ているか確認用）
    st.session_state.debug_info = f"画像解析数値: {std_dev:.2f}"

    # 3. 数値に基づいて表情を決定（閾値は要調整）
    # 一般的に、笑顔だと顔のパーツが動くため、std_devが少し上がる傾向があります。
    # 以下の数値（60, 40）は目安です。ジクさんの環境に合わせて調整が必要です。
    if std_dev > 60:
        status = "laugh"
    elif std_dev > 40:
        status = "smile"
    elif std_dev < 30:
        # あまりに動きがない＝怒り/無表情
        status = "cry"
    else:
        # 「変顔」の判定は、std_devが激しく動く時などに確率で入れる
        if random.random() < 0.2: # 20%の確率で変顔リアクション
            status = "confused"
        else:
            status = "pout"
    
    st.session_state.last_status = status

# 選択されたキャラクターの画像を表示
try:
    image = Image.open(images[st.session_state.last_status])
    st.image(image, use_container_width=True)
except Exception as e:
    st.error(f"画像が見つかりません。")

# デバッグ情報の表示（開発中のみ）
# st.write(st.session_state.debug_info)

if st.session_state.last_status == "laugh":
    st.balloons()
    st.success(f"✨ AIが笑顔を検知！{char_choice}も大喜び！ ✨")
elif st.session_state.last_status == "smile":
    st.info(f"😊 笑顔ですね！{char_choice}も嬉しそう。")
