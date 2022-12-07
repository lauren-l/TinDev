Project contributors (sorted alphabetically by last name)
============================================

* **[Solina Kim](https://github.com/SolinaKEK)**
  * Basic setup
    * scope of work
    * Django filesystem
  * Candidate and recruiter signup
    * Created models for Candidate and Recruiter
    * Created django forms for Candidate and Recruiter with custom validators where appropriate
    * Created frontend html templates for candidate and recruiter signup pages
    * Connected front and back ends via views
  * Candidate dashboard searchbar
    * Implemented backend functionality in views
    * Used ajax to be able to produce search results without reloading entire page
  * Candidate demonstrating ineterest, compatibility score
    * Implemented backend functionality for candidate to be able to demonstrate interest in a job
    * Implemented ajax and custom functions in views to automatically create and submit an application without reloading page
    * Implemented backend to automatically calculate and save compatibility score upon candidate demonstrating interest.
    * Designed formula to calculate compatibility score.

* **[Lauren Lee](https://github.com/lauren-l)**
  * Recruiter Dashboard
    * Created job post components with html and django
      * Implemented backend functionality to render card with desired information
      * Implemented backend functionality to link each card with matching view applicants portal
    * Created template for recruiter dashboard page
    * Connected front and back end in views
    * Implemented post filters
  * View Applicants Portal
    * Created models for applicants and offers
    * Created applicant info card with html and django
      * Implemented backend functionality to render card with desired information
    * Implemented send offers functionality
      * Designed and created modal that updates offers or creates a new offer if no pre-existing offer exists
      * Created Django form to get offer details
    * Created template for view applicants page
    * Connected front and back end in views
  * Database
    * Pre-populated database with candidate, recruiter, job, and offer info 


* **[Christian Matthew](https://github.com/ChristianMSurya)**
  * Homepage/Login/logout
    * Designed the homepage that holds info about TinDev, the login card, and the sign up options
    * Login function, if logged in successfully, allows username to be access during the session
    * Logout flushes out session storage used to store login info
  * Branding
    * Figma initial [mockup](https://www.figma.com/proto/p58MwVcLHV2GGAXq7cbddX/TinDev-%7C-Paradigms-Project?node-id=28%3A20&scaling=scale-down&page-id=0%3A1)
    * Branding guideline [documentation](https://docs.google.com/document/d/1JYB6tChzI9_7OUnhwf719cCepFSz9Uk3VzRyYBFnRM0/edit?usp=sharing) created
    * Created the logomark and wordmark needed for the website branding
    * Chose color proper palette for the techy vibe of the project
    * Set up typography (open sans) and button design
    * Designed the simple nav bar
    * Created style.css
  * Create, update, delete job posts
    * Created a form in forms.py for the create job post page available to recruiters
    * Allowed update/edit functionality with ModelForm with an initial instance of existing data from the database
    * Gave permission to the creator of the job posts to edit or delete their post
    * Disabled the ability for recruiters to edit or delete other people's posts
  
* **[Yewon Oh](https://github.com/team-member-2-github)**

  * ... contribution 1 description ...
  * ... contribution 2 description ...


