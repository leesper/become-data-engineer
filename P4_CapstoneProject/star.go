package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

const (
	repoFile = "./repos/part-00000-3cae6868-1434-4213-be45-9596c62a7890-c000.txt"
	// repoFile = "./repos/test.txt"
)

// readFile reads repository infos from text file
func readFile(fn string) []string {
	f, err := os.Open(fn)
	defer f.Close()
	if err != nil {
		log.Fatalf("error: %s\n", err)
	}
	reader := bufio.NewReader(f)
	repos := []string{}
	for {
		bs, _, err := reader.ReadLine()
		if err == io.EOF {
			break
		}
		repos = append(repos, string(bs))
	}
	return repos
}

// fetchStars concurrently fetch starring history from GitHub API
func fetchStars(repos []string) {
	var wg sync.WaitGroup
	// rate limit: always keep 10 concurrent goroutines at the moment
	tokenBuckets := make(chan int, 10)
	// rate limit: wait for 1 second every 10 concurrent tasks
	tick := time.Tick(1 * time.Second)
	for idx, repo := range repos {
		i := idx
		r := repo
		// put a token in the bucket then run go-routines
		tokenBuckets <- i
		wg.Add(1)
		go githubAPI(i, r, &wg, tokenBuckets)
		if idx > 0 && idx%10 == 0 {
			<-tick
		}
	}
	wg.Wait()
}

func githubAPI(i int, r string, wg *sync.WaitGroup, buckets chan int) {
	// upon finished, get the token back, leave a place for the next task
	defer func() {
		<-buckets
	}()
	defer wg.Done()
	api := "https://api.github.com/repos/%s/stargazers"
	api = fmt.Sprintf(api, r)
	client := &http.Client{}
	req, err := http.NewRequest("GET", api, nil)
	if err != nil {
		log.Fatalf("error: %s\n", err)
	}
	req.Header.Add("Accept", "application/vnd.github.v3.star+json")
	req.Header.Add("Authorization", "token ebc2b6de279b38b2d88dbc233e1e55e00e42e597")
	rsp, err := client.Do(req)
	if err != nil {
		log.Fatalf("error: %s\n", err)
	}
	defer rsp.Body.Close()
	if rsp.StatusCode == http.StatusNotFound {
		return
	}
	body, err := ioutil.ReadAll(rsp.Body)
	if err != nil {
		log.Fatalf("error: %s\n", err)
	}
	jsonData := parseAndProcess(r, body)
	fn := strings.Replace(r, "/", "__", -1)
	err = ioutil.WriteFile(fmt.Sprintf("data/%s.json", fn), jsonData, 0644)
	if err != nil {
		log.Fatalf("error: %s\n", err)
	}
	fmt.Printf("index %d: %s finished\n", i, api)
}

func parseAndProcess(repo string, data []byte) []byte {
	type User struct {
		Login             string `json:"login"`
		ID                int    `json:"id"`
		NodeID            string `json:"node_id"`
		AvatarURL         string `json:"avatar_url"`
		GravatarID        string `json:"gravatar_id"`
		URL               string `json:"url"`
		HTMLURL           string `json:"html_url"`
		FollowersURL      string `json:"followers_url"`
		FollowingURL      string `json:"following_url"`
		GistsURL          string `json:"gists_url"`
		StarredURL        string `json:"starred_url"`
		SubscriptionsURL  string `json:"subscriptions_url"`
		OrganizationsURL  string `json:"organizations_url"`
		ReposURL          string `json:"repos_url"`
		EventsURL         string `json:"events_url"`
		ReceivedEventsURL string `json:"received_events_url"`
		Type              string `json:"type"`
		SiteAdmin         bool   `json:"site_admin"`
	}

	type Star struct {
		StarredAt string `json:"starred_at"`
		User      User   `json:"user"`
	}

	var stars []Star
	err := json.Unmarshal(data, &stars)
	if err != nil {
		log.Fatalf("error: %s\n", err)
	}

	type Record struct {
		Repo      string `json:"repo"`
		StarredAt string `json:"starred_at"`
		Login     string `json:"login"`
		ID        int    `json:"id"`
		NodeID    string `json:"node_id"`
		HTMLURL   string `json:"html_url"`
		Type      string `json:"type"`
		SiteAdmin bool   `json:"site_admin"`
	}

	jsonData := []byte{}
	// flatten the JSON data
	for _, star := range stars {
		var record Record
		record.Repo = repo
		record.StarredAt = star.StarredAt
		record.Login = star.User.Login
		record.ID = star.User.ID
		record.NodeID = star.User.NodeID
		record.HTMLURL = star.User.HTMLURL
		record.Type = star.User.Type
		record.SiteAdmin = star.User.SiteAdmin
		data, err := json.Marshal(record)
		data = append(data, []byte("\n")...)
		if err != nil {
			log.Fatalf("error: %s\n", err)
		}
		jsonData = append(jsonData, data...)
	}

	return jsonData
}

func main() {
	repos := readFile(repoFile)
	fmt.Printf("%d repositories to process\n", len(repos))
	fetchStars(repos)
}
