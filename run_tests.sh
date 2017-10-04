echo Installing requirements
pip3 install -r requirements.txt

echo Generating Session Key
python3 gen_sessionKey.py

pytest --html=report.html -v -n auto tests/

open ./report.html