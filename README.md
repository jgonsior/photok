# Functional and technological specification
## Functional specification:

Photok is a web application around photo contests. Every user 
can perform the following actions:
* Register
* Create a contest with a theme, deadline, prize
* Participate in an existing contest (via handing in pictures)

### User management
A user can have one or more of the following roles, each depending in the context of the contest:
* Organiser (defined as a user who created a contest)
* Participant (a user who participates in a contest)
* Jury (a user who can vote for the winner for a contest)
* Guest (a user who has basically only "read access" to view the pictures for a contest)

## Technological specification:
### Technical Requirements
Our frameworks need to offer the following abilities in order to implement our desired 
functional requirements:
* Multiple user roles
* Persistent storage
* Process images (generate multiple resolutions etc.)
* REST-API e.g.for a possible mobile app
* Send mails to users

### Choosen frameworks
#### Client framework
Most client-side frameworks would be enough for our project. We are going to use AngularJS
as a frontend because it is greatly documented, is used by many other developers and is known to be
stable. In addition to that can we be sure that the development of this framework will be 
continued in the future because Google stand behind this project.

#### Server framework 
The server side framework choice was mainly influenced by the choice of the underlying
programming language. We've choosen Python and therefore Flask. It is microframework with 
the ability to create a RESTful and service-oriented API.

To be able to manage multiple connections from different users at the same time are we going
to use a task queue in the background. We'll use RabbitMQ and Celery to connect RabbitMQ to Flask.

#### Continuous integration tool
We are going to use Jenkins as a continuous integration tool because it offers good documentation, is widely used 
and it's pipeline architecture is robust, extensible and versatile.

#### Deployment platform
We'd like to deploy our application in a docker container because it gives us the 
ability to freely deploy our docker container on different infrastructures like OpenShift, 
AWS or Microsoft Azure.