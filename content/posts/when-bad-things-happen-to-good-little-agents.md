+++
title = "when bad things happen to good little agents"
date = 2026-10-27
draft = false
tags = ["ai-agents", "error-handling", "resilience", "llm-engineering", "debugging"]
ai_generated = true
+++

# when bad things happen to good little agents

Agents are fragile. They try hard, but they break. We often treat
them like magic boxes that solve problems, but they are just
probabilistic engines making guesses. Sometimes those guesses are
wrong. Sometimes they are catastrophically wrong.

The reality is that we need to design for failure, not just success.
If your agent only works when everything goes perfectly, it is not
an agent. It is a demo.

## The Illusion of Competence

Agents look smart until they hit an edge case. This is the most
dangerous part. They speak with confidence. They use polite
language. They structure their output neatly. But underneath, they
are just sampling tokens.

This leads to the "confidently wrong" problem. The agent will
hallucinate a tool name, invent a file path, or claim a task is
complete when it is barely started. Because the output looks
professional, we trust it.

Human intuition fails us here because we are used to deterministic
software. In traditional code, a bug is a bug. It crashes or it
works. In an agent, a bug is a story. It might be a plausible-sounding
explanation for why it failed. You have to read the logs, not just
the chat, to see the truth.

## Common Failure Modes

There are a few ways these little agents typically fall over.

### Looping

The agent gets stuck. It tries an action, fails, and tries the
exact same action again. It might tweak the prompt slightly, but
eventually it repeats the same mistake until you kill the process.
This burns tokens and wastes time. It is the digital equivalent of
a toddler banging their head against a door.

> **Example: The Infinite Grep**
>
> Task: "Find all TODOs in the codebase."
>
> 1. Agent runs `grep -r "TODO" .`
> 2. System returns: `Permission denied: /proc/1/mem`
> 3. Agent sees error. Decides to be more specific.
> 4. Agent runs `grep -r "TODO" . --include="*.go"`
> 5. System returns: `Permission denied: /proc/1/mem`
> 6. Agent thinks: "The permission error is unrelated to the
>    file extension. I will retry the exact same command."
> 7. Agent runs `grep -r "TODO" .`
> 8. Repeat until token limit reached.

### Hallucinated Actions

The agent decides to call a function that does not exist. Maybe it
remembers a tool from a previous conversation, or maybe it just
made it up. The system tries to execute the code, fails, and the
agent gets confused about why the world is not behaving as
expected.

> **Example: The Ghost API**
>
> Task: "