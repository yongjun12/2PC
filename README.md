# Two-phases-commit

The second project in Distributed Computing: Two phases commit.

The first project is implemented in function in global scope, so I have to register all put, get, del functions for xmlrpc interface. 
Later after referring to some other students' work, I realized that a better way to build the system is through Class. For better organization, I implemented the system in Object-oriented programming. 

Another improvement is how the record is logged. In first project, the activities of both coordinator and replica are logged in SQLite tables.
This will create unnecessary overhead of database connection and insert/update request. In addition, database has the potentiality to crash,
which is bound to jeopardize the availability of logging information. Thereofore, in the second project, I use text file to keep track of coordinator/replica status. This should reduce the extra cost and chance of failure.

## Installation
##### Have to make sure the following tools available in both server and client machines. 

1. sqlite3
2. python
3. fabric

##### Have Fabric ready to streamline client processes. 
In this project, fabfile will be run on server machine for simplicity. 


## Environment Setup

1. vim coordinator.py, change relica_add to ip of replica that store the key-value pair
    ```
      replica_add = <ip of ther replica process>
    ```
2. Run coodinator.py in current work directory
  ```
    python coordinator.py
  ```
3. vim fabfile.py, set env.host to server ip and all replica ip
    ```
      env.hosts = [<server_ip>, <replica1_ip>, ..., <replicaN_ip>] 
    ```
4. vim fabfile.py, define server/replica roles
   ```
       env.roledefs.update({
       'server': [<server_ip>],
       'replica': [<replica1_ip>, ..., <replicaN_ip>]
       }) 
    ```
5. Run command `fab setup` to put the python files to replicas and create logs.
6. Now everything is up and running! Start your exploration!

## Code Structure

###### The project use built-in library xmlrpclib as an interface for server-client communication. Each machine, both server and multiple clients, has an independent database where key value and process status are logged. SQLite is introduced as the its advantage of being light-weight and easy installation. For better streamlining, fabric command-line tool is also injected in the project, simplifying the execution of python files in distributed machines.

1. Coordinator.py
   - commit: ask all replicas to commit changes
   - abort: ask all replicas to abort changes
   - get: fetch key value
   - put: update key value
   - delete: delete key 
   - recover: Checks log file to see if there are any entries without commit/abort action
   - main: create coordinator and set up port for incoming events, register the class coordinator.
   
2. replica.py
   - decide: to if see there are ongoing request 
   - get: fetch key value from sqlite3, if no value is received, return null
   - put: update key value in sqlite3
   - delete: delete key in sqlite3

3. fabfile.py
   - configure coordinator/replica address and appoint roles
   - identify login key and ssh_configure file
   - putFile: Put replica.py to a set of machines

