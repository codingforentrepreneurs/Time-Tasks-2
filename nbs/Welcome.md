# Welcome to Time & Tasks 2

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