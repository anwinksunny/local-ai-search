import ollama

# streams structured response from local ollama
def ask_ai_stream(q, ctx):
    # sys instructions to force live facts and ban placeholder templates
    sys_prompt = (
        "You are an up-to-date, real-time AI search engine. "
        "Answer the user's query in a natural, cohesive, and direct way based on the provided web context.\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. Avoid writing robotic template tables, placeholders (like '[Not available]'), or complaining notes about missing data. "
        "Simply summarize the actual facts present in the text in a helpful, conversational paragraph.\n"
        "2. Never state 'as of my last update' or mention your knowledge cutoff (such as December 2023). Speak confidently in the present tense.\n"
        "3. Focus strictly on chronological facts. If a new leader has taken office in a recent election (e.g., 2026), identify the successor as the current incumbent and the previous leader as the predecessor.\n"
        "4. Summarize directly without safety refusals for public figures.\n"
        "5. Structure your response with clean, logical headings and bullet points only where helpful, and cite sources using inline brackets like [1], [2], etc."
    )
    # user text prompt
    user_prompt = f"Web Context:\n{ctx}\n\nQuery: {q}"
    
    try:
        # stream resp from ollama
        resp = ollama.chat(
            model='llama3.2:1b', # set model
            messages=[
                {'role': 'system', 'content': sys_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            stream=True,
            options={
                "temperature": 0.0  # force deterministic output
            }
        )
        # yield chunks
        for chunk in resp:
            yield chunk['message']['content']
    except Exception as e:
        # send err message
        yield f"\nerror: {e}"