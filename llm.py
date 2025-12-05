from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import memory
from datetime import datetime
from dotenv import load_dotenv
import re
from os import getenv

load_dotenv()


# CONFIGURATION
REPO_ID = getenv("REPO_ID")
FILENAME = getenv("FILENAME") 
CACHE_DIR = getenv("CACHE_DIR")

print(f"Checking for model in {CACHE_DIR}...")

# Get the real path (handles the complex snapshot folders automatically)
model_path = hf_hub_download(
    repo_id=REPO_ID,
    filename=FILENAME,
    cache_dir=CACHE_DIR
)

print(f"Loading model from: {model_path}")

#Initialize the model using the path we just found
# We do this outside a try/except block because if this fails, 
# the bot shouldn't start anyway.
llm_model = Llama(
    model_path=model_path,  
    n_gpu_layers=-1,        # -1 = Offload all layers to GPU
    n_ctx=9168,             # Set context window 
    verbose=True            # Keeps logs on so you can see if GPU is working
)
# --- HELPER FUNCTION ---
def clean_response(full_response):
    """
    Removes <think>...</think> tags and returns only the final answer.
    """
    # Regex to find everything between <think> tags (including newlines)
    # flags=re.DOTALL makes the dot (.) match newlines too
    cleaned = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL)
    return cleaned.strip()

def remember(user, prompt):
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    sys_prompt = (
        "Analyze the message. Return strictly in this format: "
        "'YES | <short summary containing user's fact/preferences>' if it contains user facts/preferences about the user specifically. "
        "'NO' if it is chit-chat. "
        "Do not output thinking."
        f"Current Date: {current_date}. "
    )
    
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": f"{datetime.date} {user}: {prompt}"}
    ]

# low max tokens to get a good summary and low temperature to keep consistent format
    output = llm_model.create_chat_completion(
        messages=messages,
        max_tokens=256,
        temperature=0.1
    )

    full_response = output['choices'][0]['message']['content']
    
    # final answer is the cleaned version
    final_answer = clean_response(full_response)
    
    print(f"[DEBUG] Raw Remember: {full_response[:50]}...")
    print(f"[DEBUG] Clean Remember: {final_answer}")

    #Parse the Cleaned Result
    if "YES |" in final_answer:
        # Split only on the first '|' just in case the summary has one
        parts = final_answer.split("|", 1)
        if len(parts) > 1:
            summary = parts[1].strip()
            memory.save_memory(user, summary)
            return True
            
    return False

def llm_speak(user, prompt):
    # Retrieve existing memories
    user_memories = memory.get_user_memories(user)
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    # Inject memories into the System Prompt
    system_message = (
        f"You are a helpful AI assistant that rarely uses emoticons. "
        f"Current Date: {current_date}. "
        f"Here is what you know about the user from your memory, '{user}': [{user_memories}]. "
        "If the user asks a personal question about themselves specifically, check your memory and see if any of the information is relevent to their response and if so use it to personalize your response, also their facts are not yours so do not confuse that or you will be heavily penalized."
    )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{user}: {prompt}"}
    ]

    output = llm_model.create_chat_completion(
        messages=messages,
        max_tokens=512,
        temperature=0.7
    )

    # ... (Keep your existing Parsing Logic here) ...
    full_response = output['choices'][0]['message']['content']
     # --- Thinking Parsing Logic -
    thinking_content = ""
    final_content = full_response

    # removes <think> tags
    if "</think>" in full_response:
        parts = full_response.split("</think>")
        if len(parts) > 1:
            raw_thinking = parts[0]
            thinking_content = raw_thinking.replace("<think>", "").strip()
            final_content = parts[1].strip()

    if thinking_content:
        print(f"Thinking Process:\n{thinking_content}\n")

    return final_content
