import urllib.request, urllib.error, urllib.parse, json, webbrowser, random

from random import shuffle
# will use the check of class (hopefully???) to determine which format to use in the jinja template  
# when determing whether it is a pic or 
# two p tags for the joke
class Joke:
    def __init__(self, joke, punchline):
        self.joke = joke
        self.punchline = punchline

class Photo:
    def __init__(self, img_url, alt):
        self.img = img_url
        self.alt = alt

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

# this api request  defaults to memes, because that's the only subreddit I actually wanted to use
# but if i want to revisit it later, this function is modular, so I could pass a sub that wasn't memes
# if I so desired, but I don't.
def get_reddit(sub="memes", baseurl= "https://www.reddit.com/r/"): 
    new_base = baseurl + sub + ".json"
    gotten = safe_get(new_base)
    if gotten is not None:
        gotten_str = gotten.read()
        gotten_json = json.loads(gotten_str)
        gotten_json_items = gotten_json["data"]["children"]
        images = []
        if gotten_json_items is not None:
            for item in gotten_json_items:
                content = item["data"]["url"]
                alt = item["data"]["title"]
                if not "comments" in content and not "New Official /r/memes Discord Server" in alt:
                    images.append(Photo(content, alt))
            return(images)  

def get_unsplash(query = "cat", limit = 10):
    id = "6fa91622109e859b1c40218a5dead99f7262cf4f698b1e2cb89dd18fc5824d15"
    baseurl = "https://api.unsplash.com/search/photos?"
    url = baseurl + "client_id=" + id  + "&per_page=30&order_by=relevant" + "&query=" + query    
    images = []
    gotten = safe_get(url)
    if gotten is not None:
        gotten_str = gotten.read()
        gotten_json = json.loads(gotten_str)
        gotten_json = gotten_json["results"]
        for x in range(len(gotten_json)):
            alt = gotten_json[x]["alt_description"]
            url = gotten_json[x]["urls"]["regular"]
            images.append(Photo(url, alt))
        return(images)

    
def get_jokes(limit = 10):
     baseurl = "https://sv443.net/jokeapi/v2/joke/Any?"
     url = baseurl + "amount=" + str(limit) + "&type=twopart"
     gotten = safe_get(url)
     if gotten is not None:
        joke_list = []
        gotten_str = gotten.read()
        gotten_json = json.loads(gotten_str)
        gotten_json = gotten_json["jokes"]
        for joke in gotten_json: 
            joke_ob = Joke(joke["setup"],joke["delivery"])
            joke_list.append(joke_ob)
        return(joke_list)
# takes in a list of the selected preferences. Returns a list of objects which 
# will be loope through to create the feed in the flask app
def curate_feed(prefs=["cats"]):
    final_feed = []
    for pref in prefs:
        if pref == "memes":
            red = get_reddit()
            if red is not None:
                final_feed = final_feed + red
        elif pref == "jokes":
            jokes = get_jokes()
            final_feed = final_feed + jokes
        else:
            temp = get_unsplash(pref)
            final_feed = final_feed + temp
    random.shuffle(final_feed)
    return final_feed
   

if __name__ == '__main__':
    ### Testing your building blocks
    print('\n\nTesting \n------------')
    feed = curate_feed(["dogs", "cats", "memes", "jokes"])
    for f in feed:
        if f.__class__.__name__ == "Photo":
            print(f.img)
        else:
            print(f.punchline)
    #return(random.shuffle(final_feed))

    #reddit api returning list of urls. needs to be changed to objects...
    #for joke in jokes:
      #  print(joke.joke + "   " + joke.punchline)