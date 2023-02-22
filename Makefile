pythondeps:
	python3 -m pip install --user -r requirements.txt

install:
	mkdir -p ~/.todo.actions.d
	cp -as $${PWD}/todo.actions.d/* ~/.todo.actions.d/
