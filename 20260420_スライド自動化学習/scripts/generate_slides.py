import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import datetime
import asyncio
from playwright.async_api import async_playwright

# ============================================================
# スライドデータ定義
# ============================================================
slides = [
    {
        "filename": "01_タイトル",
        "html": """
        <div class="slide slide-title">
            <div class="title-badge">📅 2026 / 04 / 17</div>
            <h1 class="main-title">Antigravity<br><span class="accent">学習記録</span></h1>
            <p class="subtitle">AIエージェントと歩んだ最初の一日</p>
            <div class="postit postit-yellow" style="right:120px; bottom:160px; transform:rotate(3deg)">
                使用ツール：<br><strong>Antigravity</strong><br>（VSCode系 AI エディタ）
            </div>
            <div class="postit postit-green" style="right:320px; bottom:100px; transform:rotate(-2deg)">
                WOOP 計画<br><strong>第1週 達成！</strong>🎉
            </div>
            <div class="hole"></div>
        </div>
        """
    },
    {
        "filename": "02_目次",
        "html": """
        <div class="slide">
            <div class="hole"></div>
            <h2 class="slide-heading">📋 目次 / アジェンダ</h2>
            <div class="agenda-grid">
                <div class="agenda-item">
                    <span class="agenda-num">1</span>
                    <span class="agenda-text">Antigravityの初期設定</span>
                </div>
                <div class="agenda-item">
                    <span class="agenda-num">2</span>
                    <span class="agenda-text">セキュリティ対策の実施</span>
                </div>
                <div class="agenda-item">
                    <span class="agenda-num">3</span>
                    <span class="agenda-text">AIエージェントへの初指示体験</span>
                </div>
                <div class="agenda-item">
                    <span class="agenda-num">4</span>
                    <span class="agenda-text">ローカルPDF読み込み（ミニNotebookLM化）</span>
                </div>
                <div class="agenda-item">
                    <span class="agenda-num">5</span>
                    <span class="agenda-text">Pythonでパワポを自動生成！</span>
                </div>
                <div class="agenda-item">
                    <span class="agenda-num">6</span>
                    <span class="agenda-text">自動マニュアル生成への4つの階段</span>
                </div>
                <div class="agenda-item">
                    <span class="agenda-num">7</span>
                    <span class="agenda-text">まとめ・Next Action</span>
                </div>
            </div>
        </div>
        """
    },
    {
        "filename": "03_初期設定",
        "html": """
        <div class="slide">
            <div class="hole"></div>
            <div class="slide-num-badge">1 / 6</div>
            <h2 class="slide-heading">🎨 Antigravityの初期設定</h2>
            <div class="content-cols">
                <div class="col-main">
                    <ul class="bullet-list">
                        <li>
                            <strong>テーマ選択：</strong>
                            <span class="hl">Solarized Dark</span>（青緑）
                            <span class="sub-note">→ 長時間でも目が疲れにくい</span>
                        </li>
                        <li>
                            <strong>AIモード：</strong>
                            <code>Review-driven development</code>（レビュー重視）
                            <ul class="sub-list">
                                <li>AIが何かするたびに「これでいいですか？」と確認</li>
                                <li>勝手に進む不安がゼロ → 主導権は常に人間に</li>
                            </ul>
                        </li>
                        <li>
                            <strong>日本語化：</strong>
                            <code>Japanese Language Pack</code> をインストール
                            <span class="sub-note">→ 英語の迷いを解消</span>
                        </li>
                    </ul>
                </div>
                <div class="col-side">
                    <div class="postit postit-pink" style="transform:rotate(-3deg)">
                        💡 迷いや疲労を防ぐ<br>ために最初に設定を<br>整えることが大切！
                    </div>
                </div>
            </div>
            <div class="info-block block-blue">
                <strong>📌 ポイント：</strong>「レビュー重視モード」は WOOP の内的障害「迷い・不安」を防ぐための最初の防衛策
            </div>
        </div>
        """
    },
    {
        "filename": "04_セキュリティ",
        "html": """
        <div class="slide">
            <div class="hole"></div>
            <div class="slide-num-badge">2 / 6</div>
            <h2 class="slide-heading">🛡 セキュリティ対策の実施</h2>
            <div class="content-cols">
                <div class="col-main">
                    <ul class="bullet-list">
                        <li>
                            <strong>Enable Telemetry をオフ</strong>
                            <ul class="sub-list">
                                <li>GoogleへのデータBS送信を停止</li>
                                <li>二重のロックを完成させた</li>
                            </ul>
                        </li>
                        <li>
                            <strong>Google Workspace 契約の安心材料</strong>
                            <ul class="sub-list">
                                <li>入力データがAIの学習に<span class="hl">使われない</span>強固な保護が標準適用</li>
                            </ul>
                        </li>
                        <li>
                            <strong>開発ルール（最大の防御策）</strong>
                            <ul class="sub-list">
                                <li>本物の個人情報を開発環境に持ち込まない</li>
                                <li>ダミーデータ（架空のITリーダーのメモ）で安全に実験</li>
                            </ul>
                        </li>
                    </ul>
                </div>
                <div class="col-side">
                    <div class="postit postit-yellow" style="transform:rotate(2deg)">
                        🔒 テレメトリOFF<br>+ Workspace 契約<br>= 二重ロック完成
                    </div>
                </div>
            </div>
            <div class="info-block block-red">
                <strong>⚠ 鉄則：</strong>開発中は本物のデータを使わない。まずはダミーデータで仕組みを作る。
            </div>
        </div>
        """
    },
    {
        "filename": "05_初指示体験",
        "html": """
        <div class="slide">
            <div class="hole"></div>
            <div class="slide-num-badge">3 / 6</div>
            <h2 class="slide-heading">🤖 AIエージェントへの初指示体験</h2>
            <div class="flow-row">
                <div class="flow-box">
                    <div class="flow-icon">📝</div>
                    <div class="flow-label">入力</div>
                    <div class="flow-desc">架空のITリーダーの<br><strong>雑多なメモ</strong></div>
                </div>
                <div class="flow-arrow">→</div>
                <div class="flow-box">
                    <div class="flow-icon">🤖</div>
                    <div class="flow-label">Agent が処理</div>
                    <div class="flow-desc">手順を抽出・整理<br>Markdownで構造化</div>
                </div>
                <div class="flow-arrow">→</div>
                <div class="flow-box">
                    <div class="flow-icon">📄</div>
                    <div class="flow-label">出力</div>
                    <div class="flow-desc">新人向け<br><strong>手順書(.md)</strong><br>自動生成！</div>
                </div>
            </div>
            <ul class="bullet-list" style="margin-top: 32px">
                <li>Agent は「Accept（承認）」を求めてから保存 → <span class="hl">主導権は常に人間に</span></li>
                <li>緑色の提案 → 人間が確認 → Accept → ファイル完成、のフローが確立</li>
            </ul>
            <div class="info-block block-green">
                <strong>🎯 これがWOOPの成果：</strong>「裏でAIが働き、マニュアルが自動生成される仕組み」の第一歩！
            </div>
        </div>
        """
    },
    {
        "filename": "06_ミニNotebookLM",
        "html": """
        <div class="slide">
            <div class="hole"></div>
            <div class="slide-num-badge">4 / 6</div>
            <h2 class="slide-heading">📚 ローカルPDF読み込み（ミニNotebookLM化）</h2>
            <div class="content-cols">
                <div class="col-main">
                    <ul class="bullet-list">
                        <li>
                            <strong>87ページのPDF</strong>をAntigravityで直接読み込みに成功
                        </li>
                        <li>
                            AIがPDF内から<span class="hl">「ステップ0〜4のロードマップ」</span>を正確に抽出・整理
                        </li>
                        <li>
                            <strong>個人情報を外部クラウドに出さず</strong>、自分のPC内だけで完結
                        </li>
                    </ul>
                    <div class="compare-table">
                        <div class="compare-row header">
                            <div>NotebookLM</div>
                            <div>Antigravity（今回）</div>
                        </div>
                        <div class="compare-row">
                            <div>クラウド上で処理</div>
                            <div>ローカルPC内で処理 ✅</div>
                        </div>
                        <div class="compare-row">
                            <div>外部APIへデータ送信</div>
                            <div>データ外部流出なし ✅</div>
                        </div>
                        <div class="compare-row">
                            <div>操作はブラウザ上</div>
                            <div>Agentに自然言語で指示 ✅</div>
                        </div>
                    </div>
                </div>
                <div class="col-side">
                    <div class="postit postit-green" style="transform:rotate(-2deg)">
                        💡 これが<br>「自分専用<br>ミニNotebookLM」<br>の原型！
                    </div>
                </div>
            </div>
        </div>
        """
    },
    {
        "filename": "07_Python自動生成",
        "html": """
        <div class="slide">
            <div class="hole"></div>
            <div class="slide-num-badge">5 / 6</div>
            <h2 class="slide-heading">🐍 Pythonでパワポを自動生成！</h2>
            <div class="flow-row flow-row-vertical">
                <div class="flow-box-h">
                    <div class="flow-icon">💬</div>
                    <div class="flow-desc">チャットのテキスト（スライド構成案）</div>
                </div>
                <div class="flow-arrow-v">↓ Agentがコードを生成</div>
                <div class="flow-box-h code-box">
                    <div class="flow-icon">🐍</div>
                    <div class="flow-desc"><code>python-pptx</code> ライブラリを使ったPythonスクリプト</div>
                </div>
                <div class="flow-arrow-v">↓ Agentがインストール＆実行まで代行</div>
                <div class="flow-box-h result-box">
                    <div class="flow-icon">📊</div>
                    <div class="flow-desc"><strong>.pptxファイル</strong>が自動生成！（全6枚）</div>
                </div>
            </div>
            <div class="info-block block-green" style="margin-top: 28px">
                <strong>💡 AIが「ライター」から「エンジニア」として動いた瞬間！</strong><br>
                コードの意味：<code>slide_data</code>（データ定義） → <code>for</code>ループ（反復処理） → <code>prs.save()</code>（ファイル保存）
            </div>
        </div>
        """
    },
    {
        "filename": "08_まとめ",
        "html": """
        <div class="slide">
            <div class="hole"></div>
            <h2 class="slide-heading">🏁 まとめ・Next Action</h2>
            <div class="summary-grid">
                <div class="summary-col">
                    <h3 class="summary-title">✅ 本日の達成事項</h3>
                    <ul class="bullet-list">
                        <li>初期設定・セキュリティ・手順書生成</li>
                        <li>PDF読み込み（ミニNotebookLM化）</li>
                        <li>Pythonでパワポ自動化</li>
                        <li><span class="hl">「AIに指示を出す人」から<br>「AIでシステムを構築する人」へ</span></li>
                    </ul>
                </div>
                <div class="summary-col">
                    <h3 class="summary-title">🪜 4つの階段（ロードマップ）</h3>
                    <ul class="road-list">
                        <li class="done">✅ 第1形態：Python で「文字」を出力</li>
                        <li class="next">▶ 第2形態：デザインテンプレート活用</li>
                        <li>　第3形態：PythonにAI頭脳（API）を接続</li>
                        <li>　第4形態：複数データから自動マニュアル生成・製品化</li>
                    </ul>
                </div>
            </div>
            <div class="postit postit-yellow" style="position:absolute; right:80px; bottom:80px; transform:rotate(2deg)">
                🎯 Next Action：<br>第2形態に挑戦！<br>実戦＋疑問解消<br>スタイルで進める
            </div>
        </div>
        """
    },
]

# ============================================================
# CSS（大学ノート風デザイン）
# ============================================================
CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    width: 2560px;
    height: 1440px;
    overflow: hidden;
    font-family: 'Zen Kaku Gothic New', 'Noto Sans JP', sans-serif;
    background: #f5f0e8;
}

.slide {
    width: 2560px;
    height: 1440px;
    position: relative;
    overflow: hidden;
    /* 大学ノート風の罫線 */
    background-color: #fdfaf3;
    background-image:
        linear-gradient(transparent 79px, #c5d8f0 79px, #c5d8f0 80px, transparent 80px),
        linear-gradient(90deg, transparent 119px, #f9c0c0 119px, #f9c0c0 120px, transparent 120px);
    background-size: 100% 80px, 100% 100%;
    padding: 80px 160px 80px 180px;
}

/* バインダーの穴 */
.hole {
    position: absolute;
    left: 52px;
    top: 50%;
    transform: translateY(-50%);
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #e8dfd0;
    border: 3px solid #c9bfa8;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
}

/* スライド番号バッジ */
.slide-num-badge {
    position: absolute;
    top: 52px;
    right: 80px;
    background: #4a90d9;
    color: white;
    font-size: 28px;
    font-weight: 700;
    padding: 8px 28px;
    border-radius: 30px;
    letter-spacing: 1px;
}

/* ============================================================
   タイトルスライド
   ============================================================ */
.slide-title {
    background-color: #1a2a4a;
    background-image:
        linear-gradient(transparent 79px, rgba(255,255,255,0.06) 79px, rgba(255,255,255,0.06) 80px, transparent 80px),
        linear-gradient(90deg, transparent 119px, rgba(255,100,100,0.15) 119px, rgba(255,100,100,0.15) 120px, transparent 120px);
    background-size: 100% 80px, 100% 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
}

.title-badge {
    background: rgba(255,255,255,0.15);
    border: 2px solid rgba(255,255,255,0.3);
    color: #a0c8f8;
    font-size: 38px;
    font-weight: 600;
    padding: 12px 40px;
    border-radius: 40px;
    margin-bottom: 40px;
    letter-spacing: 3px;
}

.main-title {
    font-size: 130px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 40px;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.main-title .accent {
    color: #4adbb5;
    background: linear-gradient(135deg, #4adbb5, #60a3f8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subtitle {
    font-size: 50px;
    color: #a0b8d8;
    font-weight: 400;
    letter-spacing: 2px;
}

.slide-title .hole {
    background: rgba(255,255,255,0.1);
    border-color: rgba(255,255,255,0.2);
}

/* ============================================================
   見出し
   ============================================================ */
.slide-heading {
    font-size: 68px;
    font-weight: 900;
    color: #1a2a4a;
    margin-bottom: 48px;
    padding-bottom: 20px;
    border-bottom: 5px solid #4a90d9;
    line-height: 1.2;
}

/* ============================================================
   目次スライド
   ============================================================ */
.agenda-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px 64px;
}

.agenda-item {
    display: flex;
    align-items: center;
    gap: 24px;
    background: rgba(74, 144, 217, 0.06);
    border: 2px solid rgba(74, 144, 217, 0.2);
    border-radius: 16px;
    padding: 20px 32px;
    transition: all 0.2s;
}

.agenda-num {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4a90d9, #2c5f9e);
    color: white;
    font-size: 32px;
    font-weight: 900;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(74,144,217,0.4);
}

.agenda-text {
    font-size: 38px;
    font-weight: 600;
    color: #1a2a4a;
    line-height: 1.3;
}

/* ============================================================
   本文・レイアウト
   ============================================================ */
.content-cols {
    display: flex;
    gap: 60px;
    align-items: flex-start;
}

.col-main { flex: 1; }
.col-side { width: 280px; flex-shrink: 0; }

.bullet-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 28px;
}

.bullet-list > li {
    font-size: 36px;
    color: #1a2a4a;
    line-height: 1.6;
    padding-left: 36px;
    position: relative;
}

.bullet-list > li::before {
    content: "▶";
    position: absolute;
    left: 0;
    color: #4a90d9;
    font-size: 28px;
    top: 6px;
}

.sub-list {
    list-style: none;
    margin-top: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.sub-list li {
    font-size: 30px;
    color: #3a5272;
    padding-left: 28px;
    position: relative;
}

.sub-list li::before {
    content: "・";
    position: absolute;
    left: 0;
    color: #4a90d9;
}

.sub-note {
    font-size: 28px;
    color: #6a8ab0;
    margin-left: 12px;
}

/* ============================================================
   ハイライト・コード
   ============================================================ */
.hl {
    background: linear-gradient(transparent 60%, #fff200 60%);
    padding: 0 4px;
    font-weight: 700;
}

code {
    background: #e8f0f8;
    border: 1.5px solid #b0cce8;
    border-radius: 8px;
    padding: 4px 14px;
    font-family: 'Courier New', monospace;
    font-size: 30px;
    color: #1a4a7a;
}

/* ============================================================
   情報ブロック
   ============================================================ */
.info-block {
    margin-top: 36px;
    padding: 24px 36px;
    border-radius: 12px;
    font-size: 34px;
    line-height: 1.5;
    border-left: 10px solid;
}

.block-green {
    background: #edfaf4;
    border-color: #2ecc71;
    color: #1a5c3a;
}

.block-blue {
    background: #edf4fa;
    border-color: #3498db;
    color: #1a3a5c;
}

.block-red {
    background: #faedf0;
    border-color: #e74c3c;
    color: #5c1a1a;
}

/* ============================================================
   付箋（Post-it）
   ============================================================ */
.postit {
    width: 260px;
    padding: 24px 20px;
    font-size: 28px;
    line-height: 1.6;
    border-radius: 4px;
    box-shadow: 4px 6px 16px rgba(0,0,0,0.15);
    font-weight: 500;
    text-align: center;
}

.postit-yellow {
    background: #fffac1;
    color: #3a3000;
}

.postit-pink {
    background: #ffc8d8;
    color: #3a0010;
}

.postit-green {
    background: #c8f0d8;
    color: #003a18;
}

/* タイトルスライド内の付箋は absolute 配置 */
.slide-title .postit {
    position: absolute;
}

/* ============================================================
   フロー図（横）
   ============================================================ */
.flow-row {
    display: flex;
    align-items: center;
    gap: 32px;
    margin: 40px 0;
}

.flow-box {
    flex: 1;
    background: #f0f6ff;
    border: 3px solid #4a90d9;
    border-radius: 20px;
    padding: 32px 24px;
    text-align: center;
}

.flow-icon { font-size: 60px; margin-bottom: 12px; }
.flow-label {
    font-size: 28px;
    font-weight: 700;
    color: #4a90d9;
    margin-bottom: 8px;
}
.flow-desc {
    font-size: 30px;
    color: #1a2a4a;
    line-height: 1.4;
}

.flow-arrow {
    font-size: 60px;
    color: #4a90d9;
    flex-shrink: 0;
    font-weight: 900;
}

/* フロー図（縦） */
.flow-row-vertical {
    flex-direction: column;
    gap: 0;
}

.flow-box-h {
    width: 100%;
    background: #f0f6ff;
    border: 3px solid #4a90d9;
    border-radius: 20px;
    padding: 24px 40px;
    display: flex;
    align-items: center;
    gap: 24px;
}

.flow-box-h .flow-icon { font-size: 48px; flex-shrink: 0; }
.flow-box-h .flow-desc { font-size: 34px; color: #1a2a4a; }

.code-box { background: #eef4ff; border-color: #7aabeb; }
.result-box { background: #edfaf4; border-color: #2ecc71; }

.flow-arrow-v {
    font-size: 32px;
    color: #4a90d9;
    font-weight: 700;
    text-align: center;
    padding: 12px;
    width: 100%;
}

/* ============================================================
   比較テーブル
   ============================================================ */
.compare-table {
    margin-top: 32px;
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid #b0cce8;
    font-size: 30px;
}

.compare-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
}

.compare-row div {
    padding: 16px 24px;
    border-right: 1px solid #b0cce8;
    border-bottom: 1px solid #b0cce8;
    color: #1a2a4a;
}

.compare-row.header div {
    background: #1a2a4a;
    color: white;
    font-weight: 700;
    text-align: center;
}

.compare-row:not(.header):nth-child(even) div {
    background: #f0f6ff;
}

/* ============================================================
   まとめスライド
   ============================================================ */
.summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
}

.summary-title {
    font-size: 42px;
    font-weight: 800;
    color: #1a2a4a;
    margin-bottom: 28px;
    padding-bottom: 12px;
    border-bottom: 3px solid #4a90d9;
}

.road-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.road-list li {
    font-size: 32px;
    color: #3a5272;
    padding: 16px 24px;
    border-radius: 10px;
    background: rgba(74, 144, 217, 0.05);
    border: 1.5px solid rgba(74, 144, 217, 0.15);
    line-height: 1.4;
}

.road-list li.done {
    background: #edfaf4;
    border-color: #2ecc71;
    color: #1a4a2a;
    font-weight: 700;
}

.road-list li.next {
    background: #fff8e1;
    border-color: #f0c040;
    color: #3a2a00;
    font-weight: 700;
}
"""

# ============================================================
# HTML テンプレート
# ============================================================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
{content}
</body>
</html>
"""

# ============================================================
# メイン処理
# ============================================================
async def generate():
    now = datetime.datetime.now()
    dir_name = now.strftime('%Y-%m-%d-%H')
    output_dir = os.path.join("Outputs", dir_name)
    os.makedirs(output_dir, exist_ok=True)

    print(f"[OUT] 出力先: {output_dir}")
    print(f"[INFO] 生成枚数: {len(slides)} 枚")
    print()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 2560, 'height': 1440})

        for i, slide in enumerate(slides, 1):
            html_path = os.path.abspath("temp_slide.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(HTML_TEMPLATE.format(css=CSS, content=slide["html"]))

            await page.goto(f"file:///{html_path.replace(os.sep, '/')}")
            await page.evaluate('document.fonts.ready')
            await asyncio.sleep(0.6)

            out_path = os.path.join(output_dir, f"{slide['filename']}.png")
            await page.screenshot(path=out_path, type="png")
            print(f"  [OK] [{i:02d}/{len(slides):02d}] {slide['filename']}.png")

        await browser.close()

    if os.path.exists("temp_slide.html"):
        os.remove("temp_slide.html")

    print()
    print(f"[DONE] 全スライド生成完了!")
    print(f"[PATH] 保存先: {os.path.abspath(output_dir)}")

if __name__ == '__main__':
    asyncio.run(generate())
