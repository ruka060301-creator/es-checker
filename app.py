import streamlit as st
from main import review

st.title("ES添削ツール")

industry = st.selectbox("志望業界", ["AI・IT", "コンサル", "金融", "メーカー"])
question = st.text_input("設問", "学生時代に力を入れたこと")
answer = st.text_area("回答", height=250)

if st.button("添削する"):
    if not answer.strip():
        st.warning("回答を入力してください")
    else:
        st.info(f"文字数: {len(answer)}字")
        with st.spinner("添削中..."):
            st.markdown(review(question, answer, industry))
