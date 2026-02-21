package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"net"
	"net/url"
	"os"
	"strings"
	"time"
)

type DNSInfo struct {
	Host string `json:"host"`
	IP   string `json:"ip"`
	PTR  string `json:"ptr"`
}

type WhoisInfo struct {
	Server string `json:"server"`
	Raw    string `json:"raw"`
}

type Output struct {
	DNS   DNSInfo   `json:"dns"`
	Whois WhoisInfo `json:"whois"`
}

func parseHost(target string) string {
	u, err := url.Parse(target)
	if err != nil || u.Host == "" {
		return target
	}
	h := u.Host
	if i := strings.Index(h, ":"); i >= 0 {
		h = h[:i]
	}
	return h
}

func resolve(host string) DNSInfo {
	var ipStr string
	var ptr string
	ips, err := net.LookupIP(host)
	if err == nil && len(ips) > 0 {
		ipStr = ips[0].String()
		names, err := net.LookupAddr(ipStr)
		if err == nil && len(names) > 0 {
			ptr = strings.TrimSuffix(names[0], ".")
		}
	}
	return DNSInfo{Host: host, IP: ipStr, PTR: ptr}
}

func whoisServer(host string) string {
	parts := strings.Split(host, ".")
	if len(parts) < 2 {
		return "whois.iana.org:43"
	}
	tld := strings.ToLower(parts[len(parts)-1])
	switch tld {
	case "com", "net":
		return "whois.verisign-grs.com:43"
	default:
		return "whois.iana.org:43"
	}
}

func whoisQuery(server, domain string, timeout time.Duration) string {
	conn, err := net.DialTimeout("tcp", server, timeout)
	if err != nil {
		return ""
	}
	defer conn.Close()
	_, _ = conn.Write([]byte(domain + "\r\n"))
	conn.SetReadDeadline(time.Now().Add(timeout))
	var b strings.Builder
	reader := bufio.NewReader(conn)
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			break
		}
		b.WriteString(line)
	}
	return b.String()
}

func main() {
	target := flag.String("target", "", "target URL or domain")
	timeout := flag.Int("timeout", 8, "timeout seconds")
	flag.Parse()
	if *target == "" {
		fmt.Fprintln(os.Stderr, "usage: go run main.go -target <url>")
		os.Exit(1)
	}
	host := parseHost(*target)
	dns := resolve(host)
	srv := whoisServer(host)
	raw := whoisQuery(srv, host, time.Duration(*timeout)*time.Second)
	out := Output{DNS: dns, Whois: WhoisInfo{Server: srv, Raw: raw}}
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	_ = enc.Encode(out)
}
