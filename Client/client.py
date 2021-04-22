#!/usr/bin/env python3
import xmlrpc.client
import argparse

import dill

def countingWords(text):
    return len(text.split())

def reduceCounting(listText):
    mapped = map(lambda string: int(string), listText)
    reduced = 0
    for elem in list(mapped):
        reduced += elem
    return reduced

def wordCount(text):
    myMap = {}
    for word in text.split():
        if word in myMap:
            myMap[word] += 1
        else:
            myMap[word] = 1
    return myMap

def reduceWordCount(listText):
    myMap = {}
    for elem in listText:
        for key, value in elem.items():
            if key in myMap:
                myMap[key] += value
            else:
                myMap[key] = value
    return myMap

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:9000")

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
        proxy.removeWorker(argument.del_id)
        return

    if hasattr(argument, "workercmd") and argument.workercmd == "create":
        proxy.addWorker()
        return

    if hasattr(argument, "workercmd") and argument.workercmd == "list":
        print(proxy.listWorkers())
        return

    if hasattr(argument, "jobcmd") and argument.jobcmd == "run-wordcount":
        serWordCount = dill.dumps(wordCount)
        serReduceWordCount = dill.dumps(reduceWordCount)
        taskID = proxy.submitTaskGroup("a", serWordCount, argument.links, serReduceWordCount)
        jobid, res = proxy.getTaskResult(taskID)
        print("Task:", jobid, "=", res)
        return

    if hasattr(argument, "jobcmd") and argument.jobcmd == "run-countwords":
        serCountingWords = dill.dumps(countingWords)
        serReduceCountingWords = dill.dumps(reduceCounting)
        taskID = proxy.submitTaskGroup("a", serCountingWords, argument.links, serReduceCountingWords)
        jobid, res = proxy.getTaskResult(taskID)
        print("Task:", jobid, "=", res)
        return


if __name__ == '__main__':
    main()