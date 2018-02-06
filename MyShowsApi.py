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

#create standart function for request performing
def performRequest (jsonValues=None, headers=None):
    request = urllib2.Request(url, json.dumps(jsonValues), headers=headers)
    return urllib2.urlopen(request)

#add function for preparing json
def prepareJson(methodName, parameters={}):
    requestJson = {
        "jsonrpc": "2.0",
        "method": methodName,
        "params": parameters,
        "id": 1
    }
    return requestJson

#add function for search show to get id for 'Add TV show by name to watch list' functionality - > Request:[shows.Search]
def performedSearch(showName):
    showIds = []
    parameters = {"query": showName}
    requestJson = prepareJson("shows.Search", parameters)
    response = simplejson.load(performRequest(requestJson, standartHeader))
    for data in response["result"]:
        if data["titleOriginal"] == showName:
            showIds.append (data["id"])
    return showIds

#performed function for 'Add TV show by name to watch list' - > Request:[lists.AddShow]
def addShowByName(nameOfShow):
    showIds = performedSearch(showName=nameOfShow)
    for showId in showIds:
        parameter = {
            "id": showId,
            "list": "favorites"
        }
        requestJson = prepareJson("lists.AddShow", parameter)
        performRequest(requestJson, standartHeader)

'''
Performed function for 'Get unwatched TV shows list'
the logic of this functionality is next:
1. I decided to use request 'profile.Shows'
2. To understand if user watch correct show I check if parameter 'watchedEpisodes' equals 0
if yes then user doesn't watched show.
Request:[profile.Shows]
'''

def getUnWatchedShows():
    unWatchedShowList = []
    requestJson = prepareJson("profile.Shows")
    response = simplejson.load(performRequest(requestJson, standartHeader))
    for data in response["result"]:
        if data["watchedEpisodes"] == 0:
            unWatchedShowList.append(data["show"]["title"])
    return unWatchedShowList


#performed function for 'Get names of unwatched episodes' - > Request:[lists.Episodes]
def getUnWatchedEpisodesName():
    names = []
    parameters = {"list": "unwatched"}
    requestJson = prepareJson("lists.Episodes", parameters)
    response = simplejson.load(performRequest(requestJson, standartHeader))
    for data in response["result"]:
        names.append(data["episode"]["title"])
    return names


#performed function for 'Mark 1 episode as watched by it's id' - > Request:[lists.Episodes] - > Request:[manage.CheckEpisode]
def checkFirstEpisodeAsWatched():
    requestJson = prepareJson("lists.Episodes", {"list": "unwatched"})
    response = simplejson.load(performRequest(requestJson, standartHeader))
    parameters = {
        "id": response["result"][0]["episode"]["id"],
        "rating": 0
    }
    requestChangeById = prepareJson("manage.CheckEpisode", parameters)
    simplejson.load(performRequest(requestChangeById, standartHeader))

'''
Performed function for 'Mark all episodes in one show with given name as watched'
the logic of this functionality is next:
1. Search show by name and get id of this show
2. Initialize list of with id's of all episodes
3. Use check 'manage.CheckEpisode' request to update episodes in loop
Request:[shows.GetById] - > Request:[manage.CheckEpisode]
'''
def markEpisodesAsWatched(nameOfShow):
    global response
    showIds = performedSearch(showName=nameOfShow)
    episodesList = []
    for showId in showIds:
        parameters = {
            "showId": showId,
            "withEpisodes": True
        }
        requestEpisodesIds = prepareJson("shows.GetById", parameters)
        response = simplejson.load(performRequest(requestEpisodesIds, standartHeader))
    for data in response["result"]["episodes"]:
        episodesList.append(data["id"])
    for episodes in episodesList:
        parameters = {
            "id": episodes,
            "rating": 0
        }
        requestJson  = prepareJson("manage.CheckEpisode", parameters)
        simplejson.load(performRequest(requestJson, standartHeader))

#Here you could call functions and test whenever you want


