from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

links = {}

headers = {"authorization": "token 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"}


def makeAPICall(request, account):
    try:
        return requests.get(
            'https://api.github.com/users/{}'.format(account),
            headers=headers).text
    except AttributeError:
        pass
    except Exception:
        return render(request, 'misc.html', {"error": "User {} does not exist!".format(account)})


def appendLinks(acc):
    try:
        obj = {
            "followers": acc["followers_url"],
            "following": acc["following_url"].split("{")[0],
            "repos": acc["repos_url"]
        }
        links[acc["login"]] = obj
        return obj
    except Exception as e:
        print(e)
        pass

def getProfiles(request, name):
    profiles = []
    accounts = [x.strip() for x in name.split('&')]
    try:
        for account in accounts:
            res = makeAPICall(request, account)
            acc = json.loads(res)
            appendLinks(acc)
            profiles.append({"name": acc["name"], "login": acc["login"], "picture": acc["avatar_url"], "link": acc["html_url"], "followers": acc["followers_url"],
                             "following": acc["following_url"].split("{")[0], "repos": acc["repos_url"], "title": acc["company"], "bio": acc["bio"]})
    except Exception:
        pass
    finally:
        return {'profiles': profiles}


def miscView(request):
    def call(url):
        res = requests.get(url, headers=headers).text
        return json.loads(res)

    def addInstance(view, account, _type):
        res = makeAPICall(request, account)
        acc = json.loads(res)
        data = call(appendLinks(acc)[view])
        return render(request, "misc.html", {_type: data})
    try:
        [view, account] = request.path.strip().split("/")[1:]
        _type = "profiles" if view == "following" or view == "followers" else "repos"
        if account in links:
            profile = links[account]
            return render(request, "misc.html", {_type: call(profile[view])})
        return addInstance(view, account, _type)
    except KeyError:
        return addInstance(view, account, _type)
    except Exception as e:
        print(e)
        return render(request, "misc.html", {"error": "{} is not a registered github user!".format(account)})

def defaultView(request):
    return render(request, 'default.html')

def landingView(request):
    return render(request, 'instructional.html')


def profileView(request, names):
    return render(request, 'profile.html', getProfiles(request, names))
