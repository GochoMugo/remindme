remindme
========

[![Build Status](https://travis-ci.org/GochoMugo/remindme.svg?branch=master)](https://travis-ci.org/GochoMugo/remindme)

If only our brains were like computers, we wouldn't have problems remembering even the small things. But sadly we aren't!

**Some time ago**: *(adding a short remindme note...)*

```bash
$ remindme -a Formula For Water
Enter what you remember now:

> I must not forget the formula for Water.
>
> But if I do, please tell me about it.
> It is H20. Right?
> :end

```

> **Note:** When you are finished editing the remindme, you need to type `:end` in a newline to exit. You might also use `Cmd`/`Ctrl` + `C` (keyboard interrupt) to exit editing.

**Some time to come**: *(remembering...)*

```bash
$ remindme Formula For Water

RemindMe reminding you:

I must not forget the formula for Water.

But if I do, please tell me about it.
It is H20. Right?

```

## Get Started ##

**Installing**:

`$ pip install remindme`

**Upgrading**:

`$ pip install --upgrade remindme`

** Documentation **

Usage and Help information may be found [here][gh-pages]

## Usage ##

```bash

usage: remindme [-h] [-l] [-a keywords [keywords ...]] [-r REMOVE [REMOVE ...]]
                          [-v]
                          [KEYWORDS [KEYWORDS ...]]

Reminds you of something you knew before

positional arguments:
  KEYWORDS              Keyword to remind me something I knew

optional arguments:
    -h, --help          show this help message and exit
    -l, --list          list all RemindMe keywords
    -a keywords [keywords ...], --add keywords [keywords ...]
                        add new RemindMe content
    -r REMOVE [REMOVE ...], --remove REMOVE [REMOVE ...]
                        remove a RemindMe
    -v, --version       show program's version number and exit

```

## Version Information ##

|Aspect|Detail|
|-------|------:|
|Version| 0.1.0|
|Python|2.6, 2.7, 3.2, 3.3, 3.4|
|Last Upgrade|2nd August, 2014|

## Contributtion ##

If you find a bug, please create an [issue][issues] and I (with you, ofcourse) will get it fixed, won't we?

Waiting so much for your Pull Request. :-)

Contributors:
1. [GochoMugo](https://github.com/GochoMugo)
2. [Low Kian Seong](https://github.com/lowks)

## License ##

The Application and its Source Code is issued under the [MIT License].


[gh-pages]:https://gochomugo.github.io/remindme "Remindme Home page"
[issues]:https://github.com/GochoMugo/remindme/issues "Create an Issue"
[MIT License]:https://github.com/GochoMugo/remindme/blob/master/LICENSE "MIT License"
