import streamlit as st
from langchain_ollama import ChatOllama
from datetime import date

# ---------------------------
# LLM setup
# ---------------------------
llm = ChatOllama(
    model="llama-3.2-3b-it:latest",
)

# ---------------------------
# Session state for chat
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------------------------
# Prefilled array of Indian states
# ---------------------------
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi"
]

# ---------------------------
# System prompt for itinerary planner
# ---------------------------
SYSTEM_PROMPT = (
    "You are a professional travel itinerary planner . "
    "Always provide structured itineraries with day-wise plans, activities, hotels, "
    "transportation, and tips for the given destination and dates. "
    "Do not provide unrelated information. "
    "Always follow the user's dates, locations, and preferences."
    " If information is missing, ask clarifying questions."
    "Also check for any travel restrictions or guidelines for the selected places."
    "check the possibility of dates if they are backdated or invalid."
    "Check the locations or inputs provided by users are valid or not."
)

# ---------------------------
# Function to handle user input
# ---------------------------
def handle_input():
    user_input = st.session_state.input_text.strip()
    if user_input:
        from_date = st.session_state.from_date
        to_date = st.session_state.to_date
        places = st.session_state.selected_places

        full_prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"User Query: {user_input}\n"
            f"From Date: {from_date}\n"
            f"To Date: {to_date}\n"
            f"Places: {', '.join(places)}"
        )

        # Append only user text to chat
        st.session_state.messages.append({"role": "user", "content": user_input})

        # LLM response
        response = llm.invoke(full_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.content})

        st.session_state.input_text = ""

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Travel Itinerary Planner", layout="wide")

st.markdown("<h1 style='text-align:center;'>🌏 Travel Itinerary Planner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Enter travel details and get a structured day-wise itinerary.</p>", unsafe_allow_html=True)

# Input section in columns
col1, col2, col3 = st.columns([1,1,2])

with col1:
    from_date = st.date_input("From Date", value=date.today(), key="from_date")
with col2:
    to_date = st.date_input("To Date", value=date.today(), key="to_date")
with col3:
    selected_places = st.multiselect(
        "Select Places / States:",
        options=INDIAN_STATES,
        default=["Delhi"],
        key="selected_places"
    )

st.markdown("---")

# Chat container
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div style='background-color:#DCF8C6; color:#000; padding:10px; border-radius:10px; margin:5px 0; width:fit-content; max-width:70%;'>
                <b>You:</b> {msg['content']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background-color:#F1F0F0; color:#000; padding:10px; border-radius:10px; margin:5px 0; width:fit-content; max-width:70%;'>
                <b>Itinerary Planner:</b> {msg['content']}
                </div>
            """, unsafe_allow_html=True)

# Input box for new message
st.text_input(
    "Describe your travel request or ask a question:",
    key="input_text",
    on_change=handle_input,
    placeholder="Example: Plan a 3-day trip to Delhi and Jaipur with sightseeing and hotels."
)

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
