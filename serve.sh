rm -rf nbs/_build
jupyter-book build --all nbs
ghp-import -n -p -f nbs/_build/html

cp -r nbs/_build/html/* book/
python -m http.server --directory book/