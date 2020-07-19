# Tech Stack Onboarding Doc (help write this!)

# Summary

The static site is hosted [here](http://humanityforward.s3-website-us-east-1.amazonaws.com).

The API endpoint is [here](http://www.ec2-18-144-155-31.us-west-1.compute.amazonaws.com).

The tech stack is **Vue.js => Django REST => AWS**.

# Design

# Frontend

Install npm and yarn. Get [this](https://github.com/multiplegeorges/vue-cli-plugin-s3-deploy) for deploying to s3 (see below).

# Backend

# AWS

We use the following services:

EC2: Server-side
  * ping Michael for .pem to ssh in

S3: Host website and bucket to upload user content
  * ping Michael for read/write permission to bucket
  * ping Michael for aws credentials to deploy to bucket

RDS: PostgresQL database
  * install pgadmin4 workbench

Route 53: Domain name registration

# Costs

EC2: $0/year (free-tier)

S3: $0.023/GB/[month](https://aws.amazon.com/s3/pricing/)

Route 53: $12/year for demodraft.com domain

# Notes \[IMPORTANT\]

Both frontend and backend folders are in this repo to keep everything in one place.

Keep master branch always functional. To create any feature, create new branch then later pull. Because backend and frontend is separate, there shouldn't be merge conflicts. 

When pulled into master, an Action automatically builds and deploys /forward_web to S3 bucket static hosting (frontend) and uses [this]() to restart server on EC2 instance (backend).

# Notes \[OPTIONAL\]

**Why Vue.js/Django/AWS?**

It's to work maximally parallel. The backend and data model logic is separate from the frontend. Vue.js is a flexible JS framework for single-page applications with scalability and an easy learning curve. Components are decomposable. Vue.js supports importing HTML/CSS templates for easy design integration. 

Django-REST is extension of Django, with scalability and easy learning curve. It easily integrates with SQL database engine.

AWS is also scalable.

**Helpful links**

Frontend

  * [Fetch API with Vue.js](https://rapidapi.com/blog/how-to-use-an-api-with-vue-js/)
  
Backend

  * [Django REST](https://www.django-rest-framework.org/tutorial/quickstart/)

  * [Server-side setup with Django](https://www.youtube.com/watch?v=u0oEIqQV_-E)
  

