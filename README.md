# Book A Meal :pizza:
[![Build Status](https://travis-ci.org/codingedward/book-a-meal.svg?branch=feature%2Fapi)](https://travis-ci.org/codingedward/book-a-meal)
[![Coverage Status](https://coveralls.io/repos/github/codingedward/book-a-meal/badge.svg?branch=feature%2Fapi)](https://coveralls.io/github/codingedward/book-a-meal?branch=feature%2Fapi)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
<a href="http://flask.pocoo.org/"><img
   src="http://flask.pocoo.org/static/badges/made-with-flask-s.png"
   border="0"
   alt="made with Flask"
   title="made with Flask"></a>

This is the Andela Book-A-Meal web project challenge.  This GitHub repository 
has also been integrated with that PivotalTracker project and on every commit, 
there will be an id to the story being worked on.

**Note**: The UI template is [here](https://codingedward.github.io/book-a-meal).

**Note**: The PivotalTracker project is
[here](https://www.pivotaltracker.com/n/projects/2165567). 

**Note**: The documentation for the API is 
[here](https://mealbooking.docs.apiary.io)

## Table of Content

  * [Introduction](#introduction)
  * [The Client Side](#the-client-side)
     * [Color Palette](#color-palette)
     * [Fonts](#fonts)
     * [Images and Textures](#images-and-textures)
     * [Pages](#pages)
        * [Landing Page](#landing-page)
        * [Sign Up Page](#sign-up-page)
        * [Login Page](#login-page)
        * [Caterer Meals Management Page](#caterer-meals-management-page)
        * [Caterer Menu Management](#caterer-menu-management)
        * [Caterer Orders](#caterer-orders)
        * [Caterer Order History](#caterer-order-history)
        * [Customer Menu](#customer-menu)
        * [Customer Orders](#customer-orders)
        * [Customer Notifications](#customer-notifications)
        * [Customer Order History.](#customer-order-history)
  * [The Server Side](#the-server-side)
     * [Installation](#installation)
     * [Configuration](#configuration)
     * [Running](#running)
     * [Running](#testing)


## Introduction
The project entails having a caterer as the site administrator and can add 
meals to the application as well as set menus for a particular day. 
The customers, after signing up first, are then allowed to book meals online.

## The Client Side
This is the frontend part of the application and will involve building from 
the ground up a user interface without the use of UI frontend frameworks such 
as Bootstrap or Foundation. 

The color palette was generated using [coolors.co](https://coolors.co) which 
is a tool for generating non-crashing colors.

The wireframes are built using [wireframe.cc](https://wireframe.cc/).

### Color Palette
The following is the chosen scheme:

![Coolors Chosen Palette](https://coolors.co/export/png/2d728f-3b8ea5-f5ee9e-f49e4c-ab3428)

### Fonts
The following are the fonts used for this project:
1. [Nunito (Google Fonts) ](https://fonts.google.com/?query=Nunito)
2. [Leckerli One (Google Fonts)](https://fonts.google.com/?query=Leckerli+One)

### Images and Textures
The following are the images and textures used for this project:
1. [Photo](https://unsplash.com/photos/4_jhDO54BYg) by Dan Gold on Unsplash.
2. [Photo](https://unsplash.com/photos/awj7sRviVXo) by Casey Lee on Unsplash.
3. [Photo](https://unsplash.com/photos/tzl1UCXg5Es) by Robin Stickel on Unsplash.
3. [Photo](https://unsplash.com/photos/QaGDmf5tMiE) by Joseph Gonzalez on Unsplash.
4. [Photo](https://unsplash.com/photos/Vajgh8pZKnI) by Tran Mau Trin Tam on Unsplash.
5. [Texture](https://www.transparenttextures.com/food.html) background pattern.
6. Hamburger menu [icon](https://icons8.com/icon/5574/menu).

### Pages
Here we will show the wireframes of the main pages. 
The heirarchy of the application is as follows:

![Map](https://image.ibb.co/gwHiWx/map.png)

The web application will have the following pages:

#### Landing Page
This will be the first page any user of the application will land on. 
The following is the the wireframe of this page:

![Landing Page Wireframe](https://image.ibb.co/irri6n/landing_page.png)

From here the user can either choose to login or sign up as well as see some 
of the menus available for that particular day.

#### Sign Up Page
This will be used to create an account by a new user.
The  following is this page's wireframe:

![Sign Up Page Wireframe](https://image.ibb.co/eYR4z7/sign_up.png)

**Note**: The administrator does not sign up and he/she will have a default
account.

#### Login Page
This page will be used by both the adminstrator(the caterer) and the 
customers. The two will be differentiated using roles on the server. 

![Login Page Wireframe](https://image.ibb.co/gtzDsS/login.png) 

#### Caterer Meals Management Page
This is where the administrator will manage the meals in the application.

![Caterer Meals Management Frame](https://image.ibb.co/d89osS/manage_meals.png)

#### Caterer Menu Management 
Here the caterer can set the menu for a specific day

![Caterer Set Menu](https://image.ibb.co/dKxxmn/set_menu.png)

#### Caterer Orders 
Here, the caterer will be able to see meals ordered by the customer.

![Caterer Orders](https://image.ibb.co/h82Kz7/orders.png)

#### Caterer Order History
Here the caterer can view the history of orders made by customers.

![Caterer Order History ](https://image.ibb.co/jJRORn/order_history.png)


#### Customer Menu
Here, the user can view what has been set on the menu and make orders.

![User Menu](https://image.ibb.co/cGb2rx/user_menu.png)

#### Customer Orders
Here the customer can see and track the orders they made. After it has been
approved by the caterer, the status of the order will also change and he/she
can see this.

![User Orders](https://image.ibb.co/jY62rx/user_orders.png)

#### Customer Notifications
Here the customer will get updates on new meals and when the caterer sets the
menu.

![User Notifications](https://image.ibb.co/i5DqBx/user_notifications.png)

#### Customer Order History.
Here the customer can see their order history.

![User Order History](https://image.ibb.co/guyqBx/user_history.png)


## The Server Side

This application uses Flask Python web microframework to create a RESTful 
API.

**Note**: The documentation for the API is 
[here](https://mealbooking.docs.apiary.io)

### Installation

To have the API running, you will have to have `pipenv` package manager. To 
install this, run the following command:
```
$ pip install pipenv
```
Then, change directory to the `/API` where the application code is located.
```
$ cd API
```
Next, you have to install the applications dependancies.
```
$ pipenv install
```

### Configuration

This application requires some configuration held in the `.env` file.
For this, the `.envexample` file has already been provided and you simply have
to copy paste it to `.env` file. That is:
```
$ cp .envexample .env
```

Then, ensure you **fill in the required values** in the configuration file.



### Running

This part assumes you have already configured your application as described 
above. To access the virtual enviroment created by `pipenv`, run:
```
$ pipenv shell
```
This will load the environment variables and create your virtual environment.  
To run your application, simply run:
```
$ flask run
```
You should then have your application up and running:
```
 * Serving Flask app "run" 
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) 
```

### Testing

The application was built using TDD pattern and therefore has tests that can
be run using `nose` test runner. To run these tests, simply run `nosetests`:
```
$ nosetests test_endpoints.py
```
