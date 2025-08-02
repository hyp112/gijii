import streamlit as st

# --- アプリの基本設定 ---
st.set_page_config(
    page_title="Gijii",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄Gijii")
st.write("会議の音声書き起こしと資料から、クライアントへ送るべき議事を自動生成します。")

# --- サイドバー (設定項目) ---
st.sidebar.header("🔑 APIキー設定")
selected_llm = st.sidebar.radio("使用するLLMを選択", ("OpenAI (ChatGPT)", "Google (Gemini)"))

if selected_llm == "OpenAI (ChatGPT)":
    openai_api_key = st.sidebar.text_input("OpenAI APIキーを入力してください", type="password")
else:
    gemini_api_key = st.sidebar.text_input("Google Gemini APIキーを入力してください", type="password")

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 会議情報の設定")

# --- メインコンテンツ ---

st.header("1. 会議参加者と役割の指定")
st.info("クライアント役を指定すると、その方の発言が議事録作成時に特に重視されます。", icon="ℹ️")

# 会議参加者入力
attendees_raw = st.text_area(
    "会議参加者名をカンマ区切りで入力してください（例: 田中部長, 鈴木さん, クライアントA社の佐藤様）",
    height=80
)
# 入力された参加者名をリストに変換（後でバックエンドに渡すため）
attendees = [a.strip() for a in attendees_raw.split(',') if a.strip()]

# クライアント役の選択
if attendees: # 参加者が入力されていれば選択肢を表示
    client_name = st.selectbox(
        "クライアント役の参加者を選択してください",
        ["選択してください"] + attendees
    )
else:
    client_name = "選択してください"
    st.warning("会議参加者を入力すると、クライアント役を選択できるようになります。")

st.markdown("---")

st.header("2. 議事録フォーマットの指定")
st.info("社内規定の議事録フォーマットをここに貼り付けてください。LLMがこのフォーマットに従って議事録を生成します。", icon="📝")
meeting_format = st.text_area(
    "議事録のフォーマットを入力してください",
    "例: 日時:\\n場所:\\n参加者:\\n【貴社ご依頼事項】\\n【弊社TODO】\\n主な議事と決定事項\\n決定事項1...::",
    height=200
)

st.markdown("---")

st.header("3. 会議データのアップロード")

uploaded_transcript_file = st.file_uploader(
    "発話書き起こしWordファイル (.docx) をアップロードしてください",
    type=["docx"]
)

uploaded_mtg_material_file = st.file_uploader(
    "会議で使用した資料ファイル (.pdf) をアップロードしてください",
    type=["pdf"]
)

st.markdown("---")

# --- 議事録生成ボタン ---
st.header("4. 議事録の生成")

if st.button("議事録を生成する"):

    if not (uploaded_transcript_file and uploaded_mtg_material_file):
        st.error("発話書き起こしファイルと会議資料の両方をアップロードしてください。")
    elif not attendees:
        st.error("会議参加者を入力してください。")
    elif client_name == "選択してください":
        st.error("クライアント役の参加者を選択してください。")
    elif not meeting_format:
        st.error("議事録フォーマットを入力してください。")
    elif selected_llm == "OpenAI (ChatGPT)" and not openai_api_key:
        st.error("OpenAI APIキーを入力してください。")
    elif selected_llm == "Google (Gemini)" and not gemini_api_key:
        st.error("Google Gemini APIキーを入力してください。")
    else:
        # ここにバックエンドへのリクエスト処理を書きます
        # まずはローカルのFastAPIに接続
        backend_url = "https://gijii-backend-service-764092828828.asia-northeast1.run.app/generate_minutes"

        # リクエストボディの準備
        # FastAPIのForm型で受け取るため、ファイルとフォームデータを分ける
        files = {
            "transcript_file": uploaded_transcript_file.getvalue(),
            "mtg_material_file": uploaded_mtg_material_file.getvalue()
        }
        data = {
            "llm_type": selected_llm.split(' ')[0], # "OpenAI (ChatGPT)"から"OpenAI"を抽出
            "api_key": openai_api_key if selected_llm == "OpenAI (ChatGPT)" else gemini_api_key,
            "attendees_str": attendees_raw, # カンマ区切りのまま渡す
            "client_name": client_name,
            "meeting_format": meeting_format
        }

        st.info("議事録を生成中...しばらくお待ちください。")
        with st.spinner("LLMが議事録を作成しています..."):
            try:
                import requests # requestsライブラリをインポート

                response = requests.post(backend_url, files=files, data=data)

                if response.status_code == 200:
                    result = response.json()
                    generated_minutes = result.get("minutes", "議事録の生成に失敗しました。")
                    st.success("議事録が生成されました！")
                    st.markdown("---")
                    st.subheader("生成された議事録")
                    st.code(generated_minutes, language="markdown") # Markdown形式で表示
                else:
                    error_detail = response.json().get("detail", "不明なエラー")
                    st.error(f"議事録の生成に失敗しました。エラーコード: {response.status_code} 詳細: {error_detail}")
            except requests.exceptions.ConnectionError:
                st.error("バックエンドサーバーに接続できません。FastAPIサーバーが起動しているか確認してください。")
            except Exception as e:
                st.error(f"予期せぬエラーが発生しました: {e}")

        # 既存の確認用出力は削除またはコメントアウト
        # st.write("---")
        # st.subheader("現在の入力値（確認用）")
        # ...