pythondeps:
	python3 -m pip install --user -r requirements.txt

install:
	mkdir -p ~/.todo.actions.d
	cp -s todo.actions.d/* ~/.todo.actions.d/
