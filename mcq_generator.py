import os
import io
from typing import List, Union
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class MCQ(BaseModel):
    question: str = Field(description="A question text based on the pdf")
    options: List[str] = Field(description="Exactly 4 options for the multiple choice question")
    correct_answer: str = Field(description="The correct option, which must be exactly one of the options in the options list")
    explanation: str = Field(description="A explanation of why the answer is correct")

class Quiz(BaseModel):
    mcqs: List[MCQ] = Field(description="A list of multiple choice questions")

def extract_text_from_pdf(pdf_file: Union[bytes, io.BytesIO]) -> str:
    if hasattr(pdf_file, "read"):
        pdf_file = io.BytesIO(pdf_file.read())
    reader = PdfReader(pdf_file)
    print(reader)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def generate_mcqs(document_text: str, num_questions: int) -> Quiz:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    structured_llm = llm.with_structured_output(Quiz)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a teacher. Your task is to generate multiple choice questions (MCQs) based on the provided text. Generate exactly {num_questions} MCQs. Each question must have 4 options (A,B,C,D), a correct answer, and a short explanation."),
        ("user", "Generate {num_questions} MCQs based on the following document content:\n{text}")
    ])

    chain = prompt | structured_llm
    
    res = chain.invoke({
        "text": document_text,
        "num_questions": num_questions
    })
    return res
