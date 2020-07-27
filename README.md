# Tech Stack Onboarding Doc (help write this!)

## Summary

Our tech stack is **AWS -> Django REST -> Vue.js**. We use ec2 instance as our server, s3 bucket for static site hosting, and (soon) RDS PostgresQL db engine.

The static development site is hosted [here](http://humanityforward.s3-website-us-east-1.amazonaws.com). There's a boilerplate app. It fetches the API for politicians from the server.

The API endpoint (master) is [here](http://www.ec2-18-144-155-31.us-west-1.compute.amazonaws.com). It should be on track with master branch. It will always be online and working.

The development API endpoint (api_dev) is [here](http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com). It should be on track with api_dev branch.

Keep master always functional and base work on dev branch off master. Make a pr from dev branches whenever it will affect other dev branch.

## Design (Courtney)

- Typography: Avenir Next
- Color palette: 

## Frontend (Alex, Jaytee)

- Make sure you have [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) and [yarn](https://classic.yarnpkg.com/en/docs/getting-started) installed
- Go through the `README.md` of [this repo](https://github.com/multiplegeorges/vue-cli-plugin-s3-deploy) and follow the steps for their prerequisites, installation, and usage. This will be used in cases of deploying to s3 bucket manually (see below)
- [Visual Studio Code](https://code.visualstudio.com/) is the recommended editor with the following plugins/extensions:
  - **Auto Import** - *Automatically finds, parses and provides code actions and code completion for all available imports. Works with Typescript and TSX.*
  - **Code Spell Checker** - *A basic spell checker that works well with camelCase code. The goal of this spell checker is to help catch common spelling errors while keeping the number of false positives low.*
  - **ESLint** - *Integrates ESLint into VS Code. If you are new to ESLint check the [documentation](https://eslint.org/).*
  - **GitLens** - *GitLens simply helps you better understand code. Quickly glimpse into whom, why, and when a line or code block was changed.*
  - **Vetur** - *For Vue syntax-highlighting, snippet, emmet, intellisense, etc.*
- More in-depth guidelines found here: **[Frontend Guidelines](https://docs.google.com/document/d/13D1f3rSPvM5YMqcQUdHwvcPw0sA0Hqfs_N4EYA5cMPs/edit?usp=sharing)**

## Backend (Michael, Brian)

- Set up dependencies: python 3.7 virtualenv with requirements.txt
- Go through [tech folder](https://drive.google.com/drive/u/1/folders/1mzIpEBgastJnrVOOt-JvNQSlSmSnBuAp)
  - Understand data models and relations on MVP slide deck
  - Expected API endpoints and example behavior in ./api_endpoints

## AWS

We use the following services:

EC2: Server-side

- ping Michael for .pem to ssh in

S3: Host website and bucket to upload user content

- ping Michael for read/write permission to bucket
- ping Michael for aws credentials to deploy to bucket

RDS: PostgresQL database

- will set up after 8/15 internal demo
- install pgadmin4 workbench

Route 53: Domain name demodraft.com

- currently demodraft.com (hosted in separate production s3 bucket) routes to demodraft.org

## Costs

EC2: \$0/year (free-tier)

S3: \$[0.023](https://aws.amazon.com/s3/pricing/)/GB/month

Route 53: \$12/year for demodraft.com domain

## Notes \[IMPORTANT\]

Both frontend and backend folders are in this repo to keep everything in one place. Frontend devs can see backend logic. Backend devs can see how frontend devs load the data.

Keep master branch always functional! To create any feature, create new branch then pull. **Don't push to master unless it's README.md**. Create pull requests often!

Because backend and frontend is separate, there shouldn't be merge conflicts.

## Notes \[OPTIONAL\]

Michael is a first-time dev lead, so no doubt he'll have many flaws. Feel free to shoot him any constructive suggestion/criticism to how he can manage the tech stack and team better.

**Why Vue.js/Django/AWS?**

It's to work in parallel easily. The backend is separate from the frontend. Vue.js is a flexible JS framework for single-page applications with scalability and an easy learning curve. Components are decomposable. Vue.js supports importing HTML/CSS templates for easy design integration.

Django REST is extension of Django. It's minimalistic but scalable, and it integrates with many db engines.

AWS is a standard for startups. It has good docs and is cheap to start (?).

**Helpful links**

Frontend

- [Fetch API with Vue.js](https://rapidapi.com/blog/how-to-use-an-api-with-vue-js/)

Backend

- [Django REST](https://www.django-rest-framework.org/tutorial/quickstart/)

- [Serializer relations](https://www.django-rest-framework.org/api-guide/relations/)

- [Server-side setup with Django](https://www.youtube.com/watch?v=u0oEIqQV_-E)
