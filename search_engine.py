from ddgs import DDGS

# fetch web data for user query
def get_web_ctx(q, max_res=5):
    ctx = ""
    try:
        # identify important keywords to filter out rate-limit spam
        stop_words = {"the", "is", "and", "or", "of", "in", "at", "to", "a", "an", "who", "what", "where", "how", "current"}
        query_words = [w.lower() for w in q.split() if w.lower() not in stop_words and len(w) > 1]
        
        # init ddg search client
        with DDGS() as ddgs:
            # get text results
            res = ddgs.text(q, max_results=max_res)
            
            valid_count = 0
            for item in res:
                title = item.get('title', '').lower()
                body = item.get('body', '').lower()
                
                # check if snippet shares at least one keyword with the query
                is_relevant = any(word in title or word in body for word in query_words) if query_words else True
                
                if is_relevant:
                    valid_count += 1
                    ctx += f"Source [{valid_count}]: {item['title']}\n"
                    ctx += f"URL: {item['href']}\n"
                    ctx += f"Text: {item['body']}\n\n"
    except Exception as e:
        # log failure
        print(f"search err: {e}")
        
    return ctx

# fetch images for query
def get_web_images(q, max_images=8):
    images = []
    try:
        # init ddg search client
        with DDGS() as ddgs:
            try:
                # fetch images with query param
                res = ddgs.images(query=q, max_results=max_images)
            except TypeError:
                # fallback for old library version
                res = ddgs.images(keywords=q, max_results=max_images)
                
            for item in res:
                images.append({
                    "title": item.get("title", ""),
                    "image_url": item.get("image", ""),
                    "thumbnail_url": item.get("thumbnail", "")
                })
    except Exception as e:
        # log image fetch failure
        print(f"image search err: {e}")
        
    return images