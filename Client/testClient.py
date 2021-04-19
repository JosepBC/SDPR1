#!/usr/bin/env python3
import xmlrpc.client
import base64
import dill

def CountingWords(text):
    print("Len=", len(text.split()))
    return len(text.split())

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:9000")
    proxy.addWorker()
    l = proxy.listWorkers()
    print("Workers: ", l)
    ser = dill.dumps(CountingWords)
    proxy.submitTask("ex", ser, "https://gist.githubusercontent.com/jsdario/6d6c69398cb0c73111e49f1218960f79/raw/8d4fc4548d437e2a7203a5aeeace5477f598827d/el_quijote.txt")

if __name__ == '__main__':
    main()