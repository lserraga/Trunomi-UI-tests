pip3 install -r requirements.txt

python3 gen_sessionKey.py

pytest --html=report.html -n auto tests/

open ./report.html