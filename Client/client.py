#!/usr/bin/env python3
import xmlrpc.client
import argparse

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


    parser = argparse.ArgumentParser(description='Client')
    subparsers = parser.add_subparsers(help='sub-commnad-help', dest="cmd")

    parser_w = subparsers.add_parser("worker", help="Worker related items")
    parser_subW = parser_w.add_subparsers(help='sub-commnad-help', dest="workercmd")
    parser_subW.add_parser("create")
    del_parse = parser_subW.add_parser("delete") 
    del_parse.add_argument("del_id", type=int)
    parser_subW.add_parser("list")
    
    parser_j = subparsers.add_parser("job", help="Job related items")
    parser_subJ = parser_j.add_subparsers(help='sub-commnad-help', dest="jobcmd")
    wordCOunt = parser_subJ.add_parser("run-wordcount")
    wordCOunt.add_argument("links", type=str, nargs="+") 
    countWords = parser_subJ.add_parser("run-countwords")
    countWords.add_argument("links", type=str, nargs="+") 
    
    argument = parser.parse_args()

    if hasattr(argument, "workercmd") and argument.workercmd == "delete":
        #El argument de eliminar worker es argument.del_id 
        pass
    if hasattr(argument, "workercmd") and argument.workercmd == "create":
        #Llamar a la funcion de crear worker
        pass
    if hasattr(argument, "workercmd") and argument.workercmd == "list":
        #Llamar a la funcion de listar workers
        pass
    if hasattr(argument, "jobcmd") and argument.jobcmd == "run-wordcount":
        #Llamar a run-wordcount con el parametro argument.links
        pass

    if hasattr(argument, "jobcmd") and argument.jobcmd == "run-countwords":
        #Llamar a run-countwords con el parametro argument.links



if __name__ == '__main__':
    main()