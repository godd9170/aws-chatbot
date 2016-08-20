#AWS-Chatbot

##Getting Started
#### 1) Get yourself serverless from npm
```
npm install -g serverless@v0.5.5
```
#### 2) Clone this repo
```
git clone git@github.com:godd9170/aws-chatbot.git
```
#### 3) install the modules
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
  "project": "aws-chatbot",
}

```

If you're creating a new function, and you'd like access to those credentials in it, make sure you include the SFDC environment variables in the `s-function.json`:

```
"environment": {
    "SERVERLESS_PROJECT": "${project}",
    "SERVERLESS_STAGE": "${stage}",
    "SERVERLESS_REGION": "${region}"
  }
```

## Some Inspiration

https://medium.com/@pixelcodeuk/create-a-slack-slash-command-with-aws-lambda-83fb172f9a74#.yqkccdlvq