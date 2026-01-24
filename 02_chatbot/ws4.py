from fasthtml.common import *
from hx4_patch.core import *
from claudette import *
import asyncio
import json

# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
hdrs = [tlink, dlink, picolink]

hdrs.extend([*htmx_v4_hdrs, ws_v4])
app = FastHTML(hdrs=hdrs, htmx=False)

# Set up a chat model client and list of messages (https://claudette.answer.ai/)
cli = Client(models[-1])
sp = """You are a helpful and concise assistant."""
messages = []

# Chat message component (renders a chat bubble)
def ChatMessage(msg):
    bubble_class = "chat-bubble-primary" if msg['role']=='user' else 'chat-bubble-secondary'
    chat_class = "chat-end" if msg['role']=='user' else 'chat-start'
    return Div(Div(msg['role'], cls="chat-header"),
               Div(msg['content'], cls=f"chat-bubble {bubble_class}"),
               cls=f"chat {chat_class}")

# The input field for the user message. Also used to clear the
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(type="text", name='msg', id='msg-input',
                 placeholder="Type a message",
                 cls="input input-bordered w-full", hx_swap_oob='true')

def build_ws_msg(element, target="#chatlist", swap="beforeend"):
    # WS message in v4 expects a JSON
    return json.dumps({
        "target": target,
        "swap": swap,
        "payload": to_xml(element)
    })
# The main screen
@app.route("/")
def get():
    page = Body(H1('Chatbot Demo'),
                Div(*[ChatMessage(msg) for msg in messages],
                    id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
                Form(Group(ChatInput(), Button("Send", cls="btn btn-primary",)),
                    hx_ws_connect="/wscon",
                     hx_ws_send=True,
                    cls="flex space-x-2 mt-2",
                ),
                cls="p-4 max-w-lg mx-auto",
                )
    return Title('Chatbot Demo'), page

#TODO: Access msg as param instead of data dict?
@app.ws('/wscon')
async def ws(data: dict, send):
    print("Received data:", data)
    msg = data["values"]["msg"].rstrip()
    # Send the user message to the user (updates the UI right away)
    messages.append({"role":"user", "content":msg})
    msg_e = build_ws_msg(ChatMessage(messages[-1]))
    await send(msg_e)

    # Send the clear input field command to the user
    input_e = build_ws_msg(ChatInput(), target="#msg-input", swap="outerHTML")
    await send(input_e)
    # Simulate a delay
    await asyncio.sleep(1)

    # Get and send the model response
    r = cli(messages, sp=sp)
    messages.append({"role":"assistant", "content":contents(r)})
    msg_e = build_ws_msg(ChatMessage(messages[-1]))
    await send(msg_e)

if __name__ == '__main__': uvicorn.run("ws:app", host='0.0.0.0', port=8000, reload=True)
