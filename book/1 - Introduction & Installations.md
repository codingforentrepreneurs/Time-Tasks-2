## Chapter 1 - Introduction &  Installations

Welcome to Time & Tasks 2. This book & project will help you understand how to schedule, delay, and queue tasks (ie run python functions) with Django, Celery, & Redis. 

To accomplish all of this, it is best to use a worker process. This is a separate process outside the context of the standard `request/response` (ie `python manage.py runserver` or `gunicorn proj.wsgi:application` ) cycle that you might already be familiar with. The goal is to have a way to run tasks outside of `models`, `views`, `middleware`, `signals`, and many of the other ways you might run tasks within Django.

So, why do we need this?

**Efficiency**

There are cases were users needs things *right now* and there are times where they do not. Using Celery with Django allows you to offload tasks users don't need *literally right now*.

Here's a few examples of items that you can potentially offload:
- Email confirmations
- PDF Generation
- Data backups & downloads
- Machine Learning Results
- Graphs & Charts
- Webhook events
- Long-running programs (such as data analytics/analysis)
- Report generation


Now, the above is a list of things you might want to **delay** from running immediately especially if doing the above things is requested by any user on your site.

And here's the key: *delay* task via *user* requests.

Celery also allows us to *schedule* tasks. This means we can run certain tasks whenever we want. Here's a few examples:

- End old user sessions every two weeks
- Daily email notification summaries at midnight
- Weekly database backups
- Every 6 hours, trigger our machine learning pipeline to train new ML models
- Send a SMS every monday at 1:30pm to your top 5 clients

`Django` *can* do the above items (both lists) without `Celery` but it's a lot more complicated. The best part: you can use `celery` in nearly *any* python project. 

This book (and accompanying video series) covers how to implement celery in a Django project so you can effectively do what's above.


## 2. Skill Requirements

To get the most out of this book, you should know the following Django & Python concepts:

- Models
- Model Managers & QuerySets
- Signals (`post_save`, `pre_save`, etc)
- Views
- Decorators
- Request / Response cycle (at least conceptually)

The version of Django matters very little for the above concepts since these concepts will be with Django for a long time to come (at least until 2025 as of 2020).



Now, let's get your system installed.





## 3. Installations
Assuming you have the skill requirements for this book, you might want to just skip to the redis installation portion. You will need `redis` installed locally for this book (and for `celery`) although `rabbitmq` is another valid option. 

- Installing Python
- Creating & Activating a Virtual Environment
- Installing Python Packages (`pip install`)
- Installing Redis (macOS, Windows, Linux)


### 3.1. Install Python 3+

You can download python on [https://www.python.org/downloads/](https://www.python.org/downloads/). That's the easiest way on all platforms. 

Below are a few blog posts on our website that are useful references:

- Install Python on Windows: [https://cfe.sh/blog/install-python-django-on-windows](https://www.codingforentrepreneurs.com/blog/install-python-django-on-windows)

- Install Python on macOS [https://cfe.sh/blog/install-django-on-mac-or-linux](https://www.codingforentrepreneurs.com/blog/install-django-on-mac-or-linux)





### 3.2. Using Virtual Environments
Once you have Python installed, you'll need to use a virtual environment for your project. Virtual environments keep all of the software requirements (ie dependency versions) isolated from other projects. 

For better isolation, you can consider `Docker` but that's not required here.

#### 1 `venv`
Here's the easies way to create a virtual environment using Python's built-in `venv` module.

```
python -m venv my_venv
```
Replace `my_venv` with any folder name you want to create your virtual environment in. Python handles the creation of the environment, you must activate it.  You can also substitute `my_venv` for `.` to create the virtual environment in your current directory (aka folder).

A few key commands:

- Activate: `source bin/activate` (mac/linux)
- Activate: `.\Scripts\activate` (windows)
- Deactivate `deactivate` (all platforms; assuming your virtual environment is activated)
- Install packages (activate first): `pip install requests` (replace `requests` with any python package)
- Remove packages (activate first) `pip uninstall requests` 
- Installed packages `pip freeze`
- Save package history (to re-install/re-create current environment): `pip freeze > requirements.txt`

#### 2 `pipenv`

[pipenv](https://github.com/pypa/pipenv) (https://github.com/pypa/pipenv) is another very popular way to create an manage your virtual environments.

Official installation options are on https://github.com/pypa/pipenv#installation.

Install:
```
python -m pip install pipenv
# or
python3 -m pip install pipenv
```

Create
```
cd path/to/project/dir
python -m pipenv --python 3.8
```
`pipenv` creates a `Pipfile` that is a document that describes your virtual environment. 


A few key commands:

- Activate: `pipenv shell` (mac/linux/windows)
- Deactivate `deactivate` (all platforms; assuming your virtual environment is activated)
- Install packages (activate first): `pipenv install requests` (replace `requests` with any python package)
- Remove packages (activate first) `pipenv uninstall requests` 
- Installed packages `pipenv run pip freeze`
- Save package history (to re-install/re-create current environment): `pipenv run pip freeze > requirements.txt`


