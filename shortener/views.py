from django.http.response import Http404, HttpResponseRedirect
from shortener.models import ShortenedURL
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.utils import IntegrityError

# Create your views here.

def home_view(request):
    return HttpResponse("Hello world")

def redirect_view(request, shortened_part):

    try:
        shortenedURL = ShortenedURL.objects.get(shortURL = shortened_part)
        shortenedURL.clicks += 1
        shortenedURL.save()

        return HttpResponseRedirect(shortenedURL.longURL)

    except:
        raise Http404("Sorry, this link is broken or doesn't exist :(")

def stats_view(request, shortened_part):

    try:
        shortenedURL = ShortenedURL.objects.get(shortURL = shortened_part)

        return HttpResponse(f"Short URL {shortenedURL.shortURL} has had {shortenedURL.clicks} clicks and leads to {shortenedURL.longURL}")

    except:
        raise Http404("Sorry, this link is broken or doesn't exist :(")

def create_endpoint(request):

    if request.method == "GET":

        try:
            unshortenedURL = request.GET["long"]
        except:
            return JsonResponse({'error': 'LONG URL not provided.'}, status = 400)
        
        if unshortenedURL.replace(" ", "") == "":
            return JsonResponse({'error': 'LONG URL is blank.'}, status = 400)


        shortenedURL = ShortenedURL(longURL = unshortenedURL)
        shortenedURL.save()

        return JsonResponse({'long_url': shortenedURL.longURL, 'short_url': shortenedURL.shortURL})
    else:
        return JsonResponse({'error': 'Request is not type GET'}, status = 400)

def stats_endpoint(request, shortened_part):

    try:
        shortenedURL = ShortenedURL.objects.get(shortURL = shortened_part)

        return JsonResponse({'long_url': shortenedURL.longURL, 'short_url': shortenedURL.shortURL, 'clicks': shortenedURL.clicks, 'created': shortenedURL.created, 'is_vanity': shortenedURL.isVanity, 'id': shortenedURL.id})
    except:
        return JsonResponse({'error': 'URL is broken or does not exist.'}, code = 404)

def vanity_create_endpoint(request):

    if request.method == "GET":
        try:
            vanitySlug = request.GET["vanity"]
            unshortenedURL = request.GET['long']
        except:
            return JsonResponse({'error': 'No vanity slug or long URL was provided.'}, status = 400)

        if unshortenedURL.replace(" ", "") == "":
            return JsonResponse({'error': 'LONG URL is blank.'}, status = 400)

        if vanitySlug in ['admin', 'api']:
            return JsonResponse({'error': 'Vanity slug requested is blocked from use.'}, status = 403)

        try:
            authToken = request.GET["auth"]
        except:
            return JsonResponse({'error': 'Bad auth token'}, status = 403)

        if authToken != "testingtoken":
            return JsonResponse({'error': 'Bad auth token'}, status = 403)
        
        try:
            shortenedURL = ShortenedURL(longURL = unshortenedURL, shortURL = vanitySlug, isVanity = True)
            shortenedURL.save()
        except IntegrityError:
            return JsonResponse({'error': 'Vanity link requested already exists'}, status = 409)

        return JsonResponse({'long_url': shortenedURL.longURL, 'short_url': shortenedURL.shortURL})

    else:
        return JsonResponse({'error': 'Request is not type GET'}, status = 400)

def list_all_endpoint(request):

    if request.method == "GET":
        try:
            authToken = request.GET["auth"]
            if authToken != "testingtoken":
                return JsonResponse({'error': 'Bad auth token'}, status = 403)
        except:
            return JsonResponse({'error': 'Bad auth token'}, status = 403)

        response = {'shortened_urls': {}, 'count': 0}
        allShortenedURLs = ShortenedURL.objects.all()

        response['count'] = len(allShortenedURLs)

        for shortenedURL in allShortenedURLs:
            response["shortened_urls"][str(shortenedURL.id)] = {'long_url': shortenedURL.longURL, 'short_url': shortenedURL.shortURL, 'clicks': shortenedURL.clicks, 'created': shortenedURL.created, 'is_vanity': shortenedURL.isVanity}

        return JsonResponse(response)

    else:
        return JsonResponse({'error': 'Request is not type GET'}, status = 400)

def api_root_endpoint(request):

    return JsonResponse({'error': 'No endpoint was provided', 'available_endpoints': ['/create?long=<long_url>', '/vanity?auth=<auth_token>&long=<long_url>', '/stats/<short_url>', '/all?auth=<auth_token>']})