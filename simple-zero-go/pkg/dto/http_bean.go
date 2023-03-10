package dto

type AnyObj interface{}
type RespObj struct {
	Code int32
	Msg  string
	Data AnyObj
}

func (respObj *RespObj) code(code int32) *RespObj {
	respObj.Code = code
	return respObj
}

func (respObj *RespObj) msg(msg string) *RespObj {
	respObj.Msg = msg
	return respObj
}

func (respObj *RespObj) data(data AnyObj) *RespObj {
	respObj.Data = data
	return respObj
}
