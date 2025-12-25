# 🛡️ GPU Concierge
A Senior Platform Manager & Cybersecurity Advisor tool to find the right GPU cloud.

## 🚀 Setup Instructions
1. **Install Requirements**: `pip install streamlit openai supabase`
2. **Configure Secrets**: Create `.streamlit/secrets.toml` with your OpenAI and Supabase keys.
3. **Database**: Table named `gpu_providers` must exist in Supabase.
4. **Run App**: `streamlit run app.py`

## 🧠 How it Works
- **Primary**: Queries the Supabase database for verified providers.
- **Fallback**: If no data is found, OpenAI GPT-3.5 provides a general recommendation.
- **Logic**: Filters based on Student, Startup, or Enterprise risk profiles.