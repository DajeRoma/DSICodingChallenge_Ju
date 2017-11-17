DSI Coding Challenge
====================

Thank you for considering Pioneer! This challenge will hopefully offer you a chance to demonstrate your skills and experience before the phone screen and scheduled in-person interview where we'll ask you quite a few things about your solutions, in addition to the usual interview-y things. If you're invited to an in-person interview, please bring your laptop!

We hope that the requirements are clear but please [email us](mailto:mailto:nikhil.anand@pioneer.com) in case you need any clarification.

Before you get started
----------------------

* The challenge consists of five parts. We'll tell you which parts to finish at a minimum, but feel free to complete all five.
* Unless asked to, implement your solutions in whatever you're comfortable with. If we're looking for something specific (e.g. Python, C#, Java, AngularJS, React, Postgres, AWS, whatever) we'll let you know.
* Please fork this repo and place your solutions, as a single repo, in your GitHub account. [Provide us](mailto:nikhil.anand@pioneer.com) a link when you're done.
* How you organize your solutions in your repo is up to you. Use it as a chance to demonstrate your VCS experience and hygiene.

Requirements
------------

You'll be designing a RESTful API that allows its clients to search through the datafile `data/canada_usa_cities.tsv` in this repository which contains a big list of cities in the United States and Canada. All parts entail a single-endpoint exposed at `/cities`.  It should return _at most_ 25 matches based on simple search criteria. Content-type should be `application/json` with the appropriate HTTP status code.

All requirements are provided as a bare minimum. Feel free to fill in (and document) anything missing. How you handle any edge/test/unusual cases that aren't specified here is entirely up to you.

### Part One - Simplicity Itself

Your API _only_ searches for _exact_ matches under the `name` field in the datafile.

```
GET /cities/Des Moines
```

should yield this

```json
{
  "city": "Des Moines",
  "state": "IA",
  "country": "US",
  "alternate_names": [
    "DSM",
    "De Moinas",
    "De Mojn",
    "De Moyn",
    "De-Mojn",
    "Dehs Mojns",
    "Demoina",
    "Des Moines",
    "Gorad Deh-Mojn",
    "Monachopolis",
    "Nte Moin",
    "de mei yin",
    "de mo'ina",
    "demoin",
    "dh mwyn",
    "di mo'ina",
    "di mxyn",
    "dimoin",
    "dy mwyn",
    "aywa",
    "dy mwyn",
    "aywwa",
    "ti moyin",
    "Ντε Μόιν",
    "Горад Дэ-Мойн",
    "Де Мойн",
    "Де Мојн",
    "Де-Мойн",
    "Дэс Мойнс",
    "Դե Մոյն",
    "דה מוין",
    "دي موين، آيوا",
    "دی موین، آیووا",
    "ڈس موئنس",
    "दि मोइन",
    "दे मॉईन",
    "டி மொயின்",
    "ดิมอยน์",
    "デモイン",
    "德梅因",
    "디모인"
  ],
  "latitude": 41.60054,
  "longitude": -93.60911
}
```

### Part Two - Getting Fuzzy

```
GET /cities?like=Des Moines
```

should yield this

```
{
  "cities": [
    {
      "city": "Des Moines",
      "state": "IA",
      "country": "US",
      "latitude": 41.60054,
      "longitude": -93.60911
      "alternate_names": List[<String>] // List of alternate names from Part One,
    },
    {
      "city": "West Des Moines",
      "state": "IA",
      "country": "US",
      "latitude": 41.57199,
      "longitude": -93.74531,
      "alternate_names": List[<String>]
    }
  ]
}
```

Hint: this doesn't _have_ to be a boring substring match like shown above...

### Part Three - Where things get interesting

Here are all the query params that your endpoint should accept. Feel free to add any you think are missing.

|    Param    |                                   Required                                   |
| ----------- | ---------------------------------------------------------------------------- |
| `like`      | Only if specific resource name (e.g. `/cities/Des Moines`) is not provided   |
| `latitude`  | Only if `longitude` specified. Ignore if specific resource name is provided. |
| `longitude` | Only if `latitude` specified. Ignore if specific resource name is provided.                                                 |

In this iteration, your solution should

* Present _up to 25 cities_ that fuzzy-match the `like` parameter.
* If `latitude` and `longitude` are specified, should find the 'closest' matches to this location.
* Whether or not `latitude` and `longitude` are provided, should display a 'relevance score', between 0.00 and 1.00 (inclusive) up to two places of decimal (two places always), based on some assessment of the results in a new `score` field for each entity in the `cities` list.

Relevance (the `score` field) is a function of a minimum of one or a maximum of two factors:

1. The search term's **similarity** to an actual city's name (hint: how could you quantify this?) and
2. Its location as determined by its **proximity** to the supplied `latitude` and `longitude` query params (if provided.)

That's the definition. How you weight them and determine a scoring algorithm is up to you. Be prepared to explain it. Doesn't have to be super fancy :)

Here's an example **which is just for guidance** since your algorithm will most certainly yield different `score`s. Let's say I'm looking for all cities with "des" in their name that are close to Chicago. Here's a sample result

```
GET /cities?like=des&latitude=41.85003&longitude=-87.65005
```

should yield something like

```
{
  "cities": [
    {
      "city": "Des Plaines",
      "state": "IL",
      "country": "US",
      "latitude": 42.03336,
      "longitude": -87.8834,
      "score": 0.95,
      "alternate_names": List[<String>] // Should still contain the alternate names from Part One!
    },
    {
      "city": "Des Moines,"
      "state": "IA,"
      "country": "US,"
      "latitude": 47.40177,
      "longitude": -122.32429,
      "score": 0.85,
      "alternate_names": List[<String>]
    },
    {
      "city": "Des Peres",
      "state": "MO",
      "country": "US",
      "latitude": 38.60089,
      "longitude": -90.4329,
      "score": 0.71,
      "alternate_names": List[<String>]
    },
    {
      "city": "Desloge",
      "state": "MO",
      "country": "US",
      "latitude": 37.87088,
      "longitude": -90.52735,
      "score": 0.70,
      "alternate_names": List[<String>]
    },
    {
      "city": "Destin",
      "state": "FL",
      "country": "US",
      "latitude": 30.39353,
      "longitude": -86.49578,
      "score": 0.64,
      "alternate_names": List[<String>]
    },
    {
      "city": "Destrehan",
      "state": "LA",
      "country": "US",
      "latitude": 29.94298,
      "longitude": -90.35175,
      "score": 0.56,
      "alternate_names": List[<String>]
    },
    {
      "city": "Desert Hot Springs",
      "state": "CA",
      "country": "US",
      "latitude": 33.96112,
      "longitude": -116.50168,
      "score": 0.31,
      "alternate_names": List[<String>]
    },
    {
      "city": "Deschutes River Woods",
      "state": "OR",
      "country": "US",
      "latitude": 43.99151,
      "longitude": -121.35836,
      "score": 0.19,
      "alternate_names": List[<String>]
    }
  ]
}
```

Note: Results don't need to be sorted in order of relevance/`score` as shown above.

### Part Four - Put a face on it

Design a web-interface that interrogates your API and displays, _as you type_, the city suggestions on a map using the Google Maps API. Use any appropriate framework or library that makes your task easier. Be prepared to be asked about your choice of framework (if applicable) and build workflow regardless of your choice.

### Part Five - Take it to the Cloud!

Deploy your solution to a _public service or server_. We like AWS and would prefer seeing your solution there (you can use the free-tier.) However, Heroku, Google Cloud, Azure, Linode, your own server, are all acceptable. Be prepared to explain your deployment process.

### Part N - Be creative!

Have improvements to the requirements listed so far? Go ahead and implement them. Go bonkers. We'd _love_ to see any new features you can think of. Make sure you talk about them during the interview!

What We Value
-------------

We value simplicity, readability/maintainability, and testability so there's nothing left-field here. Like every other software shop, we love good

* Documentation
* Syntax
* Tests
* VCS practices
* Packaging and deployment practices

We value our developers' creativity. We understand that 'elegant' solutions might not be optimal and vice-versa.

Whatever you do, please be prepared to explain your design choices and accept and offer critique gracefully and with respect. We're all in this to learn and become better.

Ultimately, we're a research company that is very interested in _how you think about data_ and how you're able to unleash its utility to solve our problems with your creativity and skillset.

Good luck, and thank you for your time! Code away!
