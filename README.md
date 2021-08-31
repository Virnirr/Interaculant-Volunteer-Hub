![](https://github.com/Virnirr/Interaculant-Volunteer-Hub/blob/main/static/image/banner.png?raw=true)

[![Python](https://img.shields.io/badge/Python-3.9.6-21455f?logo=python&labelColor=21455f)](https://www.python.org/)
[![HTML5](https://img.shields.io/badge/HTML5-orange?logo=HTML5&labelColor=orange)](https://html.com/)
[![CSS](https://img.shields.io/badge/CSS3-darkgreen?logo=CSS3&labelColor=darkgreen)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![CSS](https://img.shields.io/badge/JavaScript-yellow?logo=JavaScript&labelColor=darkyellow)](https://www.w3schools.com/js/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-purple?logo=Bootstrap&labelColor=purple)](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/Virnirr/Interaculant-Volunteer-Hub/blob/main/LICENSE)

This project is based upon creating and joining volunteer services across the world.

## Table of Contents:
- [Description](https://github.com/Virnirr/Interaculant-Volunteer-Hub#description)
- [Features](https://github.com/Virnirr/Interaculant-Volunteer-Hub#features)
- [Technologies](https://github.com/Virnirr/Interaculant-Volunteer-Hub#technologies)
- [What I Learned](https://github.com/Virnirr/Interaculant-Volunteer-Hub#what-i-learned)
- [Thank you!](https://github.com/Virnirr/Interaculant-Volunteer-Hub#thank-you)

## Description

This project is a responsive web application that is built to connect communities, non-profit organizations, etc., with volunteers in their communities and around the world. How this project functions is that a user sign in the website by setting an email(for others to contact), username, and a password for security (passwords are hashed with sha256). After signing in, users are taken to "Service" page, where they can freely view and sign up for any particular services that they are interested in. After signing up for a particular service, the service informations are stored in a database that is only viewable by the user who signed up. The user will also be able to remove any service that they do not plan to attend. Users can additionally create new services in the "Create Services" tab where they can enter informations related to their service including title, date, start time, end time, total volunteer needed, and a little description/instruction for the service. The service will then be stored into a database and generated into "Services" tab, where it will be public for every users. Users will be able to track their created services with each volunteer who signed up for the every particular services.

## Features

- Landing:

When a user first enters my web application, they are greeted with a message and "Get Started" button which will take them to my register page. Furthermore, the landing page also shows my project's motto, which is "Service Before Self." Additionally I have included an "About Me" section in my landing page which talks a little about the inspiration I got for my web application. 

- Contact:

In the contact page, users can contact me with the informations on the right, provided by me. However, they can also contact me by entering in their full name, email address (so that I'm able to contact back), and any messages that they would like to get across. After press the "Contact" button, a message will be sent directly to my email.

- Register and Login: 

In the register page, users (communities, non-profit organizations, and volunteers) will be able to register an account by entering their preferred username, email, password, and a confirming password. Passwords will be hashed with sha256 function for security purposes. After registration, user will be redirected to the login page where they will enter their informations.

- Services:

In the service tab, users can freely browse all the created services by others. After the user has found a service that they would like to volunteer for, they can press the "Sign Up" button to take up an available spot. The users information will then be stored into a database. Users can view all their joined services in the "Services Joined" Tab. After the available spot drops down to 0, users will not be able to sign up for that particular service until an available spot is opened. 

- Create Service:

In the Create Service tab, users can create a service by choosing a theme (currently only have three themes, Celebration, Foodie, and Education) for their service, a title, a date, a start and end time, location, maximum volunteer, and a little instruction or description of the service. After the user has inputted on the required informations and posted the service, it will then be stored into a database and generated into the Service tab, where it will be public to all other users. 

- Services Joined:

In the Services tab, users will be able to view all their joined services in a table, which will show every services, their title, their date, their start and end time, and their locations. Users will also be able to remove any services that they do not intend to volunteer at or decides not to.

## Motivation

This project is inspired by Rotary internation's service club aiming to combat world problems such as world hunger, social ineqality through the use of Volunteer Services and events. I found this project to be valuable for a wealth of applications for communities who seek to find volunteer members quickly and efficiently. It could potentially help communities resolve low volunteer issues. 

## Technologies

HTML/CSS/JavaScript:

I used HTML/CSS/JavaScript to deploy my front-end designs and features, such as functional navigation bars and forms.

Python/Flask:

I used Python and Flask for my back-end development which allows me to receive datas submitted by users, such as register and login.

CS50 SQL/Postgres

I used CS50 SQP to execute and query my SQL commands while using Postgres to store all my datas.

## What I learned

- HTML/CSS/JavaScript
- Bootstrap CSS Framework
- Python
- Git & Github
- Flask
- Postgres
- VScode (code editor)

This project definitely encouraged me to learn alot by myself. Before even starting, I had to learn how to use VScode (including setting up, using a virtual environment, etc.). Moreover, I learned a bit about python packaging and couple python libraries like psycopg2, flask, and os. Furthermore, I learned the basics of git and github; how to package and push my repository into github using git commands. Ultimately, if not for time sake, I would definitely go down a rabbit hole of learning other python libraries, using different design formats on HTML/CSS/JavaScripts. Finally, I just want to say that I'm glad I completed my first ever web development project.

## Thank You!

It has definitely been a long two week of coding, debugging, and desiging my web application, but seeing my application run while learning topics that I have not touched upon is definitely a lasting memory. Thank you for viewing my project!