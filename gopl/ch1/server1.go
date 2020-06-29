// Server1 is a minimal "echo" server.
package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", handler)
	fmt.Println("start http server")
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}

// Handler echoes the Path component of the request URL r.
func handler(w http.ResponseWriter, r * http.Request) {
	fmt.Fprintf(w, "URL.Path = %q\n", r.URL.Path)
}
