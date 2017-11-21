# Winston III

Open source virtual assisstant written for NLP (Notre Dame
[CSE-40657][class site]) semester project.

## Architecture

At the highest level, Winston is divided into a server and clients.
The server sits on a single node, such as a raspberry pi, and
dispatches commands for any number of connected clients.

Winston clients connect to a server over a TCP socket and send
commands over that socket. For instance, the CLI client reads
sentences from `stdin` and sends them to the server. The speech
client, on the other hand, listens on the client host's microphone
for commands, pipes them through a speech recognition engine
(defaults to the [Google cloud speech API][google speech], can use
[pocketsphinx][pocketsphinx] if the system supports it). In the
future, I may provide a Web client or an SMS client via Twilio.

Looking back at the server, the concerns of handling connections
and executing command actions are separated between the Winston
server and Winston services respectively. Services are classes
which fit a loose contract; the need only determine how likely it
is that a command applies to them, and be able to handle a command
it claims to know. Services can be plugged in and out via the
server configuration file and you can think of them like the
"skills" of other virtual assistants.


## Server Configuration

The following options can be set via a YAML or JSON configuration
file (just make sure your file extension matches) (types and
default values shown).

```python
# Hostname/ IP address for server bind call
host: str = 'localhost'

# Port on which to listen for incoming connections
port: int = 4000

# Path to service package, relative to runtime WD
services_root: str = 'winston.services'

# List of services to support. Give the names of the target
# modules from the services package.
services: List[str] = ['music', 'reminders', 'search']
```

## Client Usage

The Winston system was designed to be very flexible in terms of
client interaction; communication happens over a regular old socket
so it doesn't much matter to the server who's on the other end.

That being said, most of the bookkeeping and utility functions
needed for robust and easy interaction with the server are
provided by a base client class, `Client`, located in
`winston.client.baseclient`. To create a new client, you need only
inherit from `Client` and provide `getinput` and `putoutput`
methods (failing to define these in the child class will result in
a `TypeError` at runtime. See [`@abc.abstractmethod`][abstract] for
details).

Two examples of this practice are provided at
`winston.client.exapmles`: `cli` and `speech`, the first of which
provides an interactive shell for communicating with the server,
and the second of which provides a speech interface (STT and TTS)
to users. They can be invoked as follows:

```
$ python3 -m winston.client.examples.cli --help
```

Or:


```
$ python3 -m winston.client.examples.speech --help
```

End users can easily create their own custom clients using the
Winston Client Builder (WIP). The Client Build is a command line
tool which exposes a suite of input-getter and output-putter
functions which can be mixed and matched to create a very unique
client. For instance, you can create a client with keyboard input
and speech output. **Future plans** include chaining input-getters
and output-putters so that a single client might accept both
keyboard and speech input and be able to report on multiple
channels.

[class site]: https://www3.nd.edu/~dchiang/teaching/nlp/2017
[google speech]: https://cloud.google.com/speech
[pocketsphinx]: http://www.speech.cs.cmu.edu/pocketsphinx
[abstract]: https://docs.python.org/3/library/abc.html?highlight=abstractmethod#abc.abstractmethod
