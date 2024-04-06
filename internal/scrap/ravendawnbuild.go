package scrap

import (
	"fmt"
	"strings"

	"github.com/edualb/ghackathon/internal/model"
	"github.com/edualb/ghackathon/internal/templates"
)

type BuildBody struct {
	PageProps struct {
		Archetypes []struct {
			ID       int    `json:"id,omitempty"`
			Name     string `json:"name,omitempty"`
			Passives []struct {
				Name        string `json:"name"`
				Description struct {
					Format string `json:"format"`
				} `json:"description"`
			}
			Spells []struct {
				ID   int `json:"spellId,omitempty"`
				Cost int `json:"cost,omitempty"`
			} `json:"spells,omitempty"`
		} `json:"archetypes,omitempty"`
		Spells []struct {
			ID          int     `json:"id,omitempty"`
			Name        string  `json:"name,omitempty"`
			Cooldown    float64 `json:"cooldown,omitempty"`
			Channeling  bool    `json:"channeling,omitempty"`
			Range       int     `json:"range,omitempty"`
			Description struct {
				Format string `json:"format,omitempty"`
			} `json:"description,omitempty"`
			Cost struct {
				Mana []int `json:"mana,omitempty"`
			} `json:"cost,omitempty"`
		} `json:"spells"`
		Ravencards []struct {
			ID          int      `json:"id,omitempty"`
			Name        string   `json:"name"`
			Spells      []string `json:"spells"`
			Description struct {
				Text  string `json:"text,omitempty"`
				Scale []struct {
					Base      float64 `json:"base,omitempty"`
					Increment float64 `json:"increment,omitempty"`
				} `json:"scale,omitempty"`
			} `json:"description"`
		}
	} `json:"pageProps"`
}

func RavendawnBuild(url string) ([]model.Archetype, error) {
	body := &BuildBody{}
	err := getJSON(url, body)
	if err != nil {
		return nil, fmt.Errorf("getting JSON body: %w", err)
	}

	ravencards := map[string][]model.Ravencard{}
	for _, r := range body.PageProps.Ravencards {
		if len(r.Spells) > 1 {
			return nil, fmt.Errorf("more than one spell for card '%d: %s'", r.ID, r.Name)
		}

		desc := r.Description.Text
		if len(r.Description.Scale) >= 1 {
			scales := []templates.Scale{}
			for _, scale := range r.Description.Scale {
				scales = append(scales, templates.Scale{
					Base:      scale.Base,
					Increment: scale.Increment,
				})
			}
			desc, err = templates.RavencardDescription(templates.RavencardTranslation{
				Description: desc,
				Scales:      scales,
			})
			if err != nil {
				return nil, err
			}
		}
		rvc := model.Ravencard{
			ID:          r.ID,
			Name:        r.Name,
			Description: desc,
		}

		rvcs, ok := ravencards[strings.ToLower(r.Spells[0])]
		if !ok {
			ravencards[strings.ToLower(r.Spells[0])] = []model.Ravencard{rvc}
			continue
		}
		rvcs = append(rvcs, rvc)
		ravencards[strings.ToLower(r.Spells[0])] = rvcs
	}

	archetypes := []model.Archetype{}
	for _, a := range body.PageProps.Archetypes {
		arch := model.Archetype{
			ID:       a.ID,
			Name:     a.Name,
			Passives: []model.Passive{},
			Spells:   []model.Spell{},
		}

		for _, ap := range a.Passives {
			description, err := templates.PassiveDescription(strings.Replace(ap.Description.Format, "\n\n", " ", -1))
			if err != nil {
				return nil, err
			}
			passive := model.Passive{
				Name:        ap.Name,
				Description: description,
			}
			arch.Passives = append(arch.Passives, passive)
		}

		for _, as := range a.Spells {
			spell := model.Spell{}
			for _, s := range body.PageProps.Spells {
				// if strings.EqualFold(s.Name, "Deep Wound") {
				// if strings.ToLower(s.Name) == strings.ToLower("deep wounds") {
				// 	fmt.Println("Exists!")
				// }
				if as.ID == s.ID {
					spell.ID = s.ID
					spell.Cost = as.Cost
					spell.Name = s.Name
					spell.Channeling = s.Channeling
					spell.Range = s.Range
					spell.Cooldown = s.Cooldown / 1000
					spell.Description, _ = templates.SpellDescription(templates.SpellTranslation{
						Description: strings.Replace(s.Description.Format, "\n\n", " ", -1),
					})

					if s.Cost.Mana != nil {
						for _, m := range s.Cost.Mana {
							if spell.Mana == "" {
								spell.Mana = fmt.Sprintf("%d%%", m)
								continue
							}
							spell.Mana = fmt.Sprintf("%s, %d%%", spell.Mana, m)
						}
					}

					rcs, ok := ravencards[strings.ToLower(s.Name)]
					if !ok {
						return nil, fmt.Errorf("not found ravencard for spell '%s'", s.Name)
					}
					spell.RavenCards = rcs

					arch.Spells = append(arch.Spells, spell)
				}
			}
		}
		archetypes = append(archetypes, arch)
	}

	// templates.PrintDummy()

	// for _, v := range archetypes {
	// 	fmt.Printf("\n%d: %s\n", v.ID, v.Name)
	// 	for _, p := range v.Passives {
	// 		fmt.Printf("\t%s (Passive Skill)\n\t\tDescription: %s\n", p.Name, p.Description)
	// 	}
	// 	for _, s := range v.Spells {
	// 		if len(s.RavenCards) != 2 {
	// 			return nil, fmt.Errorf("spell '%d: %s' does not have two ravencards", s.ID, s.Name)
	// 		}
	// 		ravencard := ""
	// 		for _, r := range s.RavenCards {
	// 			ravencard = fmt.Sprintf("%sName: %s\n\t\t\t\tDescription: %s\n\t\t\t", ravencard, r.Name, r.Description)
	// 		}
	// 		fmt.Printf(
	// 			"\t%d: %s\n\t\tCost: %d\n\t\tCooldown: %.2f seconds\n\t\tChannel: %v\n\t\tRange: %d\n\t\tMana: %s\n\t\tDescription: %s\n\t\tRavencards:\n\t\t\t%s\n",
	// 			s.ID,
	// 			s.Name,
	// 			s.Cost,
	// 			s.Cooldown,
	// 			s.Channeling,
	// 			s.Range,
	// 			s.Mana,
	// 			s.Description,
	// 			ravencard,
	// 		)
	// 	}
	// }

	return archetypes, nil
}
