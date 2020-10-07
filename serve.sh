rm -rf nbs/_build
rm -rf book
mkdir book
jupyter-book build --all nbs
cp -r nbs/_build/html/* book/
python -m http.server --directory book/