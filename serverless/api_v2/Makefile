build:
	cd saveUser && env GOOS=linux go build -ldflags="-s -w" -o ../bin/saveUser user.go main.go && cd ..
	cd saveLocation && env GOOS=linux go build -ldflags="-s -w" -o ../bin/saveLocation main.go && cd ..

clean:
	rm -rf ./bin