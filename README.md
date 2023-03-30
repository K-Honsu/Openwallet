## Running it on the Local Server📡 <hr>

- To run a Django Python backend on the local server, you can follow these steps:

- Open a command prompt or terminal on your computer.

- Navigate to the root directory of your Django project.

- Activate the virtual environment for your project. If you don't have a virtual environment set up, you can create one using the venv module by running the following command:

```
python -m venv myvenv
```

- This will create a new virtual environment in a directory named myvenv.

- Activate the virtual environment by running the following command:

```
source myvenv/bin/activate
```

- Note: If you're on Windows, the command to activate the virtual environment will be slightly different. You can use the following command instead:

```
myvenv\Scripts\activate
```

- Once the virtual environment is activated, you can start the Django development server by running the following command:

```
python manage.py runserver
```

- This will start the development server on your local machine, and you should see output similar to the following:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

- Open a web browser and navigate to the URL that was displayed in the output. You should see the Django project running on your local machine.

- Congratulations, you have now successfully run a Django Python backend on the local server!
