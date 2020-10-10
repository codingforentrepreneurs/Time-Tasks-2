. /Users/jmitch/.local/share/virtualenvs/time_and_tasks-6Snnipga/bin/activate
rm -rf nbs/_build
jupyter-book build --all nbs
ghp-import -n -p -f nbs/_build/html