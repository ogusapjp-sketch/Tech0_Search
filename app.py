import streamlit as st
import json
from search import search_pages, highlight_match

st.set_page_config(page_title="Tech0 Search v0.1", layout="wide")  # 画面を広く使う

@st.cache_data
def load_pages():
    try:
        with open("pages.json", "r", encoding="utf-8") as f:   
            return json.load(f)
    except FileExistsError:
        return[]

def save_pages(pages):
        with open("pages.json", "w", encoding="utf-8") as f:   
            json.dump(pages, f, ensure_ascii=False, indent=2)

#マスターデータの読み込み
pages = load_pages()


# ページ設定・タイトル
st.title("Tech0 Search v0.1")
st.caption("PROJECT ZERO -新世代テック検索エンジン")
st.divider()

#検索・登録・一覧の３タブをつくる
tab1, tab2, tab3 = st.tabs(["検索", "登録", "一覧"])

# 検索タブ
with tab1:
    query = st.text_input("検索したいキーワードを入力してください")
    if query:
        results = search_pages(query, pages)
        for page in results:
            st.markdown(f"###[{page['title']}]({page['url']})")
            st.markdown(highlight_match(page["description"],query))
            st.divider()
            


with tab2:
    with st.form("register_form"):
        new_title = st.text_input("タイトル")
        new_url = st.text_input("URL")
        new_description = st.text_input("紹介文")
        new_category = st.text_input("カテゴリ")

        # ★【追加】キーワードの入力欄（文字列として受け取る）
        new_keywords_input = st.text_input(
            "キーワード（カンマ区切りで入力。例: DX, AI, 営業）"
        )
        
        submitted = st.form_submit_button("登録")

    if submitted:
        if new_title and new_url:

            # ★【追加】文字列("DX, AI")を、カンマで分割してリスト(["DX", "AI"])に変換する
            # .strip() を使うことで、ユーザーが「DX, AI」と余計なスペースを入れても綺麗に消してくれる
            new_keywords = [
                k.strip() for k in new_keywords_input.split(",") if k.strip()
            ]

            from datetime import date  # もし上部でインポートしていなければ

            today_str = date.today().isoformat()

            new_page = {
                "id": len(pages) + 1,
                "url": new_url,
                "title": new_title,
                "description": new_description,
                "keywords": new_keywords,  # ★ 空リスト [] から変更し、加工したリストを入れる
                "created_at": today_str,  # 「今日」から実際の日付にアップグレード
                "category": new_category,
            }
            pages.append(new_page)
            save_pages(pages)
            st.cache_data.clear()
            st.success("登録が完了しました！")
            st.rerun()
        else:
            st.error("タイトルとURLは必須です。")
        

with tab3:
    for page in pages:
        with st.expander(page["title"]):
            st.write("URL : ", page["url"])
            st.write("紹介文 : ", page["description"])
            st.write("カテゴリ : ", page["category"])