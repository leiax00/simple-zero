package common

import (
	"encoding/json"
	"errors"
)

type AnyObj struct {
	Value any
}

func (ao *AnyObj) Marshal() ([]byte, error) {
	return nil, errors.New("not implement")
}
func (ao *AnyObj) MarshalTo(data []byte) (n int, err error) {
	return 0, errors.New("not implement")
}
func (ao *AnyObj) Unmarshal(data []byte) error {
	return errors.New("not implement")
}
func (ao *AnyObj) Size() int {
	return -1
}

// MarshalJSON json序列化
func (ao *AnyObj) MarshalJSON() ([]byte, error) {
	return json.Marshal(ao.Value)
}

func (ao *AnyObj) UnmarshalJSON(data []byte) error {
	return json.Unmarshal(data, &ao.Value)
}

//// only required if the compare option is set
//func (t AnyObj) Compare(other T) int {}
//
//// only required if the equal option is set
//func (t AnyObj) Equal(other T) bool {}
//
//// only required if populate option is set
//func NewPopulatedT(r randyThetest) *AnyObj {}
