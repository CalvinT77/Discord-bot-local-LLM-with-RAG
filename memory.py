import json
import os 

MEMORY_FILE = "memories.json"

#load memory by checking if memories json exists, if not then load an empty state
def load_memories():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}
# save a memory base on the user's name and the info to remember summarized by the llm    
def save_memory(user, new_info):
    data = load_memories()

    if user not in data:
        data[user] = []

    data[user].append(new_info)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# get the user's memories
def get_user_memories(user):
    data = load_memories()
    if user in data:
        return "; ".join(data[user])
    return "No prior memories."