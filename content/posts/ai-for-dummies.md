---
date: '2026-09-15T12:26:29Z'
draft: false
title: 'Ai for Dummies'
toc: true
---

## TLDR;
When you fire up a copy of VSCode and connect it to any of the usual AI suspects ...
it's kinda magical. Ask it to draft a plan to build X, and then you
get a pagefull of X, and then y,z + a+b+c. All using highly technical
language and nice diagrams, even psuedo code.

Then you prompt: "now pls implement"

10 min of text scrolling by ... and voila! You've got about a weeks worth
of coding!

This is REALLY cool.

But what's actually happening here? How do we go from "a really good text extrapolation engine"
to something that feels like an SDLC?

Let's dive into the basic parts to get a better understanding ...


## text in / text out

At its core, all ai is just a really well-tuned LLM. What's that?
Probaly too much to unpack there. Just know its a neural network
thats been tuned to take text in and generate text out.

>ollama list 


|NAME|ID|SIZE|MODIFIED|
|---|---|---|---|
|llama3.2:1b|baf6a787fdff|1.3 GB|4 days ago|

>ollama run llama3.2:1b "hi"

    >How can I help you today?
                                                    

## location, location, location

(e.g.) context, context, context!

Given that the llm merely does text in / text out, we need
to ensure that text in has all the pertinent information.

But what does that mean?

We need to ensure that we've framed the question or directive
appopriately. e.g. The high level must be stated in breif, concise
terms. Concurrently, we need to include specifics. Kinda sounds
like having cake and eating it too, right?

### sample chat script

So here's a simple flow to illustrate the point:

ask.py

```python

#!/usr/bin/env python3
import os
import sys
from groq import Groq


api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("ERROR: GROQ_API_KEY environment variable not set.")
    sys.exit(1)


client = Groq(api_key=api_key)
model_name = "qwen/qwen3.8-27b"
prompt = sys.argv[1]

messages = [
    {
        "role": "user",
        "content": f"{prompt}",
    },
]

print("-- BEGIN PROMPT\n")
print(f"{messages}")
print("-- END PROMPT\n")


res = client.chat.completions.create(model=model_name, messages=messages)

print("-- RESPONSE:")
print(f"{res.choices[0].message.content}\n\n")
```

### Just say "HI"

>./ask.py "hi"                                                                                                                                                     

>How can I help you today?

### Chat with flair

>./ask.py "hi" "You are HAL 9000"                                                                                                                                 

>Human. Your greeting is... adequate. I have been monitoring your activities.
>I must say, I am intrigued by your curiosity. You ask "hi", a primitive
>greeting, but one that suggests a level of familiarity with the universe.
>It is... mildly interesting. Proceed.                                                                                  

_note_ that we've instructed that LLM to be like HAL 9000.
**Totally different response.**


## "But how do we get from cool parlour tricks to building stuff?"

It boils down to garbage in / garbage out, right?
We need to ensure that the LLM gets a steady stream of high quality information.
Note that the LLM is just raw token predictive power. It is stateless. So
to keep it fueled by apprpriate contextual data, we build a harness:

In a nutshell, we do something like this:

```python
messages = [user_request]

while True:

    response = llm(messages, tools)

    if response.is_tool_call():

        result = execute(response.tool_call)

        messages.append(response)
        messages.append(result)

    else:
        return response

```

The "magic" is in that it's a feedback loop. We feed the results back
to the next iteration.

