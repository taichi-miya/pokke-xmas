import streamlit as st
import os
import base64

# 背景画像を設定する関数
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()  # Base64エンコード → UTF-8文字列化
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/jpeg;base64,{encoded_image});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 背景画像のパスを指定
add_bg_from_local("background.jpg")  # 使用する背景画像（JPEG形式対応）

# アプリのタイトル
st.title("ぽっけサンタからのプレゼント")

# 画像保存用フォルダ
image_folder = "uploaded_images"
os.makedirs(image_folder, exist_ok=True)

# 管理者用セクション
st.sidebar.title("管理者用")
uploaded_files = st.sidebar.file_uploader(
    "画像を複数アップロードしてください", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(image_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
    st.sidebar.success(f"{len(uploaded_files)} 枚の画像がアップロードされました！")

# アクセス者用セクション
st.write("🎁 **プレゼントを選択してください！**")

# 保存された画像のリストを取得
image_files = os.listdir(image_folder)

# ファイル名をカスタム表示用の名前に変換
custom_names = [f"{i + 1}つめ" for i in range(len(image_files))]  # 例: "1つめ", "2つめ"

if image_files:
    # カスタム表示名とファイルパスを対応付ける辞書を作成
    file_mapping = dict(zip(custom_names, image_files))

    # カスタム名で画像を選択
    selected_name = st.selectbox("表示する画像を選択してください", custom_names)

    # 選択されたカスタム名に対応する実際のファイル名を取得
    selected_image_path = os.path.join(image_folder, file_mapping[selected_name])

    # ボタンで画像を表示
    if st.button("画像を表示"):
        st.image(selected_image_path, caption=selected_name, use_column_width=True)

    # ダウンロードボタン
    with open(selected_image_path, "rb") as f:
        st.download_button(
            label="📥 選択した画像をダウンロードする",
            data=f,
            file_name=file_mapping[selected_name],
            mime="image/jpeg"
        )
else:
    st.warning("現在利用可能な画像がありません。管理者が画像をアップロードするのをお待ちください。")
