# Multi-Model Chatbot with Chainlit and OpenRouter

This project creates a chatbot that gets responses from 5 different AI models and interacts with users using Chainlit.

## Features

- Allows user to choose an AI model.
- Gets responses from multiple AI models.
- Shows streaming responses in real-time chat.
- Uses OpenRouter API.

## Requirements

- Python 3.8 or higher.
- OpenRouter API key (set `OPEN_ROUTER_API_KEY` in a `.env` file).

## Setup

1. Clone or download the project.
2. Create a `.env` file and add your OpenRouter API key:
OPEN_ROUTER_API_KEY=your_api_key_here
3. Install required packages:
pip install chainlit openai python-dotenv agents
4. Run the Chainlit app:
chainlit run main.py
## Usage

- Start the chat.
- Select the AI model from the dropdown.
- Type your message and get responses from AI.

## Notes

- Make sure your API key is set correctly to avoid 401 Unauthorized errors.
- Responses will stream in real-time.

---

**Happy Chatting!**

