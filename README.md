#AWS-Chatbot

##Getting Started
#### 1) Get yourself serverless from npm
```
npm install -g serverless@v0.5.5
```
#### 2) Clone this repo
```
git clone git@github.com:
```
#### 3) install the modules (Serverless v0 doesn't like unmet dependencies)
```
npm install i
```
#### 4) Initialize the project (see [docs](http://docs.serverless.com/docs/project-init))
```
serverless project init
```
## Environment Variables

To ensure that no credentials are actually stored in this repo, we leverage the _meta folder that's created when you install this serverless project.

Within `_meta > variables > s-variables-common.json` ensure the json looks like this:

```
{
  "project": "venga-usage",
  "salesforce_username": "test@test.com",
  "salesforce_password": "p@$$w0rd",
  "salesforce_token": "TOKEN_HERE"
}

```

If you're creating a new function, and you'd like access to those credentials in it, make sure you include the SFDC environment variables in the `s-function.json`:

```
"environment": {
    "SERVERLESS_PROJECT": "${project}",
    "SERVERLESS_STAGE": "${stage}",
    "SERVERLESS_REGION": "${region}",
    "SFDC_USER" : "${salesforce_username}",
    "SFDC_PASSWORD" : "${salesforce_password}",
    "SFDC_TOKEN" : "${salesforce_token}"
  }
```