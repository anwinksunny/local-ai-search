import ollama

# streams response from local ollama
def ask_ai_stream(q, ctx):
    # sys instructions
    sys_prompt = (
        "You are an AI search engine. "
        "Answer the user query based ONLY on the provided web context. "
        "Always cite sources using [1], [2], etc."
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
            stream=True
        )
        # yield chunks
        for chunk in resp:
            yield chunk['message']['content']
    except Exception as e:
        # send err message
        yield f"\nerror: {e}"