# algolia
Algolia Test


### Install and Run the app

#### Build the docker image
`docker build --tag algolia-test .`

#### Run the app
`docker run -d -p 5000:5000 algolia-test`

By default, the container is doing so in isolation mode and cannot connect to localhost:5000.
So we use a redirection port to access the app `-p 5000:5000`

