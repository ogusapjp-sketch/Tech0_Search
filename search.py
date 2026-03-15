import re  # re = Regular Expression（正規表現）標準ライブラリ、pip install 不要

#キーワードでページを絞り込む関数
def search_pages(query: str, pages: list) -> list:
    # ① キーワードが空欄ならすぐ終了（空リストを返す）
    if not query.strip():
        return []

    results = []                    # ② 結果を入れる空のリストを用意
    query_lower = query.lower()    # ③ "DX" → "dx" と小文字に統一（大文字小文字を無視するため）

    for page in pages:              # ④ ページを1件ずつ取り出してループ
        # ⑤ title + description + keywords を1つの文字列に結合して検索対象にする
        search_text = " ".join([
            page["title"],
            page["description"],
            " ".join(page["keywords"]),  
        ])

        # ⑥ キーワードが search_text に含まれていたら results に追加
        if query_lower in search_text.lower():
            results.append(page)    # .append() でリストに追加

    return results  # ⑦ マッチしたページのリストを返す
 
# 説明文のキーワードをハイライトにする関数
def highlight_match(text: str, query: str) -> str:
    if not query:       # キーワードが空なら何もしない
        return text

    # re.compile() でパターンを作る
    # re.escape(query) で特殊文字を安全に扱う / re.IGNORECASE で大文字小文字を区別しない
    pattern = re.compile(
        re.escape(query),
        re.IGNORECASE
    )

    # pattern.sub(置換後, 元テキスト) でマッチ部分を置換する
    # 「**DX**」← Markdown で ** で囲むと太字になる
    return pattern.sub(f"**{query}**", text)
