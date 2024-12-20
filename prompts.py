from langchain_core.prompts import PromptTemplate


#### Templates
_template_summary = """
You are a helpfull bot. Your task to understand the given mail return Summary of the mail.
Mail: {email}
Summary:
"""

promtp_summary_mail = PromptTemplate.from_template(_template_summary)


_template_generate_reply = """
You are a email understanding bot your task is to read and understand given email.
And the create a reply for given email. Try to reply in good manner. Always try to
add everything asked in the email.
Given Email : {email}
Generated Reply:
"""

prompt_generate_reply =  PromptTemplate.from_template(_template_generate_reply)

_template_result_check = """
Given Email: {email}
Given Reply: {email_reply}


You are email understanding bot. Your task is to understand given mail and given email reply.
And check given reply is right or not. 

If Given reply in un-appropriate  or not contains all the information what asked in original given email
then reply `fail`
If it contain all information and genered right appropriate response reply `pass`
Always Rember 
- Return Result only `pass` or `fail`. Dont try to give an explanation.

Result:
"""

prompt_result_check = PromptTemplate.from_template(_template_result_check)

_template_rewrite_email="""
You are a helful bot. Your task is understand given email, given email summary. 

Use Given email, summary to improve the new email.

Based on this create new email with respect without using wrong words.
In return just give reply dont give any explanations.

Given Email: {email}
Give Summary: {summary}
New Email: 
"""
prompt_rewrite_new_email = PromptTemplate.from_template(_template_rewrite_email)
