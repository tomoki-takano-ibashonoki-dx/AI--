import os
import datetime
import asyncio
from playwright.async_api import async_playwright

slides = [
    {
        "filename": "1_Antigravity学習記録まとめ",
        "html": """
            <div class="slide center-content">
                <div class="sticky-note main-title-note">
                    <h1 class="main-title">Antigravity 学習記録まとめ</h1>
                    <h2 class="sub-title"><span class="highlight">VS Code環境</span>と<span class="highlight">Git/GitHub操作</span>の疑問解消</h2>
                </div>
                <div class="date-tag">2026年4月19日</div>
            </div>
        """
    },
    {
        "filename": "2_目次（アジェンダ）",
        "html": """
            <div class="slide">
                <h1 class="slide-title"><span class="highlight-blue">目次（アジェンダ）</span></h1>
                <div class="content block-note">
                    <p>本日は以下の4つのトピックについて、操作の疑問と解決策を共有します。</p>
                    <ol class="list-styled">
                        <li><span class="highlight">検索窓（コマンドパレット）</span>の場所と使い方</li>
                        <li><span class="highlight">「コミット」と「変更の同期」</span>ボタンの違い</li>
                        <li>GitHubマージ後の<span class="highlight">Git Graphの更新</span>手順</li>
                        <li>ターミナルログの意味と<span class="highlight">不要なローカルブランチの削除</span></li>
                    </ol>
                </div>
            </div>
        """
    },
    {
        "filename": "3_検索窓が見当たらない場合の対処法",
        "html": """
            <div class="slide">
                <h1 class="slide-title"><span class="highlight-blue">1. 検索窓が見当たらない場合の対処法</span></h1>
                <div class="content">
                    <p>Antigravityでは専用UIにより、検索窓が<strong>右上の「<mark>🔍虫眼鏡アイコン</mark>」</strong>にスマートに収納されています。</p>
                    
                    <div class="sticky-note info-note">
                        <h3>⚙️ 以前のように上部に表示させたい場合（任意）:</h3>
                        <ol>
                            <li>設定（<code>Ctrl + ,</code> または左下の歯車）を開く</li>
                            <li><code>title bar style</code> と検索</li>
                            <li><code>Window: Title Bar Style</code> を <code>custom</code> に変更して再起動</li>
                        </ol>
                    </div>

                    <div class="post-it yellow-post-it" style="bottom: 120px; right: 100px; transform: rotate(-2deg);">
                        <h3>💡 プロの裏技</h3>
                        <ul style="list-style-type: none; padding-left: 0;">
                            <li><span class="highlight">Ctrl + Shift + P</span><br>➔ コマンドパレットを開く</li>
                            <li><span class="highlight">Ctrl + P</span><br>➔ ファイル検索</li>
                        </ul>
                    </div>
                </div>
            </div>
        """
    },
    {
        "filename": "4_ソース管理ボタンの表示が変わるからくり",
        "html": """
            <div class="slide">
                <h1 class="slide-title"><span class="highlight-blue">2. ソース管理ボタンの表示が変わるからくり</span></h1>
                <div class="content">
                    <p>ボタンが変わるのは、<strong>「Gitの現在のステータス」</strong>を教えてくれているためです。</p>

                    <div class="flex-container">
                        <div class="box-note red-box">
                            <h3>📍 「コミット」</h3>
                            <p>まだ手元のPCで<span class="highlight">セーブしていない</span>状態</p>
                        </div>
                        <div class="arrow">➔</div>
                        <div class="box-note green-box">
                            <h3>📍 「変更の同期」</h3>
                            <p>手元のセーブ完了！<br>次は<span class="highlight">GitHubへ送信(Push)</span></p>
                        </div>
                    </div>

                    <div class="sticky-note important-note" style="margin-top: 40px;">
                        <h3>✨ おすすめの効率化テクニック</h3>
                        <p>ボタン横の「∨」メニューから<strong>「<mark>コミットして同期</mark>」</strong>を選択！<br>
                        ➔ 手元のセーブとGitHubへの送信が1クリックで全自動で完了します。</p>
                    </div>
                </div>
            </div>
        """
    },
    {
        "filename": "5_ネット上で合流した「枝」を手元に反映させる",
        "html": """
            <div class="slide">
                <h1 class="slide-title"><span class="highlight-blue">3. ネット上で合流した「枝」を手元に反映させる</span></h1>
                <div class="content">
                    <p>GitHub（ネット上）でマージしたのに、手元のGit Graphで合流していない…？<br>
                    ➔ 理由は、手元のPCが合流の事実を<strong><span class="highlight">まだダウンロード(Pull)していないから</span></strong>です。</p>

                    <div class="sticky-note info-note" style="margin-top: 30px;">
                        <h3>🛠 解決の3ステップ:</h3>
                        <ol class="list-styled-large">
                            <li>左下のブランチ名をクリックし、作業場所を <code>main</code> に切り替える</li>
                            <li>「変更の同期」（または同期ボタン）を押して最新状態を<span class="highlight">ダウンロード</span></li>
                            <li>Git Graphを開き直すと、枝が綺麗に合流🌳</li>
                        </ol>
                    </div>
                </div>
            </div>
        """
    },
    {
        "filename": "6_ログの意味と使い終わったブランチの削除",
        "html": """
            <div class="slide">
                <h1 class="slide-title"><span class="highlight-blue">4. ログの意味と使い終わったブランチの削除</span></h1>
                <div class="content">
                    <div class="block-note blue-bg">
                        <p>📺 同期時にターミナルに出る <code>[info] > git ...</code> などの長文ログ<br>
                        ➔ これは裏側の確認作業記録であり、<span class="highlight">エラーではないので無視してOK！</span></p>
                    </div>

                    <div class="sticky-note warning-note" style="margin-top: 40px;">
                        <h3>🧹 手元の作業済みブランチのお片付け手順:</h3>
                        <p>GitHub上で削除しても自分のPCには残ったままになります。混乱を防ぐため手元も消しましょう。</p>
                        <ol class="list-styled">
                            <li><strong><code>main</code> ブランチに切り替える</strong>（※開いているブランチは削除不可）</li>
                            <li>左下からブランチ一覧を開く</li>
                            <li>使い終わったブランチ横の<strong>ゴミ箱アイコン（🗑）</strong>で削除</li>
                        </ol>
                    </div>
                </div>
            </div>
        """
    },
    {
        "filename": "7_まとめ_Next_Action",
        "html": """
            <div class="slide">
                <h1 class="slide-title"><span class="highlight-blue">まとめ ＆ Next Action</span></h1>
                <div class="content block-note">
                    <h3 style="margin-top: 0;">本日の振り返り</h3>
                    <ul class="list-styled-large">
                        <li>検索やコマンド入力は <strong>「🔍」または <span class="highlight">Ctrl + Shift + P</span></strong></li>
                        <li>Git操作は、全自動の <strong>「<span class="highlight">コミットして同期</span>」</strong> が便利</li>
                        <li>枝が合流しない時は、<strong><code>main</code> ブランチに戻って<span class="highlight">同期(Pull)</span></strong></li>
                        <li>長文ログは怖くない！使い終わったブランチは<strong><span class="highlight">手元も削除</span></strong>してスッキリ</li>
                    </ul>
                </div>
                
                <div class="post-it pink-post-it center-post-it" style="transform: rotate(1deg);">
                    便利なショートカットや機能を積極的に使って、<br>快適に開発を進めていきましょう！🚀
                </div>
            </div>
        """
    }
]

CSS = '''
@import url('https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700;900&display=swap');

body {
    margin: 0;
    padding: 0;
    font-family: 'Zen Kaku Gothic New', sans-serif;
    color: #333;
    background-color: #fdfbf7;
}

.slide {
    width: 2560px;
    height: 1440px;
    background-color: #fdfbf7; /* Note paper color */
    background-image: 
        linear-gradient(90deg, transparent 79px, #ff9999 79px, #ff9999 81px, transparent 81px),
        linear-gradient(#e1e1e1 1px, transparent 1px);
    background-size: 100% 55px;
    position: relative;
    padding: 100px 140px 100px 180px;
    box-sizing: border-box;
    overflow: hidden;
}

/* Notebook holes */
.slide::before {
    content: "";
    position: absolute;
    left: 40px;
    top: 50px;
    bottom: 50px;
    width: 25px;
    background-image: radial-gradient(circle at 12px 27.5px, #fff 15px, transparent 16px);
    background-size: 100% 110px;
}

.center-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

h1.slide-title {
    font-size: 72px;
    font-weight: 900;
    margin-bottom: 60px;
    line-height: 1.2;
}

.main-title {
    font-size: 120px;
    font-weight: 900;
    margin: 0 0 30px 0;
    color: #222;
}

.sub-title {
    font-size: 65px;
    font-weight: 700;
    margin: 0;
    color: #444;
}

h3 {
    font-size: 55px;
    margin-bottom: 25px;
    margin-top: 0;
}

p {
    font-size: 48px;
    line-height: 1.7;
    margin-top: 0;
    margin-bottom: 30px;
}

li {
    font-size: 48px;
    line-height: 1.8;
    margin-bottom: 15px;
}

.highlight {
    background: linear-gradient(transparent 60%, #fff200 60%);
    font-weight: bold;
}
.highlight-blue {
    background: linear-gradient(transparent 60%, #80d8ff 60%);
}

mark {
    background-color: transparent;
    background-image: linear-gradient(to right, #ffb6c1 0%, #ffb6c1 100%);
    background-size: 100% 40%;
    background-repeat: no-repeat;
    background-position: 0 85%;
    color: #000;
    font-weight: bold;
    padding: 0 5px;
}

/* Sticky notes */
.sticky-note {
    background-color: #fffac1;
    padding: 50px;
    box-shadow: 5px 15px 30px rgba(0,0,0,0.1);
    position: relative;
    border-radius: 2px 20px 20px 20px;
}
.sticky-note::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 18px;
    background-color: rgba(0,0,0,0.05); /* tape effect */
}

.main-title-note {
    background-color: #fff;
    border: 6px solid #333;
    padding: 80px 100px;
    text-align: center;
    box-shadow: 20px 20px 0px #333;
    border-radius: 10px;
}

.date-tag {
    position: absolute;
    bottom: 100px;
    right: 150px;
    font-size: 45px;
    font-weight: bold;
    background-color: #333;
    color: #fff;
    padding: 15px 40px;
    border-radius: 5px;
    box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
    transform: rotate(-3deg);
}

.block-note {
    background-color: #f4f6f8;
    border-left: 20px solid #6c5ce7;
    padding: 50px 60px;
    margin-bottom: 40px;
    border-radius: 0 15px 15px 0;
}
.block-note.blue-bg {
    border-left: 20px solid #0984e3;
    background-color: #e3f2fd;
}

.info-note {
    background-color: #e8f5e9;
    border-left: 20px solid #4caf50;
}
.warning-note {
    background-color: #fff3e0;
    border-left: 20px solid #ff9800;
}
.important-note {
    background-color: #ffebee;
    border-left: 20px solid #f44336;
}

/* Post-Its */
.post-it {
    position: absolute;
    width: 600px;
    padding: 40px;
    font-size: 45px;
    box-shadow: 2px 10px 20px rgba(0,0,0,0.15);
}
.post-it::after { /* folded corner */
    content: "";
    position: absolute;
    bottom: 0;
    right: 0;
    border-width: 0 0 40px 40px;
    border-style: solid;
    border-color: #ccc #fff #fff #ccc;
    display: block;
    width: 0;
}
.yellow-post-it { background-color: #ffeb3b; }
.pink-post-it { background-color: #ff80ab; color: #fff; }

.center-post-it {
    position: relative;
    margin: 60px auto 0;
    width: 1400px;
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    border-radius: 5px;
}

.flex-container {
    display: flex;
    align-items: center;
    justify-content: space-around;
    margin-bottom: 40px;
    margin-top: 60px;
}

.box-note {
    padding: 50px;
    border-radius: 15px;
    width: 800px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}
.red-box { background-color: #ffebee; border: 4px dashed #f44336; }
.green-box { background-color: #e8f5e9; border: 4px dashed #4caf50; }

.arrow {
    font-size: 150px;
    color: #555;
}

.list-styled {
    margin-top: 20px;
}
.list-styled li {
    padding-left: 10px;
}
.list-styled-large li {
    font-size: 50px;
    margin-bottom: 30px;
}

code {
    background-color: #e0e0e0;
    padding: 5px 15px;
    border-radius: 8px;
    font-family: inherit;
    font-weight: bold;
    color: #e83e8c;
}
'''

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <style>
        {css}
    </style>
</head>
<body>
    {content}
</body>
</html>
"""

async def generate():
    now = datetime.datetime.now()
    dir_name = f"{now.strftime('%Y-%m-%d-%S')}"
    # The user asked for YYYY-MM-DD-SS format. So let's respect that.
    output_dir = os.path.join(r"C:\Users\user\Desktop\AI--\Outputs", dir_name)
    os.makedirs(output_dir, exist_ok=True)
    
    html_path = os.path.join(r"C:\Users\user\Desktop\AI--", "temp_slides.html")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 2560, 'height': 1440})
        
        for slide in slides:
            # Build full HTML
            full_html = HTML_TEMPLATE.format(css=CSS, content=slide["html"])
            
            # Write to temp file
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(full_html)
                
            # Render and screenshot
            await page.goto(f"file:///{html_path.replace(os.sep, '/')}")
            
            # Wait for webfonts to load
            try:
                await page.evaluate('document.fonts.ready')
                await asyncio.sleep(0.5) # Wait a bit for font rendering
            except:
                pass
            
            out_file = os.path.join(output_dir, f"{slide['filename']}.png")
            await page.screenshot(path=out_file, type="png")
            
        await browser.close()
        
    if os.path.exists(html_path):
        os.remove(html_path)

    print(f"Screenshots successfully saved to: {output_dir}")

if __name__ == '__main__':
    asyncio.run(generate())
