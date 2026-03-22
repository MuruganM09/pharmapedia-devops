from config import drug_file_path
import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Pharmapedia",
    page_icon="🧾",
    layout="wide"
)
st.title("Pharmapedia an R.A.G Assistant")
def load_drugs():
    file_path = drug_file_path
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return sorted(list(set([line.strip() for line in f if line.strip()])))
    return []

drugs_list = load_drugs()
with st.sidebar:
    st.header("💊 Drug Inventory")
    st.write(f"Total Drugs Available: **{len(drugs_list)}**")
    
    search_query = st.text_input("🔍 Check if drug exists:", placeholder="Type drug name...")
    
    if search_query:
        matches = [d for d in drugs_list if search_query.lower() in d.lower()]
        if matches:
            st.success(f"Found {len(matches)} match(es)!")
        else:
            st.error("Drug not found in database.")
    st.divider()

    st.subheader("All Available Drugs")
    with st.container(height=400):
        for drug in drugs_list:
            st.text(f"• {drug}")

if "message" not in st.session_state:
    st.session_state.message = []

for msg in st.session_state.message:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])

    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

if question := st.chat_input("Ask your question..."):
    st.session_state.message.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                response = requests.post(
                    "http://127.0.0.1:8000/query",
                    json={"question": question}
                )

                if response.status_code == 200:
                    answer = response.json()["answer"]
                else:
                    answer = f"Error: {response.status_code}"

                st.markdown(answer)

        st.session_state.message.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        st.error(f"Connection failed: {e}")