import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_ai(prompt):
    """Надсилає запит до OpenAI та повертає відповідь."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ти кулінарний помічник, який генерує рецепти. Завжди додавай орієнтовний час приготування (наприклад, Час: 45 хв ; у такому форматі), інгредієнти списком, інструкції з приготування."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
