# SEC Data project

This repo contains code for a web application that allows users to view SEC Filing data. The application downloads public data from SEC.gov every quarter and builds these filings into a database (PostgreSQL). The backend web application that interacts with the database is made with the Django web framework an several additional Django packages including celery and Django REST Framework. Primarily serving as a REST API, the Django application data is consumed by a Vue.js application that users can access in their browser over the internet. Users can also signup for an account and request credentials to access the same public API that the Vue.js application requests data from.

This project is open source and anyone is welcome to contribute or create issues and merge requests.

## Local development

To run this application on your local computer, you can use docker and docker-compose.

Before running the project, you must create a file in the root directory called `.env`. This file will provide values to docker-compose that you do not want to commit to source code, so `.env` is not committed to version control (git). The only truely sensitive data is a OAuth2 client keys for the Linkedin OAuth2 application that you may choose to setup if you wish to test social authentication in your local environment, but this is not required, so you can add placeholder values for these variables. See `.env.template` for more information about setting up OAuth2 keys with a Linkedin OAuth2 application.

Once you have created `.env`, run the following command:

```
docker-compose up
```

This will start the project locally. It may take some time build the docker images. When everything has finished, visit `http://localhost` in your browser and follow the instructions there for completing the setup of you local environment.

You can check the logs of `docker-compose up`, you should make sure that no service failed to start.

Additional project documentation is coming soon.
