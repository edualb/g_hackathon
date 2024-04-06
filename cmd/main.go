package main

import (
	"fmt"
	"os"

	"github.com/edualb/ghackathon/internal/app"
)

const url = "https://build.ravendawn.online/_next/data/KxttLcCLi7DsXoR3ZgcV-/en/builder.json"

func main() {
	application := app.RavendawnSkillExtractor{
		URL: url,
	}
	err := application.Run()
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}
}
