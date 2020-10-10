pipenv shell
rm -rf nbs/_build
jupyter-book build --all nbs
ghp-import -n -p -f nbs/_build/html