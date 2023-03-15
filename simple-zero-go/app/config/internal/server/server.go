package server

import (
	"context"
	"github.com/google/wire"
	"net"
	"net/http"
	"net/url"
)

var ProvideSet = wire.NewSet(
	NewEtcdClient,
	NewEtcdRegister,
	NewHttpServer,
)

type Server interface {
	Start(context.Context) error
	Stop(context.Context) error
}

type HttpServer struct {
	http.Server
	BaseContext context.Context
	endpoint    *url.URL
}

func (h *HttpServer) Endpoint() (*url.URL, error) {
	if h.endpoint != nil {
		return h.endpoint, nil
	}
	realAddr, err := h.Extract()
	if err != nil {
		return nil, err
	}
	h.endpoint = &url.URL{Scheme: "http", Host: realAddr}
	return h.endpoint, nil
}

func (h *HttpServer) Start(ctx context.Context) error {
	h.BaseContext = ctx
	return h.ListenAndServe()
}

func (h *HttpServer) Stop(ctx context.Context) error {
	return h.Shutdown(ctx)
}

func (h *HttpServer) Extract() (string, error) {
	addr, port, err := net.SplitHostPort(h.Addr)
	if err != nil {
		return "", err
	}
	if len(addr) > 0 && (addr != "0.0.0.0" && addr != "[::]" && addr != "::") {
		return net.JoinHostPort(addr, port), nil
	}
	ifaces, err := net.Interfaces()
	if err != nil {
		return "", err
	}
	lowest := int(^uint(0) >> 1)
	var result net.IP
	for _, iface := range ifaces {
		if (iface.Flags & net.FlagUp) == 0 {
			continue
		}
		if iface.Index < lowest || result == nil {
			lowest = iface.Index
		} else if result != nil {
			continue
		}
		addrs, err := iface.Addrs()
		if err != nil {
			continue
		}
		for _, rawAddr := range addrs {
			var ip net.IP
			switch addr := rawAddr.(type) {
			case *net.IPAddr:
				ip = addr.IP
			case *net.IPNet:
				ip = addr.IP
			default:
				continue
			}
			if isValidIP(ip.String()) {
				result = ip
			}
		}
	}
	if result != nil {
		return net.JoinHostPort(result.String(), port), nil
	}
	return "", nil
}

func isValidIP(addr string) bool {
	ip := net.ParseIP(addr)
	return ip.IsGlobalUnicast() && !ip.IsInterfaceLocalMulticast()
}
