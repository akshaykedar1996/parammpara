each "BUILD START"
python3.11 -m pip install -r requestments.txt
python3.11 manage.py collectstatic --noinput --clean
echo "BUILD END"