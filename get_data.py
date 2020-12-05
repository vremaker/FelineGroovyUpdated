import urllib.request, urllib.error, urllib.parse, json, webbrowser

### Utility functions you may want to use
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request." )
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

def get_reddit_posts(sub="memes", baseurl= "https://www.reddit.com/r/memes/.json"): 
    print(baseurl)
    gotten = safe_get(baseurl)
    if gotten is not None:
        gotten_str = gotten.read()
        gotten_json = json.loads(gotten_str)
        return gotten_json["data"]["children"]

def get_image_list(data):
    #print(len(data))
    images = []
    for item in data:
        content = item["data"]["url"]
        if not "comments" in content:
            images.append(content)
       # print((item["data"]["selftext"]))
    return(images)  

def get_image_html_list(data):
    #print(len(data))
    images = []
    for item in data:
        content = item["data"]["url"]
        if not "comments" in content:
            images.append("<img src='" + content + " alt='meme' />")
       # print((item["data"]["selftext"]))
    return(images)    
if __name__ == '__main__':
    ### Testing your building blocks
    print('\n\nTesting your building blocks\n------------')
    #
    # Test get_photo_ids() with the following line of code, which
    # will give four photo IDs that match the query "hamster".
    #
    # The ids you get may be different than what's in the sample 
    # output - you are working with live data!
    #
    data = get_reddit_posts()
    print(get_image_list(data))