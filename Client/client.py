#!/usr/bin/env python3
import xmlrpc.client

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:9000")
    proxy.add_worker()


if __name__ == '__main__':
    main()