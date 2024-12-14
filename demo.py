import gradio as gr
from Agents import Workflow

wokflow = Workflow()
graph = wokflow.compile()

def chat(email):
    result = graph.invoke({"init_msg":email})
    return result["generated_reply"]


UI = gr.Interface(fn=chat, inputs="textbox", outputs="textbox")

UI.launch()