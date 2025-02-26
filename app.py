import os
import streamlit as st
from groq import Groq

# Get the API key from the environment settings
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ Groq API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

st.set_page_config(page_title="TaxGenie - AI Tax Assistant", page_icon="📊")

st.markdown(
    """
    <style>
        /* Set background gradient */
        .main {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            color: black;
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background: #90caf9;
            color: black;
        }

        /* Chat bubbles styling */
        .stChatMessage.assistant {
            background: #5F8575;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }
        
        .stChatMessage.user {
            background: #FFE5B4;
            color: black;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌟 TaxSimplify")
st.caption(" Your Intelligent Tax Assistant")

# Sidebar with Features
with st.sidebar:
   
    st.markdown("### 🤖 What can I do ?")
    st.markdown("""
    - 💡 **Help in tax filing processes**
    - 💡 **Minimize errors and ensure accuracy**
    - 💡 **Identify deductions and credits**
    - 💡 **Simplify complex calculations**
    """)
    st.divider()
    st.markdown("### 🌟 Something more")
    st.markdown("#### Tax Estimation")
    annual_income = st.number_input("Enter your annual income:", value=50000)
    
    def calculate_tax(income):
        if income <= 1200000:
            return 0
        elif income <= 1500000:
            return (income - 1200000) * 0.10
        elif income <= 2400000:
            return (300000 * 0.10) + (income - 1500000) * 0.20
        else:
            return (300000 * 0.10) + (900000 * 0.20) + (income - 2400000) * 0.30
    
    estimated_tax = calculate_tax(annual_income)
    st.markdown(f"**Estimated tax owed:** ₹{estimated_tax:.2f}")
    
    st.markdown("#### Deductions Checklist")
    deductions = st.multiselect("Select applicable deductions:", ["Medical Expenses", "Education", "Charitable Donations", "Retirement Contributions"])
    
    st.markdown("#### Tax Resources")
    st.markdown("- [Official Website](https://www.incometax.gov.in/iec/foportal/)")
    st.markdown("- [Tax Calendar](https://incometaxindia.gov.in/pages/deadline.aspx)")
    
    st.divider()
    st.markdown("🚀 Built with **Groq | LangChain**")

# Initialize AI Client
client = Groq(api_key=GROQ_API_KEY)

system_prompt_template = "You are an expert AI tax assistant. Provide accurate, concise, and empathetic responses to user queries.  A Tax Assistant that can automate tax filing processes, simplifying complex calculations, identifying deductions, and minimizing errors.Also make sure answers are related to indian tax system as indian users will be using this chatbot."

if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "assistant", "content": "Hi! I'm TaxGenie, your AI Tax Assistant. Would love to be your guide ! "}]

# Display Chat Messages
for message in st.session_state.message_log:
    role_class = "assistant" if message["role"] == "assistant" else "user"
    st.markdown(f'<div class="stChatMessage {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# Input Field for User Queries
user_query = st.chat_input("All your tax related doubts will be resolved here...")

def generate_ai_response(messages):
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    return response

if user_query:
    st.session_state.message_log.append({"role": "user", "content": user_query})
    messages = [{"role": "system", "content": system_prompt_template}] + st.session_state.message_log
    
    with st.spinner("🧠 Processing..."):
        ai_response = generate_ai_response(messages)
    
    st.session_state.message_log.append({"role": "assistant", "content": ai_response})
    st.rerun()
