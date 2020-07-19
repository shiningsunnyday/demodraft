# Tech Stack Onboarding Doc (help write this!)

# Summary

The static site is hosted here.
The REST endpoints are here.

The tech stack is Vue.js => Django-REST => AWS. To work maximally parallel, the backend and data model logic is completely separate from the frontend. Vue.js is the most Javascript framework for single-page applications with scalability and an easy learning curve. Vue.js supports importing, making integration of good templates easy. Django-REST is extension of Django, with scalability and easy learning curve. It easily integrates with SQL database engine.

# Design (COURTNEY)

# Frontend (ALEX)

# Backend (MICHAEL)

# Deployment

# Miscellaneous Notes

Both frontend and backend folders are in this repo. See this to sync local git with just the relevant folder. When pushed to master, an Action automatically uploads to S3 bucket static hosting (frontend) and EC2 instance (backend).
