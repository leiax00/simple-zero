package server

import (
	clientV3 "go.etcd.io/etcd/client/v3"
	"google.golang.org/grpc"
	"log"
	"time"
)

var etcdC *clientV3.Client

func NewEtcdClient(addrs []string) *clientV3.Client {
	var err error
	etcdC, err = clientV3.New(clientV3.Config{
		Endpoints:   addrs,
		DialTimeout: time.Second,
		DialOptions: []grpc.DialOption{grpc.WithBlock()},
		Username:    "root",
		Password:    "lax4832.",
	})
	if err != nil {
		log.Fatalln("Failed to create etcd client: ", err)
	}
	return etcdC
}
