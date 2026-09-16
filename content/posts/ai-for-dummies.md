---
date: '2026-09-15T12:26:29Z'
draft: false
title: 'Ai for Dummies'
---

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


# text in / text out

At its core, all ai is just a really well-tuned LLM. What's that?
Probaly too much to unpack there. Just know its a neural network
thats been tuned to take text in and generate text out.

{{< gif "images/demo.gif" >}}


# location, location, location

TLDR; context, context, context!

Given that the llm merely does text in / text out, we need
to ensure that text in has all the pertinent information.

