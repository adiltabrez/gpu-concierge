import streamlit as st

st.title("🔐 Secrets Configuration Test")

# Check if the key exists in st.secrets
if "OPENAI_API_KEY" in st.secrets:
    st.success("Found `OPENAI_API_KEY` in your secrets!")
    
    # We reveal the first few characters just to prove it's the right one
    # without exposing the whole sensitive string.
    raw_key = st.secrets["OPENAI_API_KEY"]
    masked_key = raw_key[:7] + "..." + raw_key[-4:]
    st.info(f"Key preview: `{masked_key}`")
else:
    st.error("Could not find `OPENAI_API_KEY`.")
    st.write("Current keys detected in st.secrets:", list(st.secrets.keys()))
    
    st.markdown("""
    **Troubleshooting Checklist:**
    1. Is your file named exactly `secrets.toml`?
    2. Is it inside a folder named `.streamlit`?
    3. Is the `.streamlit` folder in the same directory where you are running this script?
    """)