package app

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/edualb/ghackathon/internal/scrap"
)

type RavendawnSkillExtractor struct {
	URL string
}

func (app RavendawnSkillExtractor) Run() error {
	archetypes, err := scrap.RavendawnBuild(app.URL)
	if err != nil {
		return err
	}
	for _, a := range archetypes {
		data, err := json.Marshal(a)
		if err != nil {
			return err
		}
		file, err := os.OpenFile(fmt.Sprintf("./data/%s.json", strings.ToLower(a.Name)), os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			file.Close()
			return err
		}
		_, err = file.Write(data)
		if err != nil {
			file.Close()
			return err
		}
		file.Close()
	}
	return nil
}
