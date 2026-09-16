all:
	docker build --no-cache -t my-vhs-extended:latest .
test:
	docker run --rm --network=host -v "$$PWD:/vhs" my-vhs-extended:latest ./demo.tape
	cp -v ./demo.gif ../assets/images
clean:
	ollama  list|grep -v 'NAME'|awk '{ print $1 }'|xargs  ollama  rm
