import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.schema import SystemMessage, HumanMessage
import re

# Loading HuggingFace and OpenAI:
load_dotenv(".env")
OPENAIKEY = os.getenv("OPENAI_API_KEY")


st.title("Flashcard Generator")

def generate_flashcards(user_text):
    # Step 3: Use the text to generate flashcards using OpenAI's GPT-3 API
    model = ChatOpenAI(temperature=1, openai_api_key=OPENAIKEY)
    chat_history = [
        SystemMessage('''Generate 3 flashcards with both the question and answer being less than two sentences. Use the format provided below:
        
                        Flashcard 1: What are the three phases of interphase?
                         Answer: Gap 1 (G1), DNA synthesis (S), and Gap 2 (G2).
                         Flashcard 2: What happens during interphase?
                         Answer: Preparations for cell division occur, including growth, duplication of most cellular contents, and replication of DNA. 
                         Flashcard 3: What is mitosis?
                         Answer: Mitosis is the process of active division in which duplicated chromosomes attach to spindle fibers, align along the equator of the cell, and then separate.'''),
        HumanMessage(user_text)
    ]

    # Generate flashcards
    flashcards = str(model(chat_history))
    
    # Extract flashcards
    flashcard_texts = [str(result) for result in re.findall(r'Flashcard \d+: (.*?)Flashcard \d+:|Flashcard \d+: (.*?)$', flashcards, re.MULTILINE)]
    flashcards_list = [f"Flashcard {idx + 1}: {flashcard_text.strip()}" for idx, flashcard_text in enumerate(flashcard_texts)]
    
    return flashcards_list

# The text for generating flashcards 
user_text = st.text_input("Enter the text you want to generate flashcards for:")

if st.button("Generate Flashcards"):
    flashcards_output = generate_flashcards(user_text)
    sorted_flashcards = sorted(flashcards_output)  # Sort the flashcards

    for flashcard in sorted_flashcards:
        st.write(flashcard)
        print(flashcard)


# Streamlit 
# Step 4: Save the flashcards to a file
# Step 5: Use the HuggingFace API to upload the flashcards to the HuggingFace Hub
# Step 6: Share the link to the flashcards with the user
# Step 7: Allow the user to download the flashcards

