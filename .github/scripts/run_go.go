// Generic verification driver for a Go solution file.
//
// Go can't dynamically load a function with an arbitrary signature, so the
// convention here is: the solution file (package main, no `func main`)
// exports `func Solve(input map[string]any) any`, and this driver is
// compiled together with it.
//
// Usage:
//
//	go run .github/scripts/run_go.go <solution.go> <testcases.json>
//
// (go run compiles all leading .go file arguments together into one binary;
// the first non-.go argument, testcases.json, is passed through as os.Args[1].)
//
// testcases.json format:
//
//	[{"input": {"<field>": <value>, ...}, "expected": <value>}, ...]
//
// Prints one JSON line to stdout:
//
//	{"status": "passed"|"failed", "runtime_ms": <float>, "memory_kb": <float>, "details": "..."}
package main

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
	"reflect"
	"runtime"
	"strings"
	"time"
)

type testCase struct {
	Input    map[string]any `json:"input"`
	Expected any            `json:"expected"`
}

// normalize round-trips a value through JSON so ints/floats/slices/maps end
// up as the same generic types on both the actual and expected side.
func normalize(v any) any {
	b, err := json.Marshal(v)
	if err != nil {
		return v
	}
	var out any
	_ = json.Unmarshal(b, &out)
	return out
}

func roundTo(v float64, places int) float64 {
	mult := math.Pow(10, float64(places))
	return math.Round(v*mult) / mult
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: run_go.go <solution.go> <testcases.json>")
		os.Exit(2)
	}

	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	var cases []testCase
	if err := json.Unmarshal(data, &cases); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}

	var before, after runtime.MemStats
	runtime.GC()
	runtime.ReadMemStats(&before)
	start := time.Now()

	var failures []string
	for i, tc := range cases {
		actual := Solve(tc.Input)
		if !reflect.DeepEqual(normalize(actual), normalize(tc.Expected)) {
			failures = append(failures, fmt.Sprintf("case %d: expected %v, got %v", i, tc.Expected, actual))
		}
	}

	elapsedMs := float64(time.Since(start).Microseconds()) / 1000
	runtime.ReadMemStats(&after)
	memDeltaKB := float64(after.TotalAlloc-before.TotalAlloc) / 1024

	status := "passed"
	details := fmt.Sprintf("%d case(s) passed", len(cases))
	if len(failures) > 0 {
		status = "failed"
		details = strings.Join(failures, "; ")
	}

	result := map[string]any{
		"status":     status,
		"runtime_ms": roundTo(elapsedMs, 3),
		"memory_kb":  roundTo(memDeltaKB, 1),
		"details":    details,
	}
	out, _ := json.Marshal(result)
	fmt.Println(string(out))
	if status == "failed" {
		os.Exit(1)
	}
}
