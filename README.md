# Tech Stack Onboarding Doc (help write this!)

# Summary

The static site is hosted [here](http://humanityforward.s3-website-us-east-1.amazonaws.com).

The REST endpoints are [here](http://www.ec2-18-144-155-31.us-west-1.compute.amazonaws.com).

The tech stack is **Vue.js** => **Django REST** => **AWS**.

# Design (COURTNEY)

# Frontend (ALEX)

# Backend (MICHAEL)

# AWS

Sec

# Notes \[important\]

Both frontend and backend folders are in this repo. See this to sync local git with just the relevant folder. When pushed to master, an Action automatically uploads to S3 bucket static hosting (frontend) and EC2 instance (backend).

# Notes \[optional\]

**Why Vue.js/Django/AWS?**

To work maximally parallel, the backend and data model logic is completely separate from the frontend. Vue.js is the most Javascript framework for single-page applications with scalability and an easy learning curve. Vue.js supports importing, making integration of good templates easy. Django-REST is extension of Django, with scalability and easy learning curve. It easily integrates with SQL database engine.
