import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_ai_response(message: str) -> str:

    # 1️⃣ Try OpenAI (Responses API)
    try:
        response = openai_client.responses.create(
            model="gpt-4.1-mini",
            input=message
        )
        return response.output_text

    except Exception as openai_error:
        print("⚠️ OpenAI failed:", openai_error)

        # 2️⃣ Fallback to Groq (Chat Completions API)
        try:
            response = groq_client.chat.completions.create(
                model="moonshotai/kimi-k2-instruct-0905",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content

        except Exception as groq_error:
            print("❌ Groq failed:", groq_error)
            return "❌ AI service temporarily unavailable"