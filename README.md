
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

#### Design Decisions:

I've made a small number of changes from the guidelines.

Backend:
- I've added a database table for Tools. The Tools are still loaded from a fixtures, `tool_fixtures.json`, but I think it's potentially useful to have it in the database.
- I added a ManyToMany table to join Prompt and Tools. This is currently unused, but would be useful if the prompt & tools selected were being saved.

Frontend:
- I made the 300 character limit on the description a soft requirement.
