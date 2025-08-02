# gijii-app/Dockerfile

# Pythonの公式イメージをベースにする (Python 3.11 を推奨)
# Cloud RunはDebianベースの環境で実行されるため、buster-slimやbullseye-slimが良い選択肢
FROM python:3.11-slim-bullseye

# 作業ディレクトリを /app に設定
WORKDIR /app

# プロジェクトの依存関係をコピー (requirements.txt)
# 依存関係の変更が少ない場合、先にコピーしてキャッシュを効かせる
COPY requirements.txt .

# 依存関係をインストール
# --no-cache-dir: キャッシュを使わない (イメージサイズを小さくするため)
# -r: requirements.txt からインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードを全てコピー
# requirements.txt の後にコピーすることで、コード変更時のキャッシュを効かせる
COPY . .

# FastAPIアプリケーションがリッスンするポートを環境変数で設定
# Cloud Runは環境変数PORTで指定されたポートでリッスンする必要がある
ENV PORT 8080

# アプリケーションを起動するコマンド
# uvicorn は本番環境で推奨されるGunicornなどのWSGIサーバーと組み合わせることが多いが、
# Cloud Runでは単体で動かすことも可能。ここではシンプルに uvicorn を直接使用。
# --host 0.0.0.0: 外部からのアクセスを許可するために必須
# app.main:app: appディレクトリのmain.pyファイル内のappインスタンスを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]