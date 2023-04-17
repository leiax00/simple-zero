package server

import (
	"github.com/go-kratos/kratos/contrib/registry/etcd/v2"
	clientV3 "go.etcd.io/etcd/client/v3"
	"google.golang.org/grpc"
	"log"
	"time"
)

var etcdC *clientV3.Client

// NewEtcdClient
//
// etcdAddrList:  etcd集群连接地址的列表, etcd01;etcd02;...
func NewEtcdClient(etcdAddrList []string) *clientV3.Client {
	var err error
	etcdC, err = clientV3.New(clientV3.Config{
		Endpoints:   etcdAddrList,
		DialTimeout: time.Second,
		DialOptions: []grpc.DialOption{grpc.WithBlock()},
	})
	if err != nil {
		log.Fatalln("Failed to create etcd client: ", err)
	}
	return etcdC
}

func NewEtcdRegister(client *clientV3.Client) *etcd.Registry {
	return etcd.New(client, etcd.Namespace("app/serve"))

}
