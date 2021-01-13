# Example Todo list application using CORBA

This is an example Todo list application, which uses
CORBA for communication between client and the server.

## Setup

Run `install.sh` to created python virtual environment and
download, install and compile dependencies.
```
$ ./install.sh
```

Activate virtualenv

```
$ source .venv/bin/activate
```

Set some additional environment variables required for omniORBpy

```
$ source environ
```

Generate skeletons and stubs using `omniidl`

```
$ omniidl -bpython todo.idl
```

Run OMNI name server (in a separate terminal)

```
$ omniNames
```

If you are running for the first time you may need to run
```
$ omniNames -start
```

Finally, run the server (in a separate terminal)
```
$ python3 server.py
```

Finally, and the client
```
$ python3 client.py
```



