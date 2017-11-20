# Winston III

Open source virtual assisstant written for NLP (Notre Dame
[CSE-40657][class site]) semester project.

## Architecture

At the highest level, Winston is divided into a server and clients.
The server sits on a single node, such as a raspberry pi, and
dispatches commands for any number of connected clients.

Winston clients connect to a server over a TCP socket and sends
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

[class site][https://www3.nd.edu/~dchiang/teaching/nlp/2017]
[google speech][https://cloud.google.com/speech]
[pocketsphinx][http://www.speech.cs.cmu.edu/pocketsphinx]
