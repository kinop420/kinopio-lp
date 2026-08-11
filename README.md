# キノピオAI🍄 紹介LP

AI音楽×AI動画クリエイター「キノピオAI」の紹介ランディングページ。
外部フレームワーク不使用・単一HTML。スマホ縦スクロール特化（Instagramプロフィールリンクからの流入想定）。

## 構成

```
kinopio-lp/
├── index.html      … LP本体（CSS/JSすべて内包）
├── assets/
│   ├── logo.svg    … 仮ロゴ（差し替え前提）
│   └── fv.svg      … 仮キービジュアル（差し替え前提）
└── README.md
```

## 画像の差し替え方

| 差し替えたいもの | 手順 |
| --- | --- |
| ロゴ | `assets/logo.svg` を同名で上書き。別形式なら `index.html` 内の `assets/logo.svg` を全置換（5箇所） |
| キービジュアル | `assets/fv.jpg` などを置き、`index.html` の CSS 変数 `--fv-image` の1行を書き換え |
| IG / TikTok のサムネ | 各カードの `.work__thumb` 内を `<img src="assets/work-ig.jpg" alt="…">` に置き換え |
| OGP画像 | `assets/ogp.jpg` を置き、`<meta property="og:image">` を書き換え |

## 数字の更新

`index.html` の `<!-- 実績数字 -->` コメント直下の `.stats` ブロックと、
SNSセクションの `.sns__handle` 内の数値を書き換えてください。基準日は `.stats__note` に記載。

## ローカル確認

`index.html` をブラウザで開くだけ。ビルド不要。
