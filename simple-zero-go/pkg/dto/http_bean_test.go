package dto

import (
	"encoding/json"
	"github.com/leiax00/simple-zero/api/common/v1"
	"testing"
)

func TestRespObj(t *testing.T) {
	type Demo struct {
		Name string `json:"name"`
	}
	var _ AnyObj = (*Demo)(nil)
	test := &RespObj{
		Code: int32(common.RespCode_FAIL.Number()),
		Msg:  "",
		Data: &Demo{Name: "leiax00"},
	}
	testStr, _ := json.Marshal(test)
	t.Logf("json=%+v", test)
	t.Logf("json=%s", testStr)
}
