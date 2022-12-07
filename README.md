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

### Accessing pages
Home page can be viewed at http://localhost:8000/home

Candidate Signup can be viewed at http://localhost:8000/signup_candidate  
Recruiter Signup can be viewed at http://localhost:8000/signup_recruiter

Candidate Dashboard can be viewed at http://localhost:8000/candidate_dashboard  
Recruiter Dashboard can be viewed at http://localhost:8000/recruiter_dashboard
