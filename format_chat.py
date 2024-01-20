# read history/history.txt

messages = []
with open("history/history.txt", "r") as f:
    # read lines
    lines = f.readlines()
    person = ""
    content = ""
    old_person = ""
    for line in lines:
        if(line.strip() == ""): continue
        if ", [" in line and "]" in line: # name tag
            try:
                person = line.split(", [")[0]
            except:
                print(line)
            if(person != old_person): # person changed
                if(old_person == "Benn Tan"): # benn is the assistant
                    messages.append({"role": "user", "content": content})
                else: # other person is the user
                    messages.append({"role": "assistant", "content": content}) 
                content = ""
                old_person = person
        else:
            content += line.strip() + '\n'

prompt = {"role": "system", "content": "You are Benn Tan. Respond to the following messages mimicking his language and catchphrases. Try to talk like a human and not like a chatbot."}
training_data = []
for i in range(1,len(messages),2):
    assert(messages[i]["role"] == "user")
    assert(messages[i+1]["role"] == "assistant")
    training_data.append({"messages": [prompt, messages[i], messages[i+1]]})

# save to jsonl
keywords = ['choice', 'fk', 'lah', 'die', 'gone']
import json
with open("history/training_data_small.jsonl", "w") as f:
    for data in training_data:
        include = False
        for keyword in keywords: 
            if(keyword in data["messages"][1]["content"]): 
                include = True
        if(include):
            print(data)
            f.write(json.dumps(data) + '\n')


pass