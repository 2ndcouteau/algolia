# **Algolia**

Hello, welcome on the Algolia Test exercise.

---

## **Install and Run the app**

### **Requirement**
You need **docker** to use the app

### **Build the docker image**
`docker build --tag algolia-test .`

### **Run the app**
`docker run -d -p 5000:5000 algolia-test`

By default, the container is doing so in isolation mode and cannot connect to localhost:5000.
So we use a redirection port to access the app `-p 5000:5000`

---

## **Usage**

### **DB preparation**

By defaut, you have to build the DB.
To do that, you just have to make a POST on the following url:
```
curl -X POST localhost:5000/initDB
```

This call will:
* (/) - Removes the proprerty actor_facets
* (/) - Change the score to have only 2 decimals.
* (/) - Normalize the `actors` into a separate table/collections
* (/) - Store the data in sqlite DB as source of truth
* (/) - Synchronize this source of truth with an Algolia index

---

### **Movie Requests**

* (/) POST /api/v1/movies
* (/) PUT /api/v1/movies/movieId
* (/) DELETE /api/v1/movies/movieId


#### **Post a new movie:**
```
curl -L http://127.0.0.1:5000/api/v1/movies -H "Content-Type: application/json" --data '{"title":"Matrix","year":"1998", "actors":["Toto", "John", "Algolia"]}'
```
Note that the `title` and `year` are required. This give us a way to assume the unicity of movies in the DB.
Also, here we use the -L option of curl to follow the redirection automatically


The request will expect the following json data structure:
```
{
    "title": "title",  // Not optionnal
    "year": "year",  // Not optionnal
    "image": "image",
    "color": "color",
    "score": "score",
    "rating": "rating",
    "actors": ["actor 1", "actor 2", ...],
    "alternative_titles": ["title 1", "title 2", "title 3", ...],
    "genre": ["genre 1", "genre 2", "genre 3", ...],
}
```
Note that for "actors", "alternative_titles" and "genre" you can pass a simple value instead of a list:
```
"actors": "Actor Unique",
```

This call will return the movieId and a message.
```
{
    'Message': "Creation success",
    "movieId": "440712661"
}
```



#### **Put/update a movie** :
```
curl -X PUT http://127.0.0.1:5000/api/v1/movies/440712661 -H "Content-Type: application/json" --data '{"title":"Matrix Reloaded","year":"2002","score":"4", "actors":["Laurence Fishburn", "Keanue Reeves"]}'
```
The movieId is required in the url path and this time, any other params are **optionnal**.

The request will expect the following json data structure:
```
{
    "title": "title",
    "year": "year",
    "image": "image",
    "color": "color",
    "score": "score",
    "rating": "rating",
    "actors": ["actor 1", "actor 2", ...],
    "alternative_titles": ["title 1", "title 2", "title 3", ...],
    "genre": ["genre 1", "genre 2", "genre 3", ...],
}
```
Note that for "actors", "alternative_titles" and "genre" you can pass a simple value instead of a list:
```
"actors": "Actor Unique",
```



#### **Delete a movie** :
```
curl -X DELETE http://127.0.0.1:5000/api/v1/movies/440712661
```
The movieId is required in the url path


---


## **Perspectives and evolutions**


So for now, the app respect the subject requirements
But we could still improve the project

### - On a ops perspective:

- Create a way to get metrics and logs about the the app itself.
- Add a complete CI/CD


### - On a code perspective:
- Add a log function with level of log

Logs could be formated as followed:

`[Date Hours] [Unique Token] [Level Log] : Message`

Logs should offer the capacity to print the log and to save them in a specific file

We should also be able to set a log level by default to avoid to much verbose logs output

Levels could be (in order of priority): `[ERR_TRACE, WARN_TRACE, ERR, WARN, INFO, DEBUG, TRACE, LOG]`

All these logs could be sent to **Elasticsearch** to facilitate log mining and create alert triggers.


### - On data perspective:
- Use postgreSQL instead of sqlite as a DB


### - On Code perspective:
- Use Swagger to write the spec of the API and fix a source of truth for the API design
This will offer a clear Documentation
- Add a way to manage secrets - eg: Algolia TokenAPI
- Add unit tests and integration tests with Postman


## **Development worflow**

I started by working on the use of Flask which I didn't know very well.

I decided to integrate the whole application in a Docker for the comfort of the testers.

Then I started testing the data transformation. These steps were done quickly.

I used a new table to normalize the actors in each movie. I did the same for the other data lists in the json (actors, alternative_tiltes, genre).
I used the `objectID` as a foreign key. In the main `Movies` table, the objectID is a `PrimaryKey Autoincremented`.

At this point I was comfortable with the database but still needed to check the AlgoliaAPI implementation.
So I started working with it. It was accessible and well documented, so no problem.
But I had a problem, by my fault, that little detail that matters.
I had two `save_objects` tests but I didn't notice that one of them was the `save_object` method (without s) and I spent some time to understand the problem :-(


Then I just had to `code` the application.
The POST, the PUT and the DELETE

A last difficulty was to find a way to call the url with `/movieId` as option for the POST request.

I hope you will enjoy my work.

Thank you very much

