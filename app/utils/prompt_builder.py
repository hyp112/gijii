# gijii-app\app\utils\prompt_builder.py

def build_meeting_minutes_prompt(
    mtg_purpose_summary: str,
    attendees: list[str],
    client_name: str,
    transcript: str,
    meeting_format: str
) -> str:
    """
    LLMが議事録を生成するためのプロンプトを構築します。
    """
    prompt_template = f"""
あなたは優秀なビジネスアシスタントです。以下の情報をもとに、クライアントに送るための議事録を作成してください。

# 会議の前提情報
会議の目的とゴール（資料からの要約）:
{mtg_purpose_summary}

# 会議情報
会議参加者: {', '.join(attendees)}
クライアント役: {client_name}

# 会議の発話記録
{transcript}

# 議事録の作成指示
1.  以下のフォーマットに従って議事録を作成してください。もしフォーマットに「会議日時」「場所」などの項目があっても、今回の入力には含まれないため、空欄にするか、適宜省略して構いません。
{meeting_format}

2.  会議の目的とゴール（資料からの要約）を参考に、**クライアントと合意できた内容**と、**合意が不十分だった、あるいは今後議論が必要な課題やNext Action**にフォーカスを当てて要約してください。
3.  特に「{client_name}」の発言は、クライアントの意向として最も重要視し、他の参加者の発言よりも重みをつけて反映させてください。
4.  議事録は簡潔かつ明確に、読者が一目で内容を把握できるようにまとめてください。
5.  決定事項、合意事項、課題、タスク（Next Action）を明確に区別し、箇条書きなどで分かりやすく整理してください。

議事録の出力:
"""
    return prompt_template

def build_material_summary_prompt(material_text: str) -> str:
    """
    会議資料のテキストから、会議の目的やゴールを要約するためのプロンプトを構築します。
    """
    prompt_template = f"""
以下の会議資料のテキストを読んで、この会議の目的、主要なアジェンダ、および期待される（合意したい）ゴールを簡潔に要約してください。
箇条書きで分かりやすく整理してください。

会議資料テキスト:
{material_text}

会議の目的とゴール:
"""
    return prompt_template