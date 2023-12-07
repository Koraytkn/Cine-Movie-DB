from django.shortcuts import render
from django.db import connection
from datetime import datetime
# Create your views here.

def auth_manager(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM db_manager WHERE username = %s AND password = %s", (request['username'], request['password']))
    manager = cursor.fetchone()
    if manager is None:
        return False
    return True

def auth_director(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM director WHERE username = %s AND password = %s", (request['username'], request['password']))
    director = cursor.fetchone()
    cursor.execute("SELECT * FROM experienced_director WHERE username = %s AND password = %s", (request['username'], request['password']))
    experienced_director = cursor.fetchone()
    if director is None and experienced_director is None:
        return False
    return True

def auth_audience(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM audience WHERE username = %s AND password = %s", (request['username'], request['password']))
    audience = cursor.fetchone()
    if audience is None:
        return False
    return True

def add_new_audience(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM audience WHERE username = %s", (request['username'],))

    audience = cursor.fetchone()
    if request['username'] == "" or request['password'] == "" or request['name'] == "" or request['surname'] == "":
        return False
    elif audience is not None:
        return False
    cursor.execute("INSERT INTO audience (name, surname, password, username) VALUES (%s, %s, %s, %s)", (request['name'], request['surname'], request['password'], request['username']))
    return True

    
def add_new_director(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM director WHERE username = %s", (request['username'],))

    director = cursor.fetchone()
    if request['username'] == "" or request['password'] == "" or request['name'] == "" or request['surname'] == "" or request['nation'] == "":
        return False
    elif director is not None:
        return False
    
    if request['platform'] is not None and request['platform'] != "" and request['platform'].isnumeric():
        cursor.execute("INSERT INTO experienced_director (name, surname, password, username, nation) VALUES (%s, %s, %s, %s, %s)", (request['name'], request['surname'], request['password'], request['username'], request['nation']))
        cursor.execute("INSERT INTO contract (username, platform_id) VALUES (%s, %s)", (request['username'], request['platform']))
    else:
        cursor.execute("INSERT INTO director (name, surname, password, username, nation) VALUES (%s, %s, %s, %s, %s)", (request['name'], request['surname'], request['password'], request['username'], request['nation']))
    
    return True

def update_director_platform(request):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM director WHERE username = %s", (request['username'],))
    if cursor.fetchone() is not None:           # if director is not experienced yet, director does not have a platform/contract.
        cursor.execute("INSERT INTO experienced_director (name, surname, password, username, nation) SELECT name, surname, password, username, nation FROM director WHERE username = %s", (request['username'],))
        cursor.execute("DELETE FROM director WHERE username = %s", (request['username'],))
        cursor.execute("INSERT INTO contract (username, platform_id) VALUES (%s, %s)", (request['username'], request['platform_id']))
    else:                                       # if director is experienced, has platform/contract
        cursor.execute("SELECT * FROM experienced_director WHERE username = %s", (request['username'],))
        if cursor.fetchone() is not None:
            cursor.execute("UPDATE contract SET platform_id = %s WHERE username = %s", (request['platform_id'], request['username']))
        else:
            return False
    rows_updated = cursor.rowcount
    return rows_updated > 0


def list_directors(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM director")
    raw_directors = cursor.fetchall()
    dict_directors = []
    for director in raw_directors:
        dict_director = {}
        dict_director['name'] = director[0]
        dict_director['surname'] = director[1]
        dict_director['nation'] = director[4]
        dict_director['username'] = director[3]
        dict_director['platform_id'] = None
        dict_directors.append(dict_director)
    cursor.execute("SELECT * FROM experienced_director")
    raw_directors = cursor.fetchall()
    for director in raw_directors:
        dict_director = {}
        dict_director['name'] = director[0]
        dict_director['surname'] = director[1]
        dict_director['nation'] = director[4]
        dict_director['username'] = director[3]
        cursor.execute("SELECT platform_id FROM contract WHERE username = %s", (director[3],))
        platform_id = cursor.fetchone()
       # print(platform_id)
        dict_director['platform_id'] = platform_id[0]
        dict_directors.append(dict_director)
    return dict_directors

def list_director_movies(request):
    director = request['director']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM directed_by WHERE username = %s ORDER BY movie_id", (director,))
    raw_movies = cursor.fetchall()
    dict_movies = []
    for movie in raw_movies:
        # create a new dictionary on each iteration
        dict_movie = {}
        dict_movie['movie_id'] = movie[0]
        cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (movie[0],))
        raw_movie = cursor.fetchone()
        dict_movie['duration'] = raw_movie[1]
        dict_movie['movie_name'] = raw_movie[2]
        cursor.execute("SELECT * FROM in_session WHERE movie_id = %s", (movie[0],))
        raw_sessions = cursor.fetchall()
        for session in raw_sessions:
            # create a new dictionary on each iteration
            session_movie = dict_movie.copy()
            session_movie['date'] = session[2]
            session_movie['time_slot'] = session[3]
            session_movie['theater_id'] = session[4]
            cursor.execute("SELECT theater_district FROM theater WHERE theater_id = %s", (session[4],))
            theater_district = cursor.fetchone()
            session_movie['theater_district'] = theater_district[0]
            dict_movies.append(session_movie)
    return dict_movies

def list_audience_ratings(request):
    audience = request['audience']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM review WHERE subscribed_audience = %s", (audience,))
    raw_reviews = cursor.fetchall()
    # movie_id movie_name rating will be added to dict_reviews
    dict_reviews = []
    for review in raw_reviews:
        # create a new dictionary on each iteration
        dict_review = {}
        dict_review['movie_id'] = review[3]
        cursor.execute("SELECT movie_name FROM movie WHERE movie_id = %s", (review[3],))
        movie_name = cursor.fetchone()
        dict_review['movie_name'] = movie_name[0]
        dict_review['rating'] = review[0]
        dict_reviews.append(dict_review)
    return dict_reviews

def remove_audience(request):
    removed_audience = request['username']
    #audience must be deleted including the list of tickets for movie sessions and the list of rating platforms to which they are subscribed.
    cursor = connection.cursor()
    cursor.execute("DELETE FROM audience WHERE username = %s", (removed_audience,))
    rows_updated = cursor.rowcount
    return rows_updated > 0

def list_movie_rating(request):
    movie_id = request['movie_id']
    cursor = connection.cursor()
     # movie_id movie_name average rating will be added to dict_reviews
    dict_reviews = []
    dict_review = {}
    dict_review['movie_id'] = movie_id
    cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    movie_info = cursor.fetchone()
    dict_review['movie_name'] = movie_info[2]
    dict_review['rating'] = movie_info[3]
    dict_reviews.append(dict_review)
    return dict_reviews
   
    



def list_theaters(request):
    date = request['date']
    time_slot = request['time_slot']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM theater")
    all_theaters = cursor.fetchall()
    available_theaters = []
    for theater in all_theaters:
        available_theater = {}
        cursor.execute("SELECT * FROM in_host WHERE theater_id = %s AND date = %s AND time_slot = %s", (theater[0], date, time_slot))
        x = cursor.fetchone()
        print(x)
        if x is None:
            available_theater['theater_id'] = theater[0]
            available_theater['theater_name'] = theater[1]
            available_theater['theater_capacity'] = theater[2]
            available_theater['theater_district'] = theater[3]
            available_theaters.append(available_theater)
    return available_theaters

def add_theater(request):
    director = request['director']
    theater_id = request['theater_id']
    theater_name = request['theater_name']
    theater_capacity = request['theater_capacity']
    theater_district = request['theater_district']

    cursor = connection.cursor()
    if theater_id == "" or theater_name == "" or theater_capacity == "" or theater_district == "":
        return False
    cursor.execute("SELECT * FROM experienced_director WHERE username = %s", (director,))
    if cursor.fetchone() is  None:
        return False
    cursor.execute("SELECT * FROM theater WHERE theater_id = %s", (theater_id,))
    if cursor.fetchone() is not None:
        return False
    cursor.execute("INSERT INTO theater VALUES (%s, %s, %s, %s)", (theater_id, theater_name, theater_capacity, theater_district))
    return True

def add_movie_session(request):
    director = request['director']
    #print("here", director)
    movie_id = request['movie_id']
    movie_name = request['movie_name']
    theater_id = request['theater_id']
    date = request['date']
    time_slot = request['time_slot']
    duration = request['duration']

    cursor = connection.cursor()
    if movie_id == "" or movie_name == "" or theater_id == "" or date == "" or time_slot == "" or duration == "":
        return False
    if(int(duration) + int(time_slot) > 5):
        return False
    cursor.execute("SELECT * FROM experienced_director WHERE username = %s", (director,))
    if cursor.fetchone() is  None:
        return False

    cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    if cursor.fetchone() is  None:
        cursor.execute("INSERT INTO movie (movie_id, duration, movie_name, average_rating) VALUES (%s, %s, %s,%s)", (movie_id, duration, movie_name, 0))
        cursor.execute("INSERT INTO directed_by (movie_id, username) VALUES (%s, %s)", (movie_id, director))
    
    time_slot_counter = int(time_slot)
    duration_counter = int(duration)
    while(duration_counter > 0):
        cursor.execute("SELECT * FROM movie_session WHERE date = %s AND time_slot = %s", (date, time_slot_counter))
        if cursor.fetchone() is  None:
            cursor.execute("INSERT INTO movie_session (date, time_slot) VALUES (%s, %s)", (date, time_slot_counter))

        cursor.execute("SELECT * FROM in_host WHERE theater_id = %s AND date = %s AND time_slot = %s", (theater_id, date, time_slot_counter))
        if cursor.fetchone() is not None:
            return False
        cursor.execute("INSERT INTO in_host (date, time_slot, theater_id) VALUES (%s, %s, %s)", (date, time_slot_counter, theater_id))
        duration_counter -= 1
        time_slot_counter += 1

    cursor.execute("SELECT COUNT(*) FROM in_session")
    session_id = cursor.fetchone()
    cursor.execute("INSERT INTO in_session (movie_id, session_id, date, time_slot, theater_id) VALUES (%s, %s, %s, %s, %s)", (movie_id, session_id, date, time_slot, theater_id))

    return True

def add_genre(request):
    director = request['director']
    movie_id = request['movie_id']
    genre_name = request['genre_name']
    cursor = connection.cursor()
    if movie_id == "" or genre_name == "":
        return False
    cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    if cursor.fetchone() is None:
        return False
    cursor.execute("SELECT * FROM directed_by WHERE movie_id = %s AND username = %s", (movie_id, director))
    if cursor.fetchone() is None:
        return False
    cursor.execute("SELECT * FROM genre WHERE genre_name = %s", (genre_name,))
    if cursor.fetchone() is None:
        return False
    cursor.execute("INSERT INTO which_genre (movie_id, genre_name) VALUES (%s, %s)", (movie_id, genre_name))
    return True

def add_predecessor_movie(request):
    director = request['director']
    child_movie_id = request['child_movie_id']
    predecessor_movie_id = request['predecessor_movie_id']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (child_movie_id,))
    if cursor.fetchone() is None:
        return False
    cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (predecessor_movie_id,))
    if cursor.fetchone() is None:
        return False
    cursor.execute("SELECT * FROM directed_by WHERE movie_id = %s AND username = %s", (child_movie_id, director))
    if cursor.fetchone() is None:
        return False
    cursor.execute("SELECT * FROM directed_by WHERE movie_id = %s AND username = %s", (predecessor_movie_id, director))
    if cursor.fetchone() is None:
        return False
    cursor.execute("INSERT INTO preceded (child_movie_id, predecessor_movie_id) VALUES (%s, %s)", (child_movie_id, predecessor_movie_id))  
    return True

def list_my_movies(request):
    director = request['director']
    #print("here",director)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM directed_by WHERE username = %s ORDER BY movie_id", (director,))
    raw_movies = cursor.fetchall()
    dict_movies = []
    for movie in raw_movies:
        # create a new dictionary on each iteration
        dict_movie = {}
        dict_movie['movie_id'] = movie[0]
        cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (movie[0],))
        raw_movie = cursor.fetchone()
        dict_movie['duration'] = raw_movie[1]
        dict_movie['movie_name'] = raw_movie[2]
        cursor.execute("SELECT * FROM which_genre WHERE movie_id = %s", (movie[0],))
        raw_genres = cursor.fetchall()
        genre_list = ""
        for genre in raw_genres:
            genre_list += str(genre[1]) + ", "
        dict_movie['genre_list'] = genre_list
        cursor.execute("SELECT * FROM in_session WHERE movie_id = %s", (movie[0],))
        raw_sessions = cursor.fetchall()
        for session in raw_sessions:
            # create a new dictionary on each iteration
            session_movie = dict_movie.copy()
            session_movie['date'] = session[2]
            session_movie['time_slot'] = session[3]
            session_movie['theater_id'] = session[4]
            cursor.execute("SELECT predecessor_movie_id FROM preceded WHERE child_movie_id = %s", (movie[0],))
            predecessor_list = ""
            raw_predecessors = cursor.fetchall()
            for predecessor in raw_predecessors:
                predecessor_list += str(predecessor[0]) + ", "
            session_movie['predecessor_list'] = predecessor_list
            dict_movies.append(session_movie)
    return dict_movies

def update_movie_name(request):
    director = request['director']
    movie_id = request['movie_id']
    movie_name = request['movie_name']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    if cursor.fetchone() is None:
        return False
    cursor.execute("SELECT * FROM directed_by WHERE movie_id = %s AND username = %s", (movie_id, director))
    if cursor.fetchone() is None:
        return False
    cursor.execute("UPDATE movie SET movie_name = %s WHERE movie_id = %s", (movie_name, movie_id))
    return True

def list_the_audience(request):
    director = request['director']
    movie_id = request['movie_id']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    if cursor.fetchone() is None:
        return []
    cursor.execute("SELECT * FROM directed_by WHERE movie_id = %s AND username = %s", (movie_id, director))
    if cursor.fetchone() is None:
        return []
    cursor.execute("SELECT session_id FROM in_session WHERE movie_id = %s", (movie_id,))
    raw_sessions = cursor.fetchall()
    dict_audience = []
    for session in raw_sessions:
        # create a new dictionary on each iteration
        # username, name, surname added from audience table, where session is checked from ticket table.
        cursor.execute("SELECT purchaser FROM ticket WHERE session_id = %s", (session[0],))
        raw_audience = cursor.fetchall()
        for audience in raw_audience:
            each_audience = {}
            cursor.execute("SELECT name, surname FROM audience WHERE username = %s", (audience[0],))
            raw_name = cursor.fetchone()
            each_audience['username'] = audience[0]
            each_audience['name'] = raw_name[0]
            each_audience['surname'] = raw_name[1]
            #check if the audience already exists in the list
            if each_audience not in dict_audience:
                dict_audience.append(each_audience)
    return dict_audience
    





def list_all_movies(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movie ORDER BY movie_id")
    raw_movies = cursor.fetchall()
    dict_movies = []
    for movie in raw_movies:
        # create a new dictionary on each iteration
        dict_movie = {}
        dict_movie['movie_id'] = movie[0]
        dict_movie['duration'] = movie[1]
        dict_movie['movie_name'] = movie[2]
        cursor.execute("SELECT username FROM directed_by WHERE movie_id = %s", (movie[0],))
        raw_directors = cursor.fetchone()
        cursor.execute("SELECT surname FROM experienced_director WHERE username = %s", (raw_directors[0],))
        raw_directors = cursor.fetchone()
        dict_movie['director_surname'] = raw_directors[0]
        cursor.execute("SELECT * FROM which_genre WHERE movie_id = %s", (movie[0],))
        raw_genres = cursor.fetchall()
        genre_list = ""
        for genre in raw_genres:
            genre_list += str(genre[1]) + ", "
        dict_movie['genre_list'] = genre_list
        cursor.execute("SELECT * FROM in_session WHERE movie_id = %s", (movie[0],))
        raw_sessions = cursor.fetchall()
        for session in raw_sessions:
            # create a new dictionary on each iteration
            session_movie = dict_movie.copy()
            session_movie['date'] = session[2]
            session_movie['time_slot'] = session[3]
            session_movie['theater_id'] = session[4]
            cursor.execute("SELECT predecessor_movie_id FROM preceded WHERE child_movie_id = %s", (movie[0],))
            predecessor_list = ""
            raw_predecessors = cursor.fetchall()
            for predecessor in raw_predecessors:
                predecessor_list += str(predecessor[0]) + ", "
            session_movie['predecessor_list'] = predecessor_list
            dict_movies.append(session_movie)
    return dict_movies

def purchase_ticket(request):
    session_id = request['session_id']
    username = request['audience']
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM in_session WHERE session_id = %s", (session_id,))
    movie = cursor.fetchone()
    if movie is None:
        
        return False
    movie_id = movie[0]
    
    cursor.execute("SELECT * FROM ticket WHERE session_id = %s AND purchaser = %s", (session_id, username))
    if cursor.fetchone() is not None:
        
        return False
    
    # To buy a ticket to a movie all predecessors must be watched
    cursor.execute("SELECT predecessor_movie_id FROM preceded WHERE child_movie_id = %s", (movie_id,))
    raw_predecessors = cursor.fetchall()
    for predecessor in raw_predecessors:
        cursor.execute("SELECT * FROM ticket WHERE movie_id = %s AND purchaser = %s", (predecessor[0], username))
        if cursor.fetchone() is None:
            print("here", username)
            return False
        
    #Audience can not buy a ticket if the theater capacity is full
    cursor.execute("SELECT theater_capacity FROM theater WHERE theater_id = %s", (movie[4],))
    capacity = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ticket WHERE session_id = %s", (session_id,))
    ticket_count = cursor.fetchone()[0]
    if ticket_count >= capacity:
        return False
    
    
    cursor.execute("SELECT COUNT(*) FROM ticket")
    ticket_no = cursor.fetchone()[0]
    cursor.execute("INSERT INTO ticket (ticket_no, purchaser , session_id, movie_id ) VALUES (%s, %s, %s, %s)", (ticket_no, username, session_id, movie_id))
    return True


def list_my_tickets(request):
    username = request['audience']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ticket WHERE purchaser = %s", (username,))
    raw_tickets = cursor.fetchall()
    dict_tickets = []
    for ticket in raw_tickets:
        # create a new dictionary on each iteration
        # Need to add movie_name, movie_id, session id, rating, overall rating
        dict_ticket = {}
        cursor.execute("SELECT movie_name FROM movie WHERE movie_id = %s", (ticket[3],))
        raw_movie_name = cursor.fetchone()
        dict_ticket['movie_name'] = raw_movie_name[0]
        dict_ticket['movie_id'] = ticket[3]
        dict_ticket['session_id'] = ticket[2]
        # if the session date hasn't passed yet, the rating is set to None
        cursor.execute("SELECT date FROM in_session WHERE session_id = %s", (ticket[2],))
        raw_date = cursor.fetchone()
        date_from_db = datetime.strptime(raw_date[0], '%d/%m/%Y').date()
        if date_from_db > datetime.now().date():
            dict_ticket['my_rating'] = None
        else:
            cursor.execute("SELECT rating from review WHERE subscribed_audience = %s AND movie_id = %s", (username, ticket[3]))
            raw_rating = cursor.fetchone()
            if raw_rating is None:
                dict_ticket['my_rating'] = None
            else:
                dict_ticket['my_rating'] = raw_rating[0]
        cursor.execute("SELECT average_rating FROM movie WHERE movie_id = %s", (ticket[3],))
        raw_overall_rating = cursor.fetchone()
        print("here", ticket[3])
        print("hereee", raw_overall_rating)
        if raw_overall_rating[0] is None:
            dict_ticket['overall_rating'] = None
        else:
            dict_ticket['overall_rating'] = raw_overall_rating[0]
        dict_tickets.append(dict_ticket)
    return dict_tickets

def subscribe_rating_platform(request):
    username = request['audience']
    platform_id = request['platform_id']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM rating_platform WHERE platform_id = %s", (platform_id,))
    if cursor.fetchone() is None:
        return False
    cursor.execute("SELECT * FROM subscribe WHERE audience_username = %s AND platform_id = %s", (username, platform_id))
    if cursor.fetchone() is not None:
        return False
    cursor.execute("INSERT INTO subscribe (audience_username, platform_id) VALUES (%s, %s)", (username, platform_id))
    return True

def rate_movie(request):
    username = request['audience']
    movie_id = request['movie_id']
    rating = request['rating']
    cursor = connection.cursor()

    # if the movie is not in the database, return false
    cursor.execute("SELECT * FROM movie WHERE movie_id = %s", (movie_id,))
    if cursor.fetchone() is None:
        return False
    
    # if the rating is not a float between 0 and 5, return false
    rating = float(rating)
    if rating < 0 or rating > 5:
        return False
    
    # if the audience has already rated the movie, return false
    cursor.execute("SELECT * FROM review WHERE subscribed_audience = %s AND movie_id = %s", (username, movie_id))
    if cursor.fetchone() is not None:
        return False
    
    # if the audience has not bought a ticket to the movie, return false
    cursor.execute("SELECT * FROM ticket WHERE purchaser = %s AND movie_id = %s", (username, movie_id))
    tickets = cursor.fetchall()
    if tickets is None:
        return False
    
    # if the audience has not subscribed to the rating platform, return false
    cursor.execute("SELECT username FROM directed_by WHERE movie_id = %s", (movie_id,))
    director_username = cursor.fetchone()[0]
    cursor.execute("SELECT platform_id FROM contract WHERE username = %s", (director_username,))
    platform_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM subscribe WHERE audience_username = %s AND platform_id = %s", (username, platform_id))
    if cursor.fetchone() is None:
        return False

    # if the movie has not been watched yet, return false
    ticket_no = None
    watched = False
    for ticket in tickets:
        session_id = ticket[2]
        cursor.execute("SELECT date FROM in_session WHERE session_id = %s", (session_id,))
        raw_date = cursor.fetchone()
        date_from_db = datetime.strptime(raw_date[0], '%d/%m/%Y').date()
        if date_from_db < datetime.now().date():
            watched = True
            ticket_no = ticket[0]
            break
    if not watched:
        return False

    # if the rating is valid, insert it into the database
    cursor.execute("INSERT INTO review (rating, ticket_no, subscribed_audience, movie_id, reviewer_platform_id) VALUES (%s, %s, %s, %s, %s)", (rating, ticket_no, username, movie_id, platform_id))
    return True
