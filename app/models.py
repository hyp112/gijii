# gijii-app\app\models.py
from pydantic import BaseModel
from typing import List, Optional

class MeetingInput(BaseModel):
    """議事録生成リクエストの入力データモデル"""
    llm_type: str                  # 'OpenAI' または 'Google'
    api_key: str                   # LLMのAPIキー
    attendees: List[str]           # 会議参加者リスト
    client_name: str               # クライアント役の参加者名
    meeting_format: str            # 議事録のフォーマット
    # transcript_content と mtg_material_content はファイルから抽出されるため、直接受け取らない
    # ファイルは別途アップロードとして受け取る