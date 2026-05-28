import ollama
from ddgs import DDGS

def get_web_context(search_query):
    """Goes to the internet, grabs the top 5 results for more depth."""
    print(f"\n🔍 Searching the web for: '{search_query}'...")
    formatted_context = ""
    
    try:
        with DDGS() as ddgs:
            # Increased max_results to 5 for a meatier context
            results = ddgs.text(search_query, max_results=5)
            
            for index, result in enumerate(results, 1):
                formatted_context += f"Source [{index}]: {result['title']}\n"
                formatted_context += f"Link: {result['href']}\n"
                formatted_context += f"Text: {result['body']}\n\n"
    except Exception as error:
        print(f"❌ Search ran into an issue: {error}")
        
    return formatted_context

def ask_local_ai(query, context):
    """Feeds the web data and your question into the local Llama model."""
    print("🧠 Analyzing deep search results and synthesizing a detailed report...")
    
    # Rewritten system instructions to demand a longer, structured response
    system_instructions = (
        "You are an advanced, thorough AI Search Engine. Provide a detailed, comprehensive, "
        "and structured response to the user's query using the provided web context.\n\n"
        "Guidelines:\n"
        "1. Start with a clear, detailed definition or summary.\n"
        "2. Break down the information into logical sections (e.g., Causes, Effects, Regional Impact) using bullet points or subheadings.\n"
        "3. Incorporate as many relevant details from the sources as possible.\n"
        "4. Constantly cite your sources using inline brackets like [1], [2] right after the facts you present.\n"
        "5. Do not give a short answer. Be thorough and explanatory."
    )
    
    user_prompt = f"Web Context:\n{context}\n\nUser Question: {query}"
    
    try:
        response = ollama.chat(model='llama3.2:1b', messages=[
            {'role': 'system', 'content': system_instructions},
            {'role': 'user', 'content': user_prompt}
        ])
        return response['message']['content']
    except Exception as error:
        return f"❌ AI Error: {error}. Is Ollama currently running?"

# --- Main Program Execution ---
if __name__ == "__main__":
    print("=== LOCAL AI SEARCH ENGINE READY ===")
    user_input = input("What do you want to search for? ")
    
    if user_input.strip():
        web_data = get_web_context(user_input)
        
        if web_data.strip():
            ai_response = ask_local_ai(user_input, web_data)
            
            print("\n" + "="*50)
            print("🤖 AI DETAILED ANSWER:")
            print("="*50 + "\n")
            print(ai_response)
        else:
            print("⚠️ Could not find any web results for that query.")