from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from query.views import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.
director_name = ""
audience_name = ""

def home(request):
    return render(request, "pages/home.html")

@csrf_exempt
def manager_login(request):
    # warning will be used to warn the user if the credentials are invaild or for any other warning
    context = {'page': 'Sign In', 'warning': ""}

    if request.method == "POST":  # if the sign in button clicked
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        auth_request = {'username': username, 'password': password}
        if auth_manager(auth_request):
            return redirect("/manager/")
        else:
            context['warning'] = "Invalid credentials"
    
    return render(request, "pages/manager-login.html", context)

@csrf_exempt
def director_login(request):
    global director_name
    # warning will be used to warn the user if the credentials are invaild or for any other warning
    context = {'page': 'Sign In', 'warning': ""}

    if request.method == "POST": # if the sign in button clicked
        username = request.POST.get("username")
        password = request.POST.get("password")

        auth_request = {'username': username, 'password': password}
        if auth_director(auth_request):
            director_name = username
            #response['username'] = username  # Pass the username as a header
            return redirect("/director/")
        else:
            context['warning'] = "Invalid credentials"
    
    return render(request, "pages/director-login.html", context)

@csrf_exempt
def manager(request):
     if request.method == "POST":
        if 'Add Audience' in request.POST:
          name = request.POST.get("name")
          surname = request.POST.get("surname")
          password = request.POST.get("password")
          username = request.POST.get("username")

            # Add validation and error handling here

          add_audience_request = {'username': username, 'password': password, 'name': name, 'surname': surname}
          if(add_new_audience(add_audience_request)):
            messages.success(request, "Audience added successfully")  # Add this line
            return redirect('manager')
          else:
            messages.error(request, "Audience could not be added")  # Add this line
            return redirect('manager')
          
        elif 'Add Director' in request.POST:
            director_name = request.POST.get("director_name")
            director_surname = request.POST.get("director_surname")
            director_password = request.POST.get("director_password")
            director_username = request.POST.get("director_username")
            director_nation = request.POST.get("director_nation")
            director_platform = request.POST.get("director_platform")

            add_director_request = {'username': director_username, 'password': director_password, 'name': director_name, 'surname': director_surname, 'nation': director_nation, 'platform': director_platform}
            if(add_new_director(add_director_request)):
                messages.success(request, "Director added successfully")
                return redirect('manager')
            else:
                messages.error(request, "Director could not be added")
                return redirect('manager')
        
        elif 'Update Director Platform' in request.POST:
            director_username = request.POST.get("director_username")
            director_platform_id = request.POST.get("director_platform_id")

            update_director_platform_request = {'username': director_username, 'platform_id': director_platform_id}
            if update_director_platform(update_director_platform_request):
              messages.success(request, "Director's platform id updated successfully")
            else:
              messages.error(request, "Director's platform id could not be updated")

        elif 'View All Directors' in request.POST:
            directors = list_directors(request)
            context = {'page': 'manager', 'directors': directors}
            return render(request, "pages/manager.html", context)
        
        elif 'View Director\'s Movies' in request.POST:
            director_username = request.POST.get("director_username")
            list_director_movies_request = {'director': director_username}
            director_movies = list_director_movies(list_director_movies_request)
            context = {'page': 'manager', 'movies': director_movies}
            return render(request, "pages/manager.html", context)
        
        elif 'View Audience Ratings' in request.POST:
            audience_username = request.POST.get("audience_username")
            list_audience_ratings_request = {'audience': audience_username}
            audience_ratings = list_audience_ratings(list_audience_ratings_request)
            context = {'page': 'manager', 'ratings': audience_ratings}
            return render(request, "pages/manager.html", context)
        elif 'Remove Audience' in request.POST:
            removed_audience_username = request.POST.get("audience_username")
            remove_audience_request = {'username': removed_audience_username}
            if remove_audience(remove_audience_request):
                messages.success(request, "Audience removed successfully")
            else:
                messages.error(request, "Audience could not be removed")
        elif 'View Movie Rating' in request.POST:
            movie_id = request.POST.get("movie_id")
            list_movie_rating_request = {'movie_id': movie_id}
            movie_ratings = list_movie_rating(list_movie_rating_request)
            context = {'page': 'manager', 'movie_ratings': movie_ratings}
            return render(request, "pages/manager.html", context)


     return render(request, "pages/manager.html")

@csrf_exempt
def director(request):
    global director_name
    username = director_name
    if request.method == "POST":
        if 'List Available Theaters' in request.POST:
            date = request.POST.get("date")
            slot = request.POST.get("time_slot")
            list_theaters_request = {'date': date, 'time_slot': slot}
            theaters = list_theaters(list_theaters_request)
            context = {'page': 'director', 'theaters': theaters}
            return render(request, "pages/director.html", context)
        elif 'Add Theater' in request.POST:
            theater_id = request.POST.get("theater_id")
            theater_name = request.POST.get("theater_name")
            theater_capacity = request.POST.get("theater_capacity")
            theater_district = request.POST.get("theater_district")
            add_theater_request = {'theater_id': theater_id, 'theater_name': theater_name, 'theater_capacity': theater_capacity, 'theater_district': theater_district, 'director': username}
            if add_theater(add_theater_request):
                messages.success(request, "Theater added successfully")
            else:
                messages.error(request, "Theater could not be added")
        elif 'Add Movie Session' in request.POST:
            movie_id = request.POST.get("movie_id")
            movie_name = request.POST.get("movie_name")
            theater_id = request.POST.get("theater_id")
            date = request.POST.get("date")
            slot = request.POST.get("time_slot")
            duration = request.POST.get("duration")
            add_movie_session_request = {'movie_id': movie_id, 'movie_name': movie_name, 'theater_id': theater_id, 'date': date, 'time_slot': slot, 'duration': duration, 'director': username}
            if add_movie_session(add_movie_session_request):
                messages.success(request, "Movie session added successfully")
            else:
                messages.error(request, "Movie session could not be added")
        elif 'Add Predecessor Movie' in request.POST:
            child_movie_id = request.POST.get("child_movie_id")
            predecessor_movie_id = request.POST.get("predecessor_movie_id")
            add_predecessor_movie_request = {'child_movie_id': child_movie_id, 'predecessor_movie_id': predecessor_movie_id, 'director': username}
            if add_predecessor_movie(add_predecessor_movie_request):
                messages.success(request, "Predecessor movie added successfully")
            else:
                messages.error(request, "Predecessor movie could not be added")
        elif 'Add Genre to Movie' in request.POST:
            movie_id = request.POST.get("movie_id")
            genre_name = request.POST.get("genre_name")
            add_genre_request = {'movie_id': movie_id, 'genre_name': genre_name, 'director': username}
            if add_genre(add_genre_request):
                messages.success(request, "Genre added successfully")
            else:
                messages.error(request, "Genre could not be added")
        elif 'List My Movies' in request.POST:
            list_movies_request = {'director': username}
            movies = list_my_movies(list_movies_request)
            context = {'page': 'director', 'movies': movies}
            return render(request, "pages/director.html", context)
        elif 'Update Movie Name' in request.POST:
            updated_movie_id = request.POST.get("movie_id")
            updated_movie_name = request.POST.get("new_movie_name")
            update_movie_name_request = {'movie_id': updated_movie_id, 'movie_name': updated_movie_name, 'director': username}
            if update_movie_name(update_movie_name_request):
                messages.success(request, "Movie name updated successfully")
            else:
                messages.error(request, "Movie name could not be updated")
        elif 'List The Audience' in request.POST:
            movie_id = request.POST.get("movie_id")
            list_audience_request = {'movie_id': movie_id, 'director': username}
            audience = list_the_audience(list_audience_request)
            context = {'page': 'director', 'audience_list': audience}
            return render(request, "pages/director.html", context)

    return render(request, "pages/director.html")

@csrf_exempt
def audience(request):
    global audience_name
    if request.method == "POST": 
        if 'List All Movies' in request.POST:
            movies = list_all_movies(request)
            context = {'page': 'audience', 'movies': movies}
            return render(request, "pages/audience.html", context)
        elif 'Purchase Movie Ticket' in request.POST:
            session_id = request.POST.get("session_id")
            purchase_ticket_request = {'session_id': session_id, 'audience': audience_name}
            if purchase_ticket(purchase_ticket_request):
                messages.success(request, "Ticket purchased successfully")
            else:
                messages.error(request, "Ticket could not be purchased")
        elif 'List My Tickets' in request.POST:
            list_tickets_request = {'audience': audience_name}
            tickets = list_my_tickets(list_tickets_request)
            context = {'page': 'audience', 'tickets': tickets}
            return render(request, "pages/audience.html", context)
        elif 'Subscribe to Rating Platform' in request.POST:
            platform_id = request.POST.get("platform_id")
            #print(platform_id, " ", audience_name)
            subscribe_rating_platform_request = {'platform_id': platform_id, 'audience': audience_name}
            if subscribe_rating_platform(subscribe_rating_platform_request):
                messages.success(request, "Subscribed successfully")
            else:
                messages.error(request, "Could not subscribe")
        elif 'Rate a Movie' in request.POST:
            movie_id = request.POST.get("movie_id")
            rating = request.POST.get("rating")
            rate_movie_request = {'movie_id': movie_id, 'rating': rating, 'audience': audience_name}
            if rate_movie(rate_movie_request):
                messages.success(request, "Rated successfully")
            else:
                messages.error(request, "Could not rate")

    return render(request, "pages/audience.html")

@csrf_exempt
def audience_login(request):
    global audience_name
    # warning will be used to warn the user if the credentials are invaild or for any other warning
    context = {'page': 'Sign In', 'warning': ""}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        auth_request = {'username': username, 'password': password}
        if auth_audience(auth_request):
            audience_name = username
            return redirect("/audience/")
        else:
            context['warning'] = "Invalid credentials"

    return render(request, "pages/audience-login.html", context)

from django.views.decorators.csrf import csrf_exempt


   
