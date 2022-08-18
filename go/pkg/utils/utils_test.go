package utils

import "testing"

func TestIf(t *testing.T) {
	v := If(true, "23", "43")
	t.Log(v)
}
