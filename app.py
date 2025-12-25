import streamlit as st
import pandas as pd
from openai import OpenAI
from supabase import create_client, Client

# 1. Page Config
st.set_page_config(page_title="GPU Concierge", page_icon="🛡️")

# 2. Setup Clients (Pulls from your .streamlit/secrets.toml)
try:
    # OpenAI Client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Supabase Client
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"⚠️ Configuration missing in secrets.toml! Error: {e}")
    st.stop()

# 3. The "Brain" Logic (Database Primary -> LLM Fallback)
def get_recommendation_data(user_query):
    # STEP A: Try to fetch from your live Supabase database
    try:
        # We fetch all providers to let the AI filter them based on your rules
        response = supabase.table("gpu_providers").select("*").execute()
        
        if response.data and len(response.data) > 0:
            db_df = pd.DataFrame(response.data)
            return db_df.to_string(index=False), "Verified Database"
    except Exception as e:
        # If the database connection fails, we don't crash; we move to fallback
        pass
    
    # STEP B: If DB is empty or fails, we use the LLM Fallback
    return "No database records found. Use your internal knowledge.", "AI Knowledge (Fallback)"

# 4. System Prompt
system_prompt_template = """
You are a Senior Platform Manager & Cybersecurity Advisor.
Your Goal: Recommend a GPU provider based on the user's risk profile.

LOGIC RULES:
1. STUDENT: Recommend cheap options (like Vast.ai) but warn of "High Risk".
2. STARTUP: Recommend balanced options (SOC2 Type 1/2 like RunPod/Lambda).
3. ENTERPRISE: If 'Medical', 'PII', or 'HIPAA' is mentioned, ONLY recommend CoreWeave or AWS.

CONTEXT SOURCE: {source}
AVAILABLE DATA:
{data}
"""

# 5. UI Layout
st.title("🛡️ GPU Concierge")
st.markdown("### The 'Travel Agent' for Secure Cloud Compute")

with st.form("my_form"):
    user_input = st.text_area("Describe your project (e.g., 'Medical startup needs HIPAA compliance'):")
    submitted = st.form_submit_button("Get Recommendation")

# 6. Run the Engine
if submitted and user_input:
    with st.spinner("Consulting Database & Analyzing Risks..."):
        # Get data from Supabase or trigger Fallback logic
        context_data, data_source = get_recommendation_data(user_input)
        
        try:
            # Final AI Analysis
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt_template.format(source=data_source, data=context_data)},
                    {"role": "user", "content": user_input}
                ],
                temperature=0
            )
            
            st.success(f"Analysis Complete (Source: {data_source})")
            st.markdown(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"AI Error: {e}")

# Admin View (Live DB check)
with st.expander("👀 View Internal Database (Supabase)"):
    try:
        res = supabase.table("gpu_providers").select("*").execute()
        st.dataframe(pd.DataFrame(res.data))
    except:
        st.write("Could not connect to Supabase. Check your URL/Key in secrets.")