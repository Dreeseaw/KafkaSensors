# Numina » Take-Home Project for Backend Software Engineer Candidates

## Guidelines
Before we dive into the problem, let's discuss some guidelines.

#### You don't need to "finish" the project.
We don't expect you to spend more than 4 hours on this, and it’s fine if you don’t complete all the objectives (really!). In fact, we care much less about the end result being complete than about how you approach the work. So even if you don't finish, you should make sure that the path to completion - the steps you _would_ take if you had more time - is clear. For example, you could create a to-do list, an informal project plan, or a GitHub project board.

#### You don't need to be an expert in everything.
We know that everyone has strengths and weaknesses; that’s why we collaborate as a team. Don’t feel that every aspect of the project needs to be amazing; it doesn’t. This isn’t a competition and no one can win or lose, pass or fail. The goal is for us to evaluate where you are _right now_ and to experience what it’s like to work with you on a project. So just try to meet the requirements and move on.

#### Treat this like a real project.
Treat this project as if it will eventually go to production and your co-workers will need to maintain it. Please document all components just as you would with a normal project. Add the components and documentation to this git repository, commit regularly with descriptive messages, and push to GitHub regularly.

#### Make it easy on yourself.
Feel free to use any programming language(s), libraries, frameworks, databases, etc. of your choosing. We suggest you use whatever you’re most familiar with. The program interface can be the command-line or any other interface you prefer, whatever is easiest and quickest for you.

#### Communicate with us.
Treat this like any normal project: it’s "open book," so use whatever resources you like and don’t hesitate to ask us any and all questions that come to mind. Right now, the best way to ask questions is by email. You will be given email addresses of all the relevant team members.

## Problem

Great, now that you understand the guidelines, here's the problem!

We need an application to compute and display near real-time metrics about travelers (pedestrians, bicyclists, and vehicles) moving within a city. The movement events - travelers moving through a public space — come from a [Kafka](https://kafka.apache.org/) topic. We suggest you build a local database of metrics.

## Deliverables

Please deliver:

1. A program that:
    * Reads events from the Kafka topic
    * Derives metrics (see below) from the events and stores them in a database
1. An interface that:
    * Displays the current value of each metric, updated every minute
    * BONUS: Plots the metrics over time

### Metrics
Please compute, store, and display each metric at 1 minute intervals. Make sure metrics can be aggregated by sensor, traveler type, or both.

* Counts: How many total travelers have been detected in a period of time
* Speeds: What is the average, minimum, and maximum speed of travel in a given period of time

## Definitions

### Traveler
A traveler is an object that changes its position over time. Travelers are either pedestrians, bicyclists, or vehicles. Our knowledge about a traveler only lasts for as long as a sensor can detect it.

### Sensor
A sensor is a device that detects travelers and determines their position. Sensors are identified by a unique `sensor_id`. A sensor can determine the position of each traveler within its own distinct field of view.

### Position
The sensor detects the position of travelers in its field of view, which is a 100 foot x 100 foot square. Positions are described by `[x,y]` coordinates, where  `x` and `y` are between `0` and `100`.

### Movements

A movement event is created any time a sensor detects a traveler. The movement event contains the unique `sensor_id` and `traveler_id`, the `traveler_type` (pedestrian, bicyclist, or vehicle), and the `position` and `timestamp` of the traveler detection.

Movement events are published to a "Kafka topic" called `movements`. Records in this topic are stringified JSON objects.

```json
{
  "sensor_id": "integer",
  "traveler_id": "string",
  "traveler_type": "string",
  "position": ["float","float"],
  "timestamp": "datetime"
}
```

## Setup
The instructions below were tested on MacOS but should also work on Linux or Windows. We have provided a `docker-compose.yml` file that should get you up and running quickly. Alternatively, you can follow the steps below to get everything running separately on your own.

### Kafka Broker

1. Download, install, and start ZooKeeper and Kafka by:
   1. Following steps 1–3 in the
   [Confluent Platform Quickstart](http://docs.confluent.io/current/quickstart.html)
   1. If you’re proficient with [Docker](https://www.docker.com) and prefer to use it, see the
      [Confluent Docker Images](http://docs.confluent.io/current/cp-docker-images/docs/index.html)
    1. [RECOMMENDED] If you’re proficient with [Docker Compose](https://docs.docker.com/compose/) we have provided a `docker-compose.yml` file that should help you get up and running quickly. Note that this also runs the Sensor Simulator (see below) with default parameters at the same time.
2. The Kafka broker is now up and running and accessible on `localhost` at port `9092`

### Sensor Simulator

The Sensor Simulator will generate and produce events to the `movements` topic. You can start and stop it at your convenience to generate and populate data that your program will consume.

#### Requirements

1. [Python 3.8](https://www.python.org/)
1. [The confluent-kafka Python package](https://github.com/confluentinc/confluent-kafka-python)
1. [The Numpy Python package](http://www.numpy.org/)

#### Starting and Stopping

You can start the simulator with `python simulator/sensor_simulator.py` and stop it with `ctrl-c`.

The simulator supports various options; pass `--help` for usage information.
