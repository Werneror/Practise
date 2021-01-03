package main

import (
	"html/template"
	"log"
	"os"
)

func main() {
	var t = template.Must(template.New("it").Parse(`
<h1>{{.Whoami}}</h1>
<h2>{{.Signature}}</h2>
	`))

	var data struct {
		Whoami string
		Signature template.HTML
	}

	data.Whoami = "Werner<script>alert(1)</script>"
	data.Signature = "Try Harder<script>alert(1)</script>"

	if err := t.Execute(os.Stdout, data); err != nil {
		log.Fatal(err)
	}
}
