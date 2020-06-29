// Server2
package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
)

var mu sync.Mutex
var count int

func main() {
	http.HandleFunc("/", handler)
	http.HandleFunc("/count", counter)
	fmt.Println("start http server")
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}

// Handler echoes the Path component of the request URL r.
func handler(w http.ResponseWriter, r * http.Request) {
	print(r.URL.Path)
	mu.Lock()
	count ++
	mu.Unlock()
	fmt.Fprintf(w, "URL.Path = %q\n", r.URL.Path)
}

// counter echoes the number of calls so far.
func counter(w http.ResponseWriter, r * http.Request) {
	mu.Lock()
	fmt.Fprintf(w, "Count %d\n", count)
	mu.Unlock()
}
