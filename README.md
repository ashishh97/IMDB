# IMDB
imdb to search, add, delete, edit movies and its details 

Signup (POST): ashishh87.pythonanywhere.com/login/create_user/ 
Request body: {
    "first_name": "Ashish",
    "last_name": "Kumar",
    "email": "ashish@gmail.com",
    "password": "1234",
    "user_type": "admin"
}

Login (POST) : ashishh87.pythonanywhere.com/login/
Request body: {
    "email": "ashish@gmail.com",
    "password": "1234"

}



To add movies(POST) (multiple movies can be added at a time): ashishh87.pythonanywhere.com/api/add_movies/

Request body : [{
    "99popularity": 83.0,
    "director": "Victor Fleming",
    "genre": [
      "Adventure",
      " Family",
      " Fantasy",
      " Musical"
    ],
    "imdb_score": 8.3,
    "name": "The Wizard of Oz"
  }]
  
  To edit movies(PUT)(one movie at a time): ashishh87.pythonanywhere.com/api/edit_movie/
     Request body: {
    "director": "George Lucas",
    "imdb_score": 9.8,
    "name": "Star Wars"
  }
  
  
  To delete movies(DELETE)(one movie at a time) : ashishh87.pythonanywhere.com/api/delete_movies/
  Request body :{
    "name":"Vertigo"
}


To search movie details using movie names(GET): ashishh87.pythonanywhere.com/api/?search=The Wizard of Oz

