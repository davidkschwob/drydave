#!/usr/bin/env python3
import os
import sys
import subprocess
from datetime import datetime
from groq import Groq

# build a post interactively using multiple turns on a free tier Groq hosted LLM


# converts article title to a clean url
def clean_slug(text):
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789 "
    clean_text = "".join(c for c in text.lower() if c in allowed)
    return "-".join(clean_text.split())


# load some recent examples of my writing style
def get_style_context():
    posts_dir = "content/posts"
    if not os.path.isdir(posts_dir):
        return "No historical style data found."

    files = [
        os.path.join(posts_dir, f) for f in os.listdir(posts_dir) if f.endswith(".md")
    ]
    if not files:
        return "No historical style data found."

    files.sort(key=os.path.getmtime, reverse=True)
    recent_files = files[:2]

    context = "Reference style examples from my blog:\n"
    for file_path in recent_files:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                context += f"\n--- START SAMPLE ({file_path}) ---\n"
                context += "\n".join(lines[:40])
                context += f"\n--- END SAMPLE ---\n"
        except Exception:
            continue
    return context


def main():
    if len(sys.argv) < 2:
        print("ERROR: Please provide a blog post topic.")
        print('Usage: gen-post "Your Topic Here"')
        sys.exit(1)

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY environment variable not set.")
        sys.exit(1)

    topic = sys.argv[1]
    slug = clean_slug(topic)
    output_file = f"content/posts/{slug}.md"

    client = Groq(api_key=api_key)
    model_name = "qwen/qwen3.8-27b"

    toml_delimiter = "+++"
    current_system_date = datetime.now().strftime("%Y-%m-%d")

    print("Reading repository history for style tracking...")
    style_context = get_style_context()

    base_system = (
        "You are an automated software agent compiling content for a Hugo static website. "
        "You communicate exclusively using plain ASCII characters. You write blog content "
        "using clean Markdown with short, scannable paragraphs."
        "Paragraphs should be wrapped at 80 columns for terminal friendly viewing."
    )

    # --- TURN 1: STRATEGY & PLANNING ---
    print("Executing Turn 1: Generating structural outline...")
    messages = [
        {"role": "system", "content": base_system},
        {
            "role": "user",
            "content": f"Create a short structural outline, target tags, and content strategy for a blog post titled: '{topic}'. Keep the plan brief.",
        },
    ]

    try:
        response_1 = client.chat.completions.create(
            model=model_name, messages=messages, temperature=0.3, max_tokens=300
        )
        strategy = response_1.choices[0].message.content
        messages.append({"role": "assistant", "content": strategy})

        # Initial draft prompt setup
        draft_prompt = (
            f"Now, use that exact structural outline to write the complete first draft of the post.\n\n"
            f"CRITICAL LAYOUT RULES:\n"
            f"1. You MUST start the text immediately with TOML front matter wrapped in +++ delimiters.\n"
            f"2. The front matter MUST contain: title, date (YYYY-MM-DD), draft=false, tags, and 'ai_generated = true'.\n"
            f"3. Do not use Markdown code fences (```) around the entire post.\n\n"
            f"{style_context}\n\n"
            f"Generate the full text draft now."
        )
        messages.append({"role": "user", "content": draft_prompt})

        # --- TURN 2: DRAFT & FEEDBACK LOOP ---
        draft_prompt = (
            f"Now, use that exact structural outline to write the complete first draft of the post.\n\n"
            f"CRITICAL LAYOUT RULES:\n"
            f"1. You MUST start the text immediately with TOML front matter wrapped in {toml_delimiter} delimiters.\n"
            f"2. The front matter MUST contain exactly:\n"
            f'   title = "{topic}"\n'
            f"   date = {current_system_date}\n"
            f"   draft = false\n"
            f'   tags = ["tag1", "tag2"]\n'
            f"   ai_generated = true\n"
            f"Generate the full text draft now."
        )
        messages.append({"role": "user", "content": draft_prompt})

        draft_count = 1
        while True:
            print(
                f"\nExecuting Turn 2 (Draft #{draft_count}): Generating text payload..."
            )
            response_2 = client.chat.completions.create(
                model=model_name, messages=messages, temperature=0.7, max_tokens=600
            )
            current_draft = response_2.choices[0].message.content

            # Print the draft formatting boundaries clearly for user review
            print("\n=================== CURRENT DRAFT CONTENT ===================")
            print(current_draft)
            print("=============================================================")

            # Prompt the human for iterative feedback
            print("\nREVIEW REQUIRED:")
            print("To accept this draft, type: ok")
            print(
                "Otherwise, type your revision feedback below (e.g., 'Make section 2 more technical'):"
            )
            user_input = input(">> ").strip()

            match user_input.lower():
                case "ok":
                    # Save the approved draft to the chat history array and break the loop
                    messages.append({"role": "assistant", "content": current_draft})
                    break
                case _:
                    # TOKEN OPTIMIZATION: Flush conversational history up to this exact active state.
                    # Drops historical failures/outlines to flatten the token footprint.
                    messages = [
                        {"role": "system", "content": base_system},
                        {"role": "assistant", "content": current_draft},
                    ]
                    feedback_prompt = (
                        f"Please rewrite the blog post draft based strictly on this human feedback: {user_input}\n\n"
                        f"Ensure you maintain our baseline configuration style:\n{style_context}"
                    )
                    messages.append({"role": "user", "content": feedback_prompt})
                    draft_count += 1

        # --- TURN 3: QUALITY CONTROL REFINEMENT ---
        print(
            "\nExecuting Turn 3: Auditing formatting structure and finalizing post..."
        )
        refine_prompt = (
            "Review the finalized draft you just approved. Audit it against these zero-tolerance criteria:\n"
            "- Does it start exactly with +++ and valid TOML front matter?\n"
            "- Is 'ai_generated = true' present inside the front matter?\n"
            "- Is the entire response raw markdown rather than encapsulated inside a global code fence?\n\n"
            "If any formatting rule is broken, fix it immediately. Output ONLY the finalized, ready-to-publish Hugo markdown file text."
        )
        messages.append({"role": "user", "content": refine_prompt})

        response_3 = client.chat.completions.create(
            model=model_name, messages=messages, temperature=0.1, max_tokens=700
        )
        final_post = response_3.choices[0].message.content

        if "+++" in final_post:
            final_post = final_post[final_post.find("+++") :]

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_post)

        print(
            f"\nSUCCESS: Post created successfully after {draft_count} draft iterations."
        )
        print(f"File saved: {output_file}")

    except Exception as e:
        print(f"ERROR: Pipeline execution failed. Detailed error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
