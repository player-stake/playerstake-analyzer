import streamlit as st
import fitz  # PyMuPDF
import openai

st.set_page_config(page_title="PlayerStake NIL Contract Analyzer", layout="wide")
st.title("📄 PlayerStake NIL Contract Analyzer – Beta")
st.write("Upload your NIL contract and we'll provide AI-generated insights: red flags, market value, deal rating, and revision suggestions.")

# API Key
openai.api_key = st.secrets["openai_key"]

# File uploader
uploaded_file = st.file_uploader("Upload NIL Contract (PDF)", type=["pdf"])
contract_text = ""

if uploaded_file:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            contract_text += page.get_text()

    st.text_area("📄 Extracted Contract Text", contract_text, height=300)

insta_handle = st.text_input("Instagram Handle")
sport = st.selectbox("Sport", ["Football", "Basketball", "Track", "Volleyball", "Other"])
deal_value = st.text_input("Deal Value ($)")
duration = st.text_input("Contract Duration")

def analyze_contract(text):
    prompt = f"""
You are an NIL contract analysis assistant. Review the following contract and provide:
1. 🚩 Red Flags (usage rights, term length, exclusivity, deliverables)
2. 💵 Fair Market Value (estimate based on deal value, social handle, sport)
3. ⭐ Deal Rating (from 1–5 stars)
4. ✍️ Suggested Revisions (rewrite key clauses)

Contract Text:
{text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if st.button("🔍 Analyze My Contract") and contract_text:
    with st.spinner("Analyzing with AI..."):
        result = analyze_contract(contract_text)
        st.success("Analysis Complete ✅")
        st.markdown(result)
