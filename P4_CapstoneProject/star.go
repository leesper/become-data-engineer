package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"sync"
)

const (
	repoFile = "./repos/part-00000-3cae6868-1434-4213-be45-9596c62a7890-c000.txt"
	// repoFile = "./repos/test.txt"
)

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

func fetchStars(repos []string) {
	var wg sync.WaitGroup
	api := "https://api.github.com/repos/%s/stargazers"
	for idx, repo := range repos {
		wg.Add(1)
		i := idx
		r := fmt.Sprintf(api, repo)
		go githubAPI(i, r, &wg)
	}
	wg.Wait()
}

func githubAPI(i int, r string, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Printf("index %d: %s\n", i, r)
}

func main() {
	repos := readFile(repoFile)
	fmt.Printf("%d repositories to process\n", len(repos))
	fetchStars(repos)
}
