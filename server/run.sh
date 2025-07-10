source venv/bin/activate

nohup python data_retrieval.py > out.log 2>&1 &

deactivate
