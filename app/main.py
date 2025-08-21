# gijii-app\app\main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from io import BytesIO

# ローカルのユーティリティファイルをインポート
from app.utils.file_parsers import parse_docx, parse_pdf
from app.utils.llm_client import LLMClient
from app.utils.prompt_builder import build_meeting_minutes_prompt, build_material_summary_prompt
from app.models import MeetingInput # データモデルをインポート

app = FastAPI(
    title="Gijii Backend API",
    description="LLMを用いた議事録生成のためのバックエンドAPI"
)

# CORS設定：Streamlit (フロントエンド) からのアクセスを許可
# 開発中は'*'で全て許可しても良いですが、本番環境ではフロントエンドのURLに限定してください
origins = [
    "http://localhost",
    "http://localhost:8501", # Streamlitのデフォルトポート
    # Cloud Runにデプロイ後、フロントエンドのURLもここに追加する
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Gijii Backend API is running!"}

@app.post("/generate_minutes")
async def generate_minutes(
    transcript_file: UploadFile = File(...),
    mtg_material_file: UploadFile = File(...),
    llm_type: str = Form(...),
    api_key: str = Form(...),
    our_attendees_str: str = Form(...),
    client_names_str: str = Form(...),
    meeting_format: str = Form(...)
):
    try:
        # 1. ファイル内容の読み込み
        transcript_content = await transcript_file.read()
        mtg_material_content = await mtg_material_file.read()

        # 2. ファイルのパース
        transcript_text = parse_docx(transcript_content)
        mtg_material_text = parse_pdf(mtg_material_content)

        # 3. 参加者リストの整形
        # 参加者リストの整形
        our_attendees = [a.strip() for a in our_attendees_str.split(',') if a.strip()]
        client_names = [c.strip() for c in client_names_str.split(',') if c.strip()]

        # 4. LLMクライアントの初期化
        llm = LLMClient(llm_type, api_key)

        # 5. 会議資料から目的/ゴールの要約を生成 (LLMを一度呼び出す)
        material_summary_prompt = build_material_summary_prompt(mtg_material_text)
        print(f"--- Material Summary Prompt ---:\n{material_summary_prompt[:500]}...") # デバッグ用
        mtg_purpose_summary = llm.generate_text(material_summary_prompt)
        print(f"--- Material Summary Generated ---:\n{mtg_purpose_summary[:500]}...") # デバッグ用
        if "エラー" in mtg_purpose_summary: # LLMからのエラーメッセージを検出
            raise HTTPException(status_code=500, detail=f"資料要約中にLLMエラーが発生しました: {mtg_purpose_summary}")


        # 6. 議事録生成プロンプトの構築
        minutes_prompt = build_meeting_minutes_prompt(
            mtg_purpose_summary=mtg_purpose_summary,
            our_attendees=our_attendees,
            client_names=client_names,
            transcript=transcript_text,
            meeting_format=meeting_format
        )


        # 7. LLMによる議事録の生成
        generated_minutes = llm.generate_text(minutes_prompt)
        print(f"--- Generated Minutes ---:\n{generated_minutes[:1000]}...") # デバッグ用
        if "エラー" in generated_minutes: # LLMからのエラーメッセージを検出
            raise HTTPException(status_code=500, detail=f"議事録生成中にLLMエラーが発生しました: {generated_minutes}")


        return JSONResponse(content={"minutes": generated_minutes})

    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        # その他の予期せぬエラーをキャッチ
        print(f"バックエンド処理中にエラーが発生しました: {e}")
        return JSONResponse(status_code=500, content={"error": f"サーバーエラーが発生しました: {e}"})