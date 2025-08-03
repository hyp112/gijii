# gijii-app\app\utils\prompt_builder.py

def build_meeting_minutes_prompt(
    mtg_purpose_summary: str,
    our_attendees: list[str],
    client_name: str,
    transcript: str,
    meeting_format: str
) -> str:
    """
    議事録を生成するためのプロンプトを構築します。
    """
    prompt_template = f"""
あなたは優秀なコンサルタントマネージャです。以下の情報をもとに、クライアントに送るための議事録を作成してください。

# 会議の前提情報
会議の目的とゴール（会議資料からの要約）:
{mtg_purpose_summary}

# 会議情報
弊社参加者: {', '.join(our_attendees)} # ★表示も変更
クライアント: {client_name} # ★表示も変更

# 会議の発話記録
{transcript}

# 議事録の作成指示
1.  以下のフォーマットに従って議事録を作成してください。もしフォーマットに「会議日時」「場所」などの項目があっても、今回の入力には含まれないため、空欄にするか、適宜省略して構いません。
{meeting_format}

2.  会議の目的とゴール（資料からの要約）を参考に、**クライアントと合意できた内容**と、**合意が不十分だった、あるいは今後議論が必要な課題やNext Action**にフォーカスを当てて要約してください。
3.  特に「{client_name}」の発言は、クライアントの意向として最も重要視し、他の参加者の発言よりも重みをつけて反映させてください。
4.  議事録を書く目的は、「とても忙しいクライアントが一目見て会議内容とやるべきことを把握できる」ことです。テキスト情報のみですが、改行や空白などのUI（見た目）も重視し、使う言葉は一般的で簡潔かつ明確に、読者が一目で内容を把握できるようにまとめてください。
5.  決定事項、合意事項、課題、タスク（Next Action）を明確に区別し、箇条書きなどで分かりやすく整理してください。

議事録の出力:
"""
    return prompt_template

def build_material_summary_prompt(material_text: str) -> str:
    """
    会議資料のテキストから、会議の背景を要約するためのプロンプトを構築します。
    """
    prompt_template = f"""
以下の会議資料は、コンサル会社がクライアントに提示する資料です。
テキストを読んで、この会議の目的、主要なアジェンダ、および期待される（合意したい）ゴールを簡潔に要約してください。
箇条書きで分かりやすく整理してください。

会議資料テキスト:
{material_text}

会議の目的:
"""
    return prompt_template