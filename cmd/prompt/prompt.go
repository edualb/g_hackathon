package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/edualb/ghackathon/internal/model"
)

func main() {
	b, err := os.ReadFile("./data/warfare.json")
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}
	obj := model.Archetype{}
	err = json.Unmarshal(b, &obj)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}

	// fmt.Printf("* %s (Passive Skills):\n", obj.Name)
	// for _, p := range obj.Passives {
	// 	fmt.Printf("\t-\n\t\tpassive_name: %s\n\t\tskill_cost: 3\n\t\tpassive_description: %s\n",
	// 		p.Name,
	// 		p.Description,
	// 	)
	// }
	fmt.Printf("\n* %s (Skills):\n", obj.Name)
	for _, s := range obj.Spells {
		mana := s.Mana
		if s.Mana == "" {
			mana = "0%"
		}
		// fmt.Printf("\t\tskill_ravencards:\n")
		for _, r := range s.RavenCards {
			fmt.Printf("\t-\n\t\tskill_id: %d\n\t\tskill_name: %s\n\t\tskill_channeling: %v\n\t\tskill_mana_cost: %s\n\t\tskill_range: %d\n\t\tskill_cooldown: %.2fs\n\t\tskill_description: %s\n\t\tskill_buff_id: %d\n\t\tskill_buff: %s\n",
				s.ID,
				s.Name,
				s.Channeling,
				mana,
				s.Range,
				s.Cooldown,
				s.Description,
				r.ID,
				r.Description,
			)
			// fmt.Printf("\t\t\t-\n\t\t\t\travencard_id: %d\n\t\t\t\travencard_name: %s\n\t\t\t\travencard_description: %s\n", r.ID, r.Name, r.Description)
		}
	}
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
}
