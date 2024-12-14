from langchain_ollama.chat_models import ChatOllama 
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from typing_extensions import TypedDict
from langgraph.graph import START,END, StateGraph
from IPython.display import display,Image
from langchain.pydantic_v1 import BaseModel, Field
#
from prompts import temp_email
from prompts import (promtp_summary_mail, prompt_generate_reply,
                         prompt_result_check, prompt_rewrite_new_email)

llm = ChatOllama(model="cow/gemma2_tools:2b")



class CheckRewrite(BaseModel):
    result : str = Field(description="Only return pass or fail. Dont give explanation ")

### LLMS
llm_summary = (promtp_summary_mail | llm | StrOutputParser())
llm_generate_reply = (prompt_generate_reply | llm | StrOutputParser())
_llm_so = llm.with_structured_output(CheckRewrite)
llm_check = (prompt_result_check| _llm_so )
llm_rewrite_email = (prompt_rewrite_new_email| llm | StrOutputParser())


class AgentState(TypedDict):
    init_msg:str
    summary: str
    generated_reply: str
    result: str

### Agents
class Workflow:
    def read_email_agent(self, state):
        print("--- understant email ---")

        init_msg = state["init_msg"]
        response = llm_summary.invoke(init_msg)
        state["summary"] = response
        return state

    
    def generate_reply_agent(self, state):
        print("--- generate response ---")
        
        init_msg = state["init_msg"]
        response = llm_generate_reply.invoke(init_msg)
        print("Reply::: ", response)
        state["generated_reply"] = response
        return state

    
    def check_email_and_response_agent(self,state):
        print("--- rewrite email ---")
        init_msg = state["init_msg"]
        generated_reply = state["generated_reply"]
        response = llm_check.invoke({"email":init_msg, "email_reply":generated_reply})
        print("check=>>>> ",response)
        state["result"] = response.result

        return state

    def ROUTER_email_rewrite(self,state):
        result = state["result"]

        if str(result) == "pass":
            return "pass"
        else:
            return "fail"   


    def rewrite_email_agent(self,state):
        print("--- rewrite new email ---")
        init_msg = state["init_msg"]
        summary =  state["summary"]

        response = llm_rewrite_email.invoke({"email": init_msg  , 
                                            "summary": summary})

        print("New Email::: ", response)

        state["generated_reply"] = response

        return state

    def send_email_agent(self,state):
        print("--- sending email ---")
        return state


    def compile(self,save_n_show_graph=False):
        ### Nodes
        workflow = StateGraph(AgentState)
        workflow.add_node("read_email genetate summary", self.read_email_agent)
        workflow.add_node("generate_reply",self.generate_reply_agent)
        workflow.add_node("check_email_reply",self.check_email_and_response_agent)
        workflow.add_node("rewrite_new_email",self.rewrite_email_agent )
        workflow.add_node("send_email",self.send_email_agent)

        ###EDGES
        workflow.add_edge(START, "read_email genetate summary")
        workflow.add_edge("read_email genetate summary", "generate_reply")
        workflow.add_edge("generate_reply",  "check_email_reply")
        workflow.add_conditional_edges("check_email_reply",self.ROUTER_email_rewrite, {"pass": "send_email" , "fail":"rewrite_new_email"})
        workflow.add_edge("rewrite_new_email", "check_email_reply")
        workflow.set_finish_point("send_email")
        graph = workflow.compile()

        if save_n_show_graph:
        #    display(Image(graph.get_graph().draw_mermaid_png(output_file_path="GRAPH.png")))
           display(Image(graph.get_graph().draw_mermaid_png()))

        return graph