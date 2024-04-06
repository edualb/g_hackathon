package templates

import (
	"fmt"
	"sort"
	"strings"
)

type RavencardTranslation struct {
	Description string
	Scales      []Scale
}

type Scale struct {
	Base      float64
	Increment float64
}

func RavencardDescription(r RavencardTranslation) (string, error) {
	description := r.Description

	rawMatches := reTranslation.FindAllStringSubmatchIndex(description, -1)
	for _, m := range rawMatches {
		placeholder := r.Description[m[0]:m[1]]
		v, ok := defaultTranslation[placeholder]
		if !ok {
			_, ok := specialTranslation[placeholder]
			if ok {
				continue
			}
			return "", fmt.Errorf("key '%s' not found in the ravencard default translation", placeholder)
		}
		description = strings.Replace(description, placeholder, v, 1)
	}

	refinedDescription := description
	refinedMatches := reTranslation.FindAllStringSubmatchIndex(refinedDescription, -1)
	sort.SliceStable(refinedMatches, func(i, j int) bool {
		return refinedMatches[i][0] <= refinedMatches[j][0]
	})
	for i, m := range refinedMatches {
		placeholder := description[m[0]:m[1]]
		v, ok := specialTranslation[placeholder]
		if !ok {
			return "", fmt.Errorf("special key '%s' not found in the ravencard default translation", placeholder)
		}
		refinedDescription = strings.Replace(refinedDescription, placeholder, v(r.Scales[i]), 1)
	}

	return refinedDescription, nil
}

func PassiveDescription(description string) (string, error) {
	return SpellDescription(SpellTranslation{
		Description: description,
	})
}

type SpellTranslation struct {
	Description string
}

func SpellDescription(t SpellTranslation) (string, error) {
	description := t.Description
	rawMatches := reTranslation.FindAllStringSubmatchIndex(description, -1)
	for _, m := range rawMatches {
		placeholder := t.Description[m[0]:m[1]]
		v, ok := defaultTranslation[placeholder]
		if !ok {
			_, ok := percentageTranslation[placeholder]
			if ok {
				continue
			}
			return "", fmt.Errorf("key '%s' not found in the spell default translation", placeholder)
		}
		description = strings.Replace(description, placeholder, v, 1)
	}

	refinedDescription := description
	refinedMatches := reTranslation.FindAllStringSubmatchIndex(refinedDescription, -1)
	for _, m := range refinedMatches {
		placeholder := description[m[0]:m[1]]
		v, ok := percentageTranslation[placeholder]
		if !ok {
			return "", fmt.Errorf("key '%s' not found in the spell translation", placeholder)
		}
		refinedDescription = strings.Replace(refinedDescription, placeholder, v, 1)
	}

	return refinedDescription, nil
}
