import streamlit as st
import pandas as pd
from openai import OpenAI

# 1. Page Config
st.set_page_config(page_title="GPU Concierge", page_icon="🛡️")

# 2. Setup OpenAI Client (Connects to your secrets.toml)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ OpenAI API Key missing! Check .streamlit/secrets.toml")
    st.stop()

# 3. Load Data
def load_data():
    try:
        return pd.read_csv("gpu_providers.csv")
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# Convert the Dataframe to a text string so the AI can read it
data_as_text = df.to_string(index=False)

# 4. THE SYSTEM PROMPT (The "Brain" Logic)
system_prompt = f"""
You are a Senior Platform Manager & Cybersecurity Advisor.
Your Goal: Recommend GPU providers from the list below based on the user's risk profile.

THE DATA (Providers Available):
{data_as_text}

LOGIC RULES:
1. STUDENT/HOBBYIST: If the user cares only about price, recommend Cheap providers (Vast.ai) but WARN them about "High Risk" and "Unverified Hosts".
2. STARTUP: If the user needs balance, recommend SOC2 Type 1/2 providers (RunPod, Lambda).
3. ENTERPRISE: If the user mentions "Medical", "PII", "HIPAA", or "Corporate", ONLY recommend CoreWeave or AWS. Warn about high cost.

OUTPUT FORMAT:
- Start with a clear "Recommendation: [Provider Name]"
- Provide a brief "Security Risk Assessment" (Why is it safe/unsafe?)
- End with a Markdown Table comparing the recommended options.
"""

# 5. UI Layout
st.title("🛡️ GPU Concierge")
st.markdown("### The 'Travel Agent' for Secure Cloud Compute")

with st.form("my_form"):
    user_input = st.text_area("Describe your project (e.g., 'Student looking for cheap GPU' or 'Medical startup needs HIPAA compliance'):")
    submitted = st.form_submit_button("Get Recommendation")

# 6. Run the AI
if submitted and user_input:
    with st.spinner("Analyzing Security & Compliance risks..."):
        try:
            # Send to OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # We use 3.5 to keep costs low
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0
            )
            # Display Result
            st.success("Analysis Complete")
            st.markdown(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Admin View
with st.expander("👀 View Internal Database"):
    st.dataframe(df)