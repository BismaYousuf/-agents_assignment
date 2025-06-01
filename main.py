import os
# OS module ko import kar rahe hain, jo environment variables ko handle karta hai

import chainlit as cl
# Chainlit library import kar rahe hain jisse chat UI banega

from openai import AsyncOpenAI
# OpenAI ka Async client import kar rahe hain jo async calls karta hai

# Load environment variables (create a .env file with your OpenRouter key)
from dotenv import load_dotenv
# dotenv package se load_dotenv function import kar rahe hain .env file load karne ke liye

load_dotenv()
# .env file ko load kar rahe hain jisme apni API keys hoti hain

# Initialize clients for different models
clients = {
    "DeepSeek (Free)": AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    ),
    # DeepSeek model ke liye client bana rahe hain, API key aur base URL set kar ke

    "GPT-3.5 Turbo": AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    ),
    # GPT-3.5 Turbo model ke liye client initialize kar rahe hain

    "Claude Instant": AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    ),
    # Claude Instant model ke liye client bana rahe hain

    "Mistral 7B": AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    ),
    # Mistral 7B model ka client set kar rahe hain

    "Llama 2 13B": AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    # Llama 2 13B model ke liye client initialize kar rahe hain
}

# Model configurations
models = {
    "DeepSeek (Free)": "deepseek/deepseek-r1:free",
    # DeepSeek model ka unique identifier set kar rahe hain

    "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
    # GPT-3.5 Turbo ka model ID

    "Claude Instant": "anthropic/claude-instant-v1",
    # Claude Instant ka model ID

    "Mistral 7B": "mistral/mistral-7b-instruct",
    # Mistral 7B ka model ID

    "Llama 2 13B": "meta-llama/llama-2-13b-chat"
    # Llama 2 13B ka model ID
}

@cl.on_chat_start
async def start_chat():
    # Jab chat start hoti hai to user se model choose karwana hai
    settings = await cl.ChatSettings(
        [
            cl.input_widget.Select(
                id="Model",
                label="Choose AI Model",
                values=list(models.keys()),
                initial_index=0
            )
        ]
    ).send()
    # Chat settings mein dropdown banaya jisme models ke naam hain jahan user select kar sakta hai

    await setup_chat(settings)
    # Jo model user ne select kiya use setup karne ke liye function call kar rahe hain

@cl.on_settings_update
async def setup_chat(settings):
    # Jab bhi user model select kare to ye function chalega
    model_name = settings["Model"]
    # User ke select kiye model ka naam le rahe hain

    cl.user_session.set("model", models[model_name])
    # User session mein us model ka ID save kar rahe hain

    cl.user_session.set("client", clients[model_name])
    # Us model ka client (jo API ke sath baat karega) bhi session mein save kar rahe hain

    await cl.Message(f"Model changed to: {model_name}").send()
    # User ko message bhej rahe hain ke model change ho gaya

@cl.on_message
async def main(message: cl.Message):
    # Jab user chat mein message bheje to ye function chalega

    model = cl.user_session.get("model")
    # Current selected model ID ko user session se le rahe hain

    client = cl.user_session.get("client")
    # Current model ka client bhi session se le rahe hain

    msg = cl.Message(content="")
    await msg.send()
    # Ek empty message bhejte hain jahan streaming response dikhayenge

    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message.content}],
        stream=True
    )
    # OpenRouter API ko call kar ke user ka message bhejte hain aur streaming response le rahe hain

    async for chunk in response:
        if chunk.choices[0].delta.content:
            await msg.stream_token(chunk.choices[0].delta.content)
    # Jo bhi token response mein aata hai usko stream karte hue user ko dikhate hain

    await msg.update()
    # Jab complete response aa jaye to message update kar dete hain
