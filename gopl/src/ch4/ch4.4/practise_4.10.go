// go run practise_4.10.go repo:golang/go is:open json decoder
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

const IssuesURL = "https://api.github.com/search/issues"

type IssuesSearchResult struct {
	TotalCount int `json:"total_count"`
	Items      []*Issue
}

type Issue struct {
	Number    int
	HTMLURL   string `json:"html_url"`
	Title     string
	State     string
	User      *User
	CreatedAt time.Time `json:"created_at"`
	Body      string    // in Markdown format
}

type User struct {
	Login   string
	HTMLURL string `json:"html_url"`
}

// SearchIssues queries the GitHub issue tracker.
func SearchIssues(terms []string) (*IssuesSearchResult, error) {
	q := url.QueryEscape(strings.Join(terms, " "))
	resp, err := http.Get(IssuesURL + "?q=" + q)
	if err != nil {
		return nil, err
	}

	// We must close resp.Body on all execution paths.
	// (Chapter 5 presents 'defer', which makes this simpler.)
	if resp.StatusCode != http.StatusOK {
		resp.Body.Close()
		return nil, fmt.Errorf("search query failed: %s", resp.Status)
	}

	var result IssuesSearchResult
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		resp.Body.Close()
		return nil, err
	}
	resp.Body.Close()
	return &result, nil
}

func main() {
	result, err := SearchIssues(os.Args[1:])
	if err != nil {
		log.Fatal(err)
	}
	currentTime := time.Now()
	fmt.Printf("一个月内的：\n")
	for _, item := range result.Items {
		if currentTime.Sub(item.CreatedAt) < time.Duration(24*30*time.Hour) {
		fmt.Printf("#%-5d %s %9.9s %.55s\n",
			item.Number, item.CreatedAt.Format("2006-01-02 15:04:05"), item.User.Login, item.Title)
		}
	}
	fmt.Printf("一年内的：\n")
	for _, item := range result.Items {
		if currentTime.Sub(item.CreatedAt) < time.Duration(24*365*time.Hour) && currentTime.Sub(item.CreatedAt) >= time.Duration(24*30*time.Second) {
		fmt.Printf("#%-5d %s %9.9s %.55s\n",
			item.Number, item.CreatedAt.Format("2006-01-02 15:04:05"), item.User.Login, item.Title)
		}
	}
	fmt.Printf("一年及以上的：\n")
	for _, item := range result.Items {
		if currentTime.Sub(item.CreatedAt) > time.Duration(24*365*time.Hour) {
		fmt.Printf("#%-5d %s %9.9s %.55s\n",
			item.Number, item.CreatedAt.Format("2006-01-02 15:04:05"), item.User.Login, item.Title)
		}
	}
}
