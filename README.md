![TinDev Logo](/TinDev/app/static/images/tindev_combomark.png)

# About The Project
This project is proof of concept for  "Tinder for Devlopers", created as a final project in Professor Joanna's programming paradigms class. The program supports the following functionalities and more:
* Sign up / log in as a recruiter
* Sign up  / log in as a candidate
* Create, delete, and view job posts as a recruiter
* View, like, dislike, filter, and search job posts as a candidate
* View compatibility scores between candidate and job
* Make offers to applicants
* Accept / reject offers

## Built With
List here all the dependencies of your project (including version). For example:

* [Python](https://www.python.org/) version 3.9.12
* [Django](https://www.djangoproject.com/) version 4.1.2
* [Bootstrap](https://getbootstrap.com) version 5.2.2
* [JQuery](https://jquery.com) version 3.6.1

## Getting Started

### Prerequisites

* Django
  ```sh
  python -m pip install Django
  ```
* JQuery
  ```sh
  npm install jquery
  ```
* Boostrap
  ```sh
  npm install bootstrap@3
  ```

### Installation

Describe here the list of steps to get your project running. For example:
1. Request access to the repository
2. Clone the repo
   ```sh
   git clone [https://github.com/github_username/repo_name.git](https://github.com/lauren-l/TinDev.git)
   ```

### To run
cd into Tindev/Tindev, then run `python3 manage.py runserver`

### Logging in
Home page can be viewed at http://localhost:8000/ or http://localhost:8000/home

Current user information[^1] (10 recruiters, 10 candidates) can be viewed via:
  https://docs.google.com/spreadsheets/d/1S8LFusJNuBiDUVzQEXClhF5as4ttI8G8_bJ_4_FhVcU/edit?usp=sharing

### Candidate
Job Posts can be "passed" or "smashed" if active. If the post is "smashed" then an application for the post is submitted.

Job offers can be viewed by clicking "Offers" in the navbar

Log out by clicking "Log Out" in the navbar

filter functionality works with either search bar OR post filters, not both.
* to use search bar, enter terms in the search bar and click search
* to use post filters, select desired post filters and click filter posts

### Recruiter
Job posts can be created by clicking "create new job post". Each post can be edited or deleted via the drop down menu on the top left corner of each card.

to filter posts, select desired post filters and click filter posts

To view applications, click the "View # Applicants" button on the lower right of each job post. This will redirect you to the view applicants portal.

To extend an offer, click "Extend Offer" on the bottom right of each applicant. This will open a modal to provide information to extend an offer.
* An offer will not be created/updated if the expiration date is in the past
* Offers will be created if an offer for the specific job, candidate does not exist. Otherwise, the offer will be updated

Return to the recruiter dashboard from the view applicants portal by clicking the "return to dashboard" button at the top of the page

Log out by clicking "Log Out" in the navbar

### Admin
Admin access is available at http://localhost:8000/admin [^2]

username: tindev
password: tinder


[^1]: information other than usernames and passwords may not match with info in the database
[^2]: Editing/Creating/Deleting items through admin can cause errors in data. Such actions should be performed through the UI of the website.