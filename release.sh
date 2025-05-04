cp -rf ./.pypirc ~/.pypirc
sh installer.sh
python setup.py sdist upload
pdoc -d google --output-dir doc pyheaven
git add --all
git commit -m "0.1.6.8"
git push -u

twine check pkg/*
twine upload pkg/*
