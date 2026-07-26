import streamlit as st
from main import review, PROMPTS

st.title("ES添削ツール")

industry = st.selectbox("志望業界", ["AI・IT", "コンサル", "金融", "メーカー"])
question = st.text_input("設問", "学生時代に力を入れたこと")
answer = st.text_area("回答", height=250)

limit = st.number_input("字数制限", min_value=100, max_value=2000, value=400, step=50)
count = len(answer)
st.progress(min(count / limit, 1.0))
if count > limit:
    st.error(f"{count}字 / {limit}字（{count - limit}字オーバー）")
elif count > limit * 0.9:
    st.warning(f"{count}字 / {limit}字")
else:
    st.caption(f"{count}字 / {limit}字")

# ここから追加
mode = st.radio("モード", ["通常", "プロンプト比較"], horizontal=True)

if "result" not in st.session_state:
    st.session_state.result = None

if mode == "通常":
    prompt_key = st.selectbox("プロンプト", list(PROMPTS.keys()))

    if st.button("添削する"):
        if not answer.strip():
            st.warning("回答を入力してください")
        else:
            with st.spinner("添削中..."):
                st.session_state.result = review(question, answer, industry, prompt_key)

    tab1, tab2 = st.tabs(["添削結果", "入力内容"])
    with tab1:
        if st.session_state.result:
            st.markdown(st.session_state.result)
        else:
            st.info("上の欄に入力して「添削する」を押してください")
    with tab2:
        st.write(f"業界: {industry} / 設問: {question} / {count}字")
        st.text(answer)

else:
    st.caption("同じESを3つのプロンプトに投げて、出力の違いを見ます（3回API呼び出し）")

    if st.button("3パターンで比較"):
        if not answer.strip():
            st.warning("回答を入力してください")
        else:
            cols = st.columns(3)
            for col, key in zip(cols, PROMPTS.keys()):
                with col:
                    st.subheader(key)
                    with st.spinner("..."):
                        st.markdown(review(question, answer, industry, key))
