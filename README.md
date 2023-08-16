
## Intelligent Tool Selector

This is a webpage to find a tool that matches a description of a task the user wants to complete.

### Installation instructions:

#### Backend

Use virtualenv to create a virtualenv. I recommend using `virtualenvwrapper`, and using python3.10.

```sh
mkvirtualenv tool-selector
pip install -r reqs.txt
```

To run the app:

```sh
cd backend/app
uvicorn main:app --reload
```

#### Frontend

The frontend is a create-react-app, so you can install and run it as usual.

```
npm install
npm start
```
