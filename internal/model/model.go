package model

type Archetype struct {
	ID       int       `json:"id"`
	Name     string    `json:"name"`
	Passives []Passive `json:"passives"`
	Spells   []Spell   `json:"spells"`
}

type Passive struct {
	Name        string `json:"name"`
	Description string `json:"description"`
}

type Spell struct {
	ID          int         `json:"id"`
	Cost        int         `json:"cost"`
	Name        string      `json:"name"`
	Cooldown    float64     `json:"cooldown"`
	Channeling  bool        `json:"channeling"`
	Range       int         `json:"range"`
	Description string      `json:"description"`
	Mana        string      `json:"mana"`
	RavenCards  []Ravencard `json:"ravencards"`
}

type Ravencard struct {
	ID          int     `json:"id"`
	Name        string  `json:"name"`
	Description string  `json:"description"`
	Base        float64 `json:"base"`
	Increment   float64 `json:"increment"`
}
