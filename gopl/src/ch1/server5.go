// For practice 1.12
package main

import (
	"fmt"
	"log"
	"net/http"
	"image"
	"image/color"
	"image/gif"
	"io"
	"math"
	"math/rand"
	"strconv"
)

var palette = []color.Color{color.White, color.Black}

const (
	whiteIndex = 0    // first color in palette
	blackIndex = 1    // next color in palette
)

func main() {
	http.HandleFunc("/", handler)
	fmt.Println("start http server")
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}

// Handler echoes the Path component of the request URL r.
func handler(w http.ResponseWriter, r * http.Request) {
	vars := r.URL.Query();
	var cycles float64 = 5
	var freq float64 = 2
	cycles_string, ok := vars["cycles"]
	if ok {
		cycles, _ = strconv.ParseFloat(cycles_string[0], 64);
	}
	freq_string, ok := vars["freq"]
	if ok {
		freq, _ = strconv.ParseFloat(freq_string[0], 64);
	}
	lissajous(w, cycles, freq)
}

func lissajous(out io.Writer, cycles float64, freq float64) {
	const (
		res = 0.001   // angular resolution
		size = 100    // image canvas convers [-size..+size]
		nframes = 64  // number of animation frames
		delay = 8     // delay between frames in 10ms units
	)

	anim := gif.GIF{LoopCount: nframes}
	phase := 0.0    // phase difference
	for i := 0; i < nframes; i++ {
		rect := image.Rect(0, 0, 3*size+1, 2*size+1)
		img := image.NewPaletted(rect, palette)
		for t := 0.0; t < cycles*2*math.Pi; t += res {
			x := math.Sin(t)
			y := math.Sin(t*freq+phase)
			img.SetColorIndex(size+int(x*size+0.5), size+int(y*size+0.5),
			blackIndex)
		}
		phase += 0.1
		anim.Delay = append(anim.Delay, delay)
		anim.Image = append(anim.Image, img)
	}
	gif.EncodeAll(out, &anim)    // NOTE: ignoring encoding errors
}
