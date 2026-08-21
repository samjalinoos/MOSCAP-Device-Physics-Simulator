import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
            .stApp {
                background: #0b1020;
                color: #e5e7eb;
            }

            section[data-testid="stSidebar"] {
                background: #111827;
                border-right: 1px solid #1f2937;
            }

            .block-container {
                padding-top: 1.4rem;
                padding-bottom: 1rem;
                max-width: 1450px;
            }

            h1 {
                font-size: 2.45rem !important;
                font-weight: 800 !important;
                letter-spacing: -0.04em;
                margin-bottom: 0.25rem !important;
            }

            h2, h3 {
                letter-spacing: -0.025em;
            }

            div[data-testid="stCaptionContainer"] {
                color: #9ca3af;
                margin-bottom: 0.8rem;
            }

            hr {
                margin-top: 1.1rem !important;
                margin-bottom: 1.1rem !important;
                border-color: #1f2937 !important;
            }

            div[data-testid="stMetric"] {
                background: linear-gradient(180deg, #151b2e 0%, #101827 100%);
                border: 1px solid #263244;
                border-radius: 16px;
                padding: 1rem 1.1rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.18);
            }

            div[data-testid="stMetricLabel"] {
                color: #9ca3af;
                font-size: 0.88rem;
            }

            div[data-testid="stMetricValue"] {
                color: #f9fafb;
                font-size: 1.9rem;
                font-weight: 700;
            }

            div[data-testid="stAlert"] {
                background: #0f2744;
                color: #cfe8ff;
                border: 1px solid #1e5a8a;
                border-radius: 14px;
                padding: 0.8rem 1rem;
            }

            button[data-baseweb="tab"] {
                font-weight: 600;
                color: #9ca3af;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: #60a5fa;
                border-bottom-color: #60a5fa;
            }

            div[data-testid="stVerticalBlock"] {
                gap: 0.75rem;
            }

            .title-card {
                background: radial-gradient(circle at top left, #1e3a8a 0%, #111827 42%, #0b1020 100%);
                border: 1px solid #263244;
                border-radius: 22px;
                padding: 1.4rem 1.6rem;
                margin-bottom: 1rem;
                box-shadow: 0 14px 40px rgba(0,0,0,0.28);
            }

            .section-label {
                font-size: 1.45rem;
                font-weight: 750;
                margin-top: 0.15rem;
                margin-bottom: 0.35rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )