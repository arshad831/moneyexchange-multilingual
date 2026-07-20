from typing import Tuple, Dict
import os
import json
import requests
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

# --- GitHub Models config ---
GITHUB_TOKEN = os.environ["GH_TOKEN"]                      # Codespaces secret name: GH_TOKEN
EXCHANGERATE_API_KEY = os.environ["EXCHANGERATE_API_KEY"]  # Codespaces secret name: EXCHANGERATE_API_KEY

endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=GITHUB_TOKEN,
)

# --- LangSmith tracing (optional) ---
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "multilingual-money-changer")


@traceable
def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    response = json.loads(requests.get(url).text)
    return (base, target, amount, f'{response["conversion_result"]:.2f}')


@traceable
def call_llm(textbox_input) -> Dict:
    """Call GitHub Models (gpt-4o-mini) with function/tool calling enabled."""

    tools = [
        {
            "type": "function",
            "function": {
                "name": "exchange_rate_function",
                "description": "Convert a given amount of money from one currency to another. Each currency will be represented as a 3-letter code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "base": {
                            "type": "string",
                            "description": "The base or original currency.",
                        },
                        "target": {
                            "type": "string",
                            "description": "The target or converted currency",
                        },
                        "amount": {
                            "type": "string",
                            "description": "The amount of money to convert from the base currency.",
                        },
                    },
                    "required": ["base", "target", "amount"],
                    "additionalProperties": False,
                },
            },
        }
    ]

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that understands currency conversion requests in any language.",
                },
                {
                    "role": "user",
                    "content": textbox_input,
                },
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name,
            tools=tools,
        )
    except Exception as e:
        st.error(f"LLM call failed: {e}")
        return None

    return response


@traceable
def run_pipeline(user_input):
    """Run the full pipeline: LLM → tool call decision → exchange rate lookup."""

    response = call_llm(user_input)
    if response is None:
        return

    finish_reason = response.choices[0].finish_reason

    if finish_reason == "tool_calls":
        args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        base = args["base"]
        target = args["target"]
        amount = args["amount"]
        _, _, _, result = get_exchange_rate(base, target, amount)
        st.success(f"✅  {base} {amount}  →  {target} {result}")
    elif finish_reason == "stop":
        st.info(f"ℹ️  {response.choices[0].message.content}")
    else:
        st.warning("Unexpected response from model.")


# --- Streamlit UI ---
st.title("🌍 Multilingual Money Changer")
st.caption("Powered by GitHub Models (gpt-4o-mini) + ExchangeRate-API")

user_input = st.text_input("Enter amount and currencies in any language (e.g. 'Convert 100 USD to AED')")

if st.button("Convert"):
    if user_input.strip():
        run_pipeline(user_input)
    else:
        st.warning("Please enter a conversion request.")
