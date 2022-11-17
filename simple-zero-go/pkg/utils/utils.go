package utils

import "encoding/xml"

func If[T any](cond bool, trueVal T, falseVal T) T {
	if cond {
		return trueVal
	} else {
		return falseVal
	}
}

func ToXml(o any) (string, error) {
	bytes, err := xml.Marshal(o)
	return string(bytes), err
}
