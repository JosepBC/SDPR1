# High Performance Computing Cluster
In this exercise we've created a simple server that can perform any function with the API exposed.\
We've implemented as well a simple CLI and two simple functions that can be performed, word count and count words.
## Cluster
The packages needed by the cluster are described [here](Cluster/requirements.txt). To launch the cluster, use
```bash
python3 Cluster/runCluster.py  
```
### Web server
If you want to use a local webserver, launch the web server in the folder that you want it to be using the following comand
```bash
pyhton3 -m http.server  
```
## Client
The packages needed by the client are described [here](Client/requirements.txt).

For this example, two basic functions are implemented, word count and count words.
### Word count
Word count counts the total number of words of the input.
```python
wordCount("I love distributed systems")
```
Will output 4.
### Count words
Count words counts the number of times that a word appears in the input.
```python
countWords("foo foo var")
```
Will output
| Word     | Times  |
|:--------:|:------:|
| foo      | 2      |
| var      | 1      |

## Client CLI
The client CLI allows users to interact with the cluster, and allows the following actions
### Create worker
First of all the cluster must be populated with, at least, one worker
```bash
pyhton3 Client/client.py worker create
```
### List worker
Worker ids on the cluster can be listed using
```bash
pyhton3 Client/client.py worker list
```
### Delete worker
Workers on the cluster can be deleted using
```bash
pyhton3 Client/client.py worker delete [id]
```
### Run count words
Run the count words function 
```bash
python3 Client/client.py job run-countwords [url1, url2, ...]
```

### Run word count
Run the count words function 
```bash
python3 Client/client.py job run-wordcount [url1, url2, ...]
```