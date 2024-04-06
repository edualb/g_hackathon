package templates

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

// DO NOT DELETE THIS FILE
// This file is important to help us generating code for translation.

var dummy = map[string]interface{}{}

func PrintDummy() {
	s := "ravencardDefaultTranslation = map[string]string{\n"

	full := []string{}
	for k := range dummy {
		/* Current result */
		// if strings.HasPrefix(k, "{%d [") {
		// 	continue
		// }
		// if strings.HasSuffix(k, "#FBFB79}") {
		// 	continue
		// }
		// full = append(full, fmt.Sprintf("\"%s\": \"\",", k))

		/* Spell Translation */
		re := regexp.MustCompile(`\[[^\[\]]*?\]`)
		matches := re.FindAllStringSubmatchIndex(k, -1)
		for _, m := range matches {
			percentage := k[m[0]:m[1]]
			percentage = percentage[1 : len(percentage)-1]
			percentageF, err := strconv.ParseFloat(percentage, 64)
			if err != nil {
				os.Exit(1)
			}
			percentageF = percentageF * 100
			result := strings.Replace(k, fmt.Sprintf("{%%d %s", k[m[0]:m[1]]), fmt.Sprintf("%.1f%%", percentageF), 1)
			resultSplitted := strings.Split(result, ",")
			full = append(full, fmt.Sprintf("\"%s\": \"%s\",", k, resultSplitted[0]))
		}

		/* Default Translation */
		// kSplitted := strings.Split(k, ",")
		// full = append(full, fmt.Sprintf("\"%s\": \"%s\",", k, kSplitted[0][1:]))

		/* Ravencard Special Translation */
		// kSplitted := strings.Split(k, ",")
		// full = append(full, fmt.Sprintf("\"%s\": func(s Scale) string {\n\t\tbuff := s.Base + s.Increment\n\t\treturn fmt.Sprintf(\"%s\", buff)\n\t},", k, kSplitted[0][1:]))
	}
	keys := strings.Join(full, "\n")

	fmt.Printf("%s%s\n}", s, keys)
}
