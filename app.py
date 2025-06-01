import streamlit as st
from sympy import sympify, Symbol, solve
from transformers import pipeline
st.set_page_config(page_title=" Math & Chat Bot", layout="centered")
st.title("Math & Chat Bot")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #800020; /* dark burgundy */
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def load_bot():
    return pipeline("text-generation", model="distilgpt2")

bot = load_bot()

user_input = st.text_area(
    "Enter your question:",
    value="2*x + 3 = 7",
    height=100,
    key="chat_input"
)

def try_sympy(user_input):
    try:
        if "=" in user_input:
            # Try to solve as equation
            lhs, rhs = user_input.split("=")
            x = Symbol('x')
            solution = solve(sympify(lhs) - sympify(rhs), x)
            return f"solution: {solution}"
        else:
            # Try to evaluate as expression
            result = sympify(user_input)
            return f"result: {result}"
    except Exception:
        return None

if st.button("Enter"):
    if user_input.strip():
        # Try SymPy first
        sympy_answer = try_sympy(user_input.strip())
        if sympy_answer:
            st.success(sympy_answer)
        else:
            with st.spinner("AI is thinking..."):
                prompt = user_input.strip()
                response = bot(prompt, max_length=100, do_sample=True, temperature=0.8)
                answer = response[0]['generated_text'].replace(prompt, "").strip()
                st.success(answer)
    else:
        st.warning("Please enter your question.")

st.markdown("---")
st.caption("Built by Tanjim Tanur")
