from ddgs import DDGS

# fetch web data for user query
def get_web_ctx(q, max_res=5):
    ctx = ""
    try:
        # init ddg search client
        with DDGS() as ddgs:
            # get text results
            res = ddgs.text(q, max_results=max_res)
            
            # format each result
            for idx, item in enumerate(res, 1):
                ctx += f"Source [{idx}]: {item['title']}\n"
                ctx += f"URL: {item['href']}\n"
                ctx += f"Text: {item['body']}\n\n"
    except Exception as e:
        # log failure
        print(f"search err: {e}")
        
    return ctx