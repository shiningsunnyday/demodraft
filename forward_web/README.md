# forward_web

## Project setup

### Set up config private variables

```
cd forward_web
cd src
cp config.json.example config.json
```

Inside `config.json` replace with:

```json
{
  "GOOGLE_API_KEY": "AIzaSyCZEANXil1Gxu7RJK2bsDMQqRnqmuo5OD4",
  "API_URL": "http://ec2-54-183-146-26.us-west-1.compute.amazonaws.com"
}
```

- As of now, using Alex's google api key and dev environment API_URL

```javascript
yarn install
```

### Compiles and hot-reloads for development

```javascript
yarn serve
```

### Compiles and minifies for production

```javascript
yarn build
```
