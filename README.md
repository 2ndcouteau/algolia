# algolia
Algolia Test


### Install and Run the app

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
(x) - Synchronize this source of truth with an Algolia index
