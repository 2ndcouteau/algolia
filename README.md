# **Algolia**

Hello, welcome on the Algolia Test exercise.


### Install and Run the app

#### Requirement
You need **docker** to use the app

#### Build the docker image
`docker build --tag algolia-test .`

#### Run the app
`docker run -d -p 5000:5000 algolia-test`

By default, the container is doing so in isolation mode and cannot connect to localhost:5000.
So we use a redirection port to access the app `-p 5000:5000`

#### DB preparation

By defaut, you have to build the DB.
To do that, you just have to make a POST on the following url:
```
curl -X POST localhost:5000/initDB
```

This call will:
(/) - Removes the proprerty actor_facets
(/) - Change the score to have only 2 decimals.
(/) - Normalize the `actors` into a separate table/collections
(/) - Store the data in sqlite DB as source of truth
(/) - Synchronize this source of truth with an Algolia index


#### Movie Requests

() POST /api/v1/movies
() PUT /api/v1/movies
() DELETE /api/v1/movies


Post a new movie:
```
curl http://127.0.0.1:5000/api/v1/movies -H "Content-Type: application/json" --data '{"title":"Matrix","year":"1998", "actors":["Toto", "John", "Algolia"]}'
```
Note that the `title` and `year` are required. This give us a way to assume the unicity of movies in the DB.


This call will return the MovieId
```
{
    'Message': "Creation success",
    "MovieId": "440712661"
}
```



Put/update a movie:
```
curl -X PUT http://127.0.0.1:5000/api/v1/movies -H "Content-Type: application/json" --data '{"MovieId":"440712661","year":"1999", "actors":["Keanu Reeve",]}'
```

The MovieId is required.

