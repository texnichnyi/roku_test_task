import urllib2, json, simplejson
# set basic url
url = "https://api.myshows.me/v2/rpc/"

#perform global authorization using build_opener
'''
auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password(None, url, 'yuriikushpit@gmail.com', 'viaboccea378')
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)
'''

#Change f3de5e180e4e754816f872ea7cbde9340055eb53 token to yours token
standartHeader={'Content-type': 'application/json', 'Authorization': 'Bearer f3de5e180e4e754816f872ea7cbde9340055eb53'}
list = []

#create standart function for request performing
def performRequest (jsonValues=None, headers=None):
    request = urllib2.Request(url, json.dumps(jsonValues), headers=headers)
    return urllib2.urlopen(request)

#add function for search show to get id for 'Add TV show by name to watch list' functionality
def performedSearch(showName):
    showIds = []
    requestJson = {
        "jsonrpc": "2.0",
        "method": "shows.Search",
        "params": {
            "query": showName
        },
        "id": 1
    }
    response = simplejson.load(performRequest(requestJson, standartHeader))
    for data in response["result"]:
        if data["titleOriginal"] == showName:
            showIds.append (data["id"])
    return showIds

#performed function for 'Add TV show by name to watch list'
def addShowByName(nameOfShow):
    showIds = performedSearch(showName=nameOfShow)
    for showId in showIds:
        requestJson = {
        "jsonrpc": "2.0",
        "method": "lists.AddShow",
        "params": {
            "id": showId,
            "list": "favorites"
        },
        "id": 1
    }
        performRequest(requestJson, standartHeader)

'''
Performed function for 'Get unwatched TV shows list'
the logic of this functionality is next:
1. I decided to use request 'profile.Shows'
2. To understand if user watch correct show I check if parameter 'watchedEpisodes' equals 0
if yes then user doesn't watched show.
'''

def getUnWachedShows():
    unWatchedShowList = []
    requestJson = {
         "jsonrpc": "2.0",
         "method": "profile.Shows",
         "params": {

        },
        "id": 1
    }
    response = simplejson.load(performRequest(requestJson, standartHeader))
    for data in response["result"]:
        if data["watchedEpisodes"] == 0:
            unWatchedShowList.append(data["show"]["title"])
    return unWatchedShowList

#performed function for 'Get names of unwatched episodes'
def getUnWatchedEpisodesName():
    names = []
    requestJson = {
        "jsonrpc": "2.0",
        "method": "lists.Episodes",
        "params": {
            "list": "unwatched"
        },
        "id": 1
    }
    response = simplejson.load(performRequest(requestJson, standartHeader))
    for data in response["result"]:
        names.append(data["episode"]["title"])
    return names

#performed function for 'Mark 1 episode as watched by it's id'
def checkFirstEpisodeAsWatched():
    requestJson = {
        "jsonrpc": "2.0",
        "method": "lists.Episodes",
        "params": {
            "list": "unwatched"
        },
        "id": 1
    }
    response = simplejson.load(performRequest(requestJson, standartHeader))
    requestChangeById = {
         "jsonrpc": "2.0",
         "method": "manage.CheckEpisode",
         "params": {
             "id": response["result"][0]["episode"]["id"],
             "rating": 0
         },
        "id": 1
    }
    simplejson.load(performRequest(requestChangeById, standartHeader))


'''
Performed function for 'Mark all episodes in one show with given name as watched'
the logic of this functionality is next:
1. Search show by name and get id of this show
2. Initialize list of with id's of all episodes
3. Use check 'manage.CheckEpisode' request to update episodes in loop
'''
def markEpisodesAsWatched(nameOfShow):
    global response
    showIds = performedSearch(showName=nameOfShow)
    episodesList = []
    for showId in showIds:
        requestEpisodesIds  = {
           "jsonrpc": "2.0",
            "method": "shows.GetById",
            "params": {
            "showId": showId,
            "withEpisodes": True
            },
            "id": 1
        }
        response = simplejson.load(performRequest(requestEpisodesIds, standartHeader))
    for data in response["result"]["episodes"]:
        episodesList.append(data["id"])
    for episodes in episodesList:
        requestJson  = {
            "jsonrpc": "2.0",
            "method": "manage.CheckEpisode",
            "params": {
            "id": episodes,
             "rating": 0
            },
            "id": 1
        }
        simplejson.load(performRequest(requestJson, standartHeader))

#Here you could call functions and test whenever you want
