# Tech Stack Onboarding Doc (help write this!)

# Summary

The static site is hosted [here](http://humanityforward.s3-website-us-east-1.amazonaws.com).

The API endpoint is [here](http://www.ec2-18-144-155-31.us-west-1.compute.amazonaws.com).

The tech stack is **Vue.js** => **Django REST** => **AWS**.

# Design (COURTNEY)

# Frontend (ALEX)

# Backend (MICHAEL)

# AWS

Sec

# Notes \[IMPORTANT\]

Both frontend and backend folders are in this repo. See this to sync local git with just the relevant folder. When pushed to master, an Action automatically uploads to S3 bucket static hosting (frontend) and EC2 instance (backend).

# Notes \[OPTIONAL\]

**Why Vue.js/Django/AWS?**

It's to work maximally parallel. The backend and data model logic is separate from the frontend. Vue.js is a flexible JS framework for single-page applications with scalability and an easy learning curve. Components are decomposable. Vue.js supports importing HTML/CSS templates for easy design integration. 

Django-REST is extension of Django, with scalability and easy learning curve. It easily integrates with SQL database engine.

AWS is helpful.

**Helpful links**

[Fetch API with Vue.js](https://rapidapi.com/blog/how-to-use-an-api-with-vue-js/)

[Django REST quickstart]()

[Server-side setup](https://www.youtube.com/watch?v=u0oEIqQV_-E)
