.PHONY: all install run runmanual runwithinterface
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

$(VENV)/bin/activate: 
	python3 -m venv venv
	venv/bin/pip install --upgrade -r requirements.txt
	venv/bin/pip install --upgrade opencv-python
	venv/bin/pip install scipy

run: venv
	echo "amostragrafos1-2.csv\namostragrafos1.csv\n0.3" | venv/bin/python3 src/r2.py
	xdg-open grafo.png
	xdg-open resultados.txt

runmanual: venv
	venv/bin/python3 src/r2.py
	xdg-open grafo.png
	xdg-open resultados.txt
runwithinterface:
	venv/bin/python3 src/interface.py
