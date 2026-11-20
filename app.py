import os
import gradio as gr
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def respond(message, history):
    messages = [{"role": "system", "content": "You are a helpful AI assistant with live web search."}]
    for item in history:
        if isinstance(item, dict):
            messages.append({"role": item["role"], "content": str(item["content"])})
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages[-10:],
            tools=[{"type": "browser_search"}],
            tool_choice="auto"
        )
        return response.choices.__getitem__(0).message.content
    except Exception as e:
        return f"Error: {e}"

demo = gr.ChatInterface(
    fn=respond,
    title="My AI Chatbot",
    description="Powered by Groq + Live Web Search"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 10000)))
