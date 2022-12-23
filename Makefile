deps:
	pip install --user -r requirements

install:
	mkdir -p ~/.todo.actions.d
	cp -s todo.actions.d/* ~/.todo.actions.d/
