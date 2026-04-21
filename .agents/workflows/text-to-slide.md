---
description: PDFからスライド資料作成
---

# text-to-slide

テキストファイルまたはPDF資料のパスを受け取り、学生ノート風デザインのスライド画像（2K・16:9）を全自動で生成するワークフローです。
ユーザーが「/text-to-slide」と入力するか、資料のパスを渡した際に起動します。

---

## Step 1: 資料の読み込みと内容の把握

// turbo

ユーザーから渡されたファイルを読み込み、内容を把握します。

- **テキストファイル（.txt, .md）の場合**: `view_file` ツールで直接読み込む。
- **PDFファイルの場合**: 以下のPythonスクリプトでテキストを抽出してから読み込む。

```python
# PDF抽出 (pypdfが必要: pip install pypdf)
import pypdf

pdf_path = "<ユーザーから渡されたPDFのパス>"
reader = pypdf.PdfReader(pdf_path)
text = "\n".join([page.extract_text() for page in reader.pages])
print(text)
```

抽出したテキストを `run_command` で実行し、内容を把握する。
読み込みが完了したら、内容の要約を日本語でユーザーに提示する。

---

## Step 2: スライド構成案の作成（Markdown）

// turbo

読み込んだ内容をもとに、以下のフォーマットに従ってスライドの構成案を作成します。

### 構成ルール
- 枚数は**7枚前後（内容に応じて可変）**とする。
- 必ず以下の3種類のスライドを含める:
  - **1枚目**: タイトルスライド（資料名・日付）
  - **2枚目**: 目次・アジェンダ
  - **最終枚**: まとめ・Next Action
- 中間スライドは、元資料の主要なトピックを1枚1テーマで構成する。

### 出力フォーマット（Markdown）
各スライドを `---`（水平線）で区切り、以下の構造で出力する:

```markdown
---
# [スライドタイトル]

- 箇条書きの要点1
- 箇条書きの要点2（強調したい部分は**太字**または`コードブロック`を使う）
- 💡 ポイントや補足事項

---
```

構成案を作成したら、ユーザーに提示して確認を求める。
ユーザーの承認後、Step 3 に進む。

---

## Step 3: スライド生成スクリプト（`generate_slides.py`）の作成

// turbo

Step 2 で確定した構成案をもとに、Pythonスクリプト `generate_slides.py` を作成します。
スクリプトは `write_to_file` ツールを使用して、プロジェクトのルートディレクトリに保存します。

### スクリプトの仕様

#### 3-1. スライドの定義
各スライドを Python の `list` で定義する。各要素に `filename`（ファイル名）と `html`（スライドのHTMLコンテンツ）を持たせる。

```python
slides = [
    {
        "filename": "1_タイトル",
        "html": "<div class='slide'>...</div>"
    },
    # ... 以下、各スライド
]
```

#### 3-2. デザイン（CSS）の仕様
以下のデザイン要素を必ず適用する。

| デザイン要素 | CSSの実装方法 |
|---|---|
| **大学ノート風の背景** | `linear-gradient` で罫線柄とバインダーの穴を表現 |
| **付箋（Post-it）** | `background-color: #fffac1`, `box-shadow`, `transform: rotate()` で傾きをつける |
| **蛍光ペンのハイライト** | `background: linear-gradient(transparent 60%, #fff200 60%)` |
| **情報ブロック（重要）** | 左に太いボーダーをつけた `div`（緑・青・赤など色分け） |
| **Webフォント** | Google Fonts の `Zen Kaku Gothic New` を使用 |

#### 3-3. 画面サイズと撮影仕様
```python
# Playwright起動時の設定
page = await browser.new_page(viewport={'width': 2560, 'height': 1440})  # 2K・16:9
```

#### 3-4. 出力ディレクトリの命名規則
```python
import datetime
now = datetime.datetime.now()
dir_name = now.strftime('%Y-%m-%d-%H')  # 例: 2026-04-21-10
output_dir = os.path.join("Outputs", dir_name)
os.makedirs(output_dir, exist_ok=True)
```

#### 3-5. スクリプトの全体フロー（`asyncio` + `playwright`）
```python
import os, datetime, asyncio
from playwright.async_api import async_playwright

async def generate():
    # 1. 出力ディレクトリ作成
    now = datetime.datetime.now()
    output_dir = os.path.join("Outputs", now.strftime('%Y-%m-%d-%H'))
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. ブラウザ起動（ヘッドレス）
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 2560, 'height': 1440})
        
        for slide in slides:
            # 3. HTMLを一時ファイルに書き出し
            html_path = "temp_slide.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(HTML_TEMPLATE.format(css=CSS, content=slide["html"]))
            
            # 4. ブラウザで開く
            await page.goto(f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}")
            
            # 5. フォント読み込み待機
            await page.evaluate('document.fonts.ready')
            await asyncio.sleep(0.5)
            
            # 6. スクリーンショット撮影
            out_path = os.path.join(output_dir, f"{slide['filename']}.png")
            await page.screenshot(path=out_path, type="png")
        
        await browser.close()
    
    # 7. 一時ファイル削除
    if os.path.exists("temp_slide.html"):
        os.remove("temp_slide.html")
    
    print(f"✅ 生成完了: {output_dir}")

if __name__ == '__main__':
    asyncio.run(generate())
```

> [!NOTE]
> Playwright が未インストールの場合は、Step 4 の実行前に自動でインストールする。
> `python -m pip install playwright` → `python -m playwright install chromium`

---

## Step 4: スクリプトの実行と画像の保存

// turbo

以下の手順で `generate_slides.py` を実行し、スライド画像を自動生成します。

### 4-1. Playwright のインストール確認

```powershell
python -m pip show playwright
```

コマンドが失敗した場合（未インストール）は、以下を順に実行する:

```powershell
python -m pip install playwright
python -m playwright install chromium
```

### 4-2. スクリプトの実行

```powershell
python generate_slides.py
```

`run_command` ツールで上記を実行し、終了を待つ。

### 4-3. 完了確認

実行完了後、出力された画像ファイルの一覧を表示してユーザーに報告する:

```powershell
Get-ChildItem "Outputs\<YYYY-MM-DD-HH>" | Select-Object Name
```

---

## Step 5: 完了レポートの提示

// turbo

以下の内容をまとめてユーザーに報告します。

1. **生成されたスライド枚数** と **保存先のパス**
2. **スライドの一覧**（ファイル名のリスト）
3. 今後の修正・再生成が必要な場合の案内:
   - 「スクリプト（`generate_slides.py`）のCSS/HTMLを編集し、`python generate_slides.py` を再実行するだけで全スライドを再生成できます。」

---

## 動作要件

| 項目 | 内容 |
|---|---|
| **Python** | 3.9 以上 |
| **必要ライブラリ** | `playwright` (`pip install playwright`) |
| **ブラウザ** | Chromium（`playwright install chromium` でインストール） |
| **PDF読み込み** | `pypdf` (`pip install pypdf`) ※PDFを扱う場合のみ |
| **出力形式** | PNG（2560×1440px、16:9） |
| **出力先** | `Outputs/YYYY-MM-DD-HH/` |

## 注意事項

> [!WARNING]
> 画像生成AIによる画像生成（NanoBananaPro等）は日本語テキストの文字化けが発生するため、このワークフローでは使用しない。必ずHTML/CSS + Playwright によるスクリーンショット方式を採用すること。

> [!TIP]
> `.gitignore` に `Outputs/` を追加すると、大容量のスライド画像がGitにコミットされるのを防ぐことができます。
