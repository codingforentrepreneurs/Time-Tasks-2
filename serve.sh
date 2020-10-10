. /Users/jmitch/.local/share/virtualenvs/time_and_tasks-6Snnipga/bin/activate
rm -rf book
rm -rf nbs/_build
mkdir book
jupyter-book build --all nbs
cp -r nbs/_build/html/* book/
python -m http.server --directory book/