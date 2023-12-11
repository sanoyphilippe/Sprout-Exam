# Sprout-Exam
Technical exam for Sprout Solutions Application

Please see individual readme sections for each folder of the back-end and front-end sections of this app


# Back-end
The back-end is built using the FastAPI framework utilizing python as the programming language.
Also utilizing MongoDB for the DB storage.
See: https://fastapi.tiangolo.com/

# Front-end Stack
The front-end is built using the Quasar Framework with Vue3 and Typescript/javascript

See: https://quasar.dev/

# Improvements, Technical Debt

## Front-end
### Technical Debt
Currently the front-end only has the Login, Delete Employee, and Get List of Employees feature. There are several things to still finish
for the front-end side as it has not been finished. The base scaffolding and folder structure are all completely done and set up thanks to the usage of Quasar Framework.
Code cleanup needs to be done as well. Refactoring of some components and pages needs to be done as well for better layering.
Would also be nice to have a better UI design. Better documentation could also be done for the readme as well as comments within the codes.
Some existing bugs as well regarding client side authorization for the pages using the access token.

### Future features
Functionality to change regular employees to contractual employees and vice versa, login credentials for each employee, setup for more admin users/manager users.
Localization would also be a nice addition to have.

### Setting up for production
Env variables should also be setup, considering deployment to some cloud services for production ready deployment, then setting up some tests and a CI/CD pipeline. 
Obtaining a domain name as well as setting up an SSL certificate to enable https security when accessing the site.

## Back-end
Back-end is fully functional and all APIs should be working correctly to Add, Update, Delete employees as well as get specific employee and get all employees list.

### Technical Debt
Better documentation and comments for the codes as well as setting up some unit tests.

### Setting up for production
Consider deployment to some cloud services for production, then setting up some tests and a CI/CD pipeline. 
Obtaining a domain name as well as setting up an SSL certificate to enable https security when accessing the site.
