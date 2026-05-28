import ollama
from ddgs import DDGS

def get_web_context(search_query):
    """Goes to the internet, grabs the top 3 results, and formats them."""
    print(f"\n🔍 Searching the web for: '{search_query}'...")
    formatted_context = ""
    
    try:
        # Use the updated ddgs library seamlessly
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=3)
            
            for index, result in enumerate(results, 1):
                formatted_context += f"Source [{index}]: {result['title']}\n"
                formatted_context += f"Link: {result['href']}\n"
                formatted_context += f"Text: {result['body']}\n\n"
    except Exception as error:
        print(f"❌ Search ran into an issue: {error}")
        
    return formatted_context

def ask_local_ai(query, context):
    """Feeds the web data and your question into the local Llama model."""
    print("🧠 Reading search results and writing response...")
    
    system_instructions = (
        "You are a local AI Search Engine. Answer the user's question accurately "
        "using ONLY the provided web context. You must cite your facts using inline "
        "brackets like [1], [2], pointing to the sources provided. Be concise."
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
        # 1. Get the live internet data
        web_data = get_web_context(user_input)
        
        if web_data.strip():
            # 2. Let the AI read it and answer
            ai_response = ask_local_ai(user_input, web_data)
            
            print("\n" + "="*50)
            print("🤖 ANSWER:")
            print("="*50 + "\n")
            print(ai_response)
        else:
            print("⚠️ Could not find any web results for that query.")
