#!/usr/bin/env python3
import xmlrpc.client

def CountingWords(text):
    #resp = requests.get(url)
    return len(text.split())

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:9000")
    proxy.addWorker()
    proxy.addWorker()
    l = proxy.listWorkers()
    print(l)
    proxy.submitTask("sad", "CountingWords", "asd")

if __name__ == '__main__':
    main()