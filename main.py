import os
import chainlit as cl
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from dotenv import load_dotenv
load_dotenv()

# Initialize clients for different models
clients = AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

# Model configurations
models = {
    "DeepSeek (Free)": "deepseek/deepseek-r1:free",
    # DeepSeek model ka unique identifier set kar rahe hain

    "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
    # GPT-3.5 Turbo ka model ID

    "Google Gemini": "google/gemini-2.0-flash-exp:free",
    # Claude Instant ka model ID

    "Mistral": "mistralai/devstral-small:free",
    # Mistral 7B ka model ID

    "Microsoft Mai": "microsoft/mai-ds-r1:free"
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

    cl.user_session.set("client", clients)
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

    agent = Agent(
        name="My Agent",
        instructions="you are a helpful assistant",
        model=OpenAIChatCompletionsModel(model=model, openai_client=client),
)

    result = Runner.run_streamed(agent, message.content)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)


    

    await msg.update()
    # Jab complete response aa jaye to message update kar dete hain