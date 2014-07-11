remindme
========

[![Build Status](https://travis-ci.org/GochoMugo/remindme.svg?branch=master)](https://travis-ci.org/GochoMugo/remindme)

If only our brains were like computers, we wouldn't have problems remembering even the small things. But sadly we aren't!

Some time ago: *(adding a short remindme note...)*

```bash
$ remindme -a Formula For Water
Enter what you remember now:

> I must not forget the formula for Water, but if I do, please tell me about it. It is H20. Right?

```

Some time to come: *(remembering...)*

```bash
$ remindme Formula For Water

RemindMe reminding you:

I must not forget the formula for Water, but if I do, please tell me about it. It is H20. Right?

```

## Get Started ##

**Installing**:

`$ pip install remindme`

**Upgrading**:

`$ pip install upgrade remindme`

## Usage ##

```bash

usage: remindme [-h] [-l] [-a keywords [keywords ...]] [-r REMOVE [REMOVE ...]]
                          [-v]
                          [KEYWORDS [KEYWORDS ...]]

Reminds you of something you knew before

positional arguments:
  KEYWORDS              Keyword to remind me something I knew

optional arguments:
    -h, --help           show this help message and exit
    -l, --list          list all RemindMe keywords
    -a keywords [keywords ...], --add keywords [keywords ...]
                          add new RemindMe content
  -r REMOVE [REMOVE ...], --remove REMOVE [REMOVE ...]
                          remove a RemindMe
    -v, --version      show program's version number and exit

```

## Version Information ##

|Aspect|Detail|
|-------|------:|
|Version| 0.0.1|
|Python|2.6, 2.7, 3.2, 3.3, 3.4|
|Last Upgrade|11th July, 2014|

## More ##

If you find a bug, please create an [issue][issues] and I (with you, ofcourse) will get it fixed, won't we? 

## License ##

The Application and its Source Code is issued under the [MIT License].

[issues]:https://github.com/GochoMugo/remindme/issues "Create an Issue"
[MIT License]:https://github.com/GochoMugo/remindme/blob/master/LICENSE "MIT License"
