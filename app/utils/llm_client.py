# gijii-app\app\utils\llm_client.py
import openai
import google.generativeai as genai

class LLMClient:
    def __init__(self, llm_type: str, api_key: str):
        self.llm_type = llm_type
        self.api_key = api_key

        if self.llm_type == "OpenAI":
            openai.api_key = self.api_key
        elif self.llm_type == "Google":
            genai.configure(api_key=self.api_key)
        else:
            raise ValueError("Unsupported LLM type. Choose 'OpenAI' or 'Google'.")

    def generate_text(self, prompt: str) -> str:
        """
        指定されたプロンプトに基づいてLLMからテキストを生成します。
        """
        if self.llm_type == "OpenAI":
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for meeting minute generation."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=4000, 
                    temperature=0.3 
                )
                return response.choices[0].message.content
            except openai.APIError as e:
                return f"OpenAI APIエラー: {e}"
            except Exception as e:
                return f"予期せぬエラー (OpenAI): {e}"

        elif self.llm_type == "Google":
            try:
                # Gemini Pro モデルを使用
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Google Gemini APIエラー: {e}"
        else:
            return "LLMタイプが正しく設定されていません。"