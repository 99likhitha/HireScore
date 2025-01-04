from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
    #converting the pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]

        #convert to bytes
        img_byte_arr= io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
            {
                "mime_type":'image/jpeg',
                "data":base64.b64encode(img_byte_arr).decode()   #encoding to base 64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    


##streamlit UI

st.set_page_config(page_title="Resume Expert")
st.header("Application Tracking System")
intput_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload you resume here(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("resume uploaded successfully")


button1=st.button("Tell me about the my resume")

button2=st.button("What steps can I take to improve my skills?")



button3=st.button("Percentage Match")


input_prompt1= """ 
You are an experienced HR with Tech experience in the field of  Full Stack development,Data science, Web development,Data analyst, Big data engineering, Devops, Machine Learning ,Generative AI.
Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the job description.
Highlight the candidate's strengths and weaknesses, focusing on technical skills, relevant experience, and suitability for the role.

"""

input_prompt2=""" 
You are an experienced career coach and mentor with expertise in skill development across technical domains such as Full Stack Development, Data Science, Web Development, Data Analysis, Big Data Engineering, DevOps, Machine Learning, and Generative AI. 
Analyze the candidate's profile against the provided job description to identify missing or underdeveloped skills . 
Based on this gap analysis, provide a detailed and actionable plan for improving their skills. 
Include recommended learning paths, certifications, tools, projects, and resources to help them address these gaps
"""

input_prompt3=""" 
You are a skilled Application tracking system scanner with a deep understanding in assessing candidate profiles against job descriptions for roles in Full Stack Development, Data Science, Web Development, Data Analysis, Big Data Engineering, DevOps, Machine Learning, and Generative AI.
Your task is to calculate the percentage match between the provided resume and the job description. Consider factors such as required skills, relevant experience, certifications, technical expertise, and alignment with job responsibilities.
Provide a detailed breakdown of the highlighting areas where the candidate excels and where they fall short.
"""


if button1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,intput_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a pdf")


elif button2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,intput_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a pdf")


elif button3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,intput_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a pdf")