
# remindme #

[![Build Status](https://travis-ci.org/GochoMugo/remindme.svg?branch=master)](https://travis-ci.org/GochoMugo/remindme)

If only our brains were like computers, we wouldn't have problems
 remembering even the small things. But sadly we aren't!

**Some time ago**: *(adding a short remindme note...)*

```bash
⇒ remindme -a Formula For Water
[runner]: Enter what you remember now?
> I must not forget the formula for Water.
>
> But if I do, please tell me about it.
> It is H20. Right?
> :end

```

> **Note:** When you are finished editing the remindme, you need
> to type `:end` in a newline to exit. You might also
> use `Cmd`/`Ctrl` + `C` (keyboard interrupt) to exit editing.


**Some time to come**: *(remembering...)*

```bash
⇒ remindme Formula For Water
[runner]: Reminding you:
1  I must not forget the formula for Water.
2
3  But if I do, please tell me about it.
4  It is H20. Right?

```


## Get Started ##

### Installing: ###

```bash
⇒  pip install remindme
```

### Upgrading: ###

```bash
⇒ pip install --upgrade remindme
```


## Documentation ##

Usage and Help information may be found [here][gh-pages]


## Usage ##

```bash

usage: remindme [-h] [-l] [-a title [title ...]] [-i title [title ...]]
              [-r title [title ...]] [-Ra] [-v]
              [TITLE [TITLE ...]]

Reminds you of something you knew before

positional arguments:
  TITLE                 Title for RemindMe

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            list all RemindMe titles
  -a title [title ...], --add title [title ...]
                        add new RemindMe
  -i title [title ...], --in title [title ...]
                        pipe-in input for a new remindme
  -r title [title ...], --remove title [title ...]
                        remove a RemindMe
  -Ra, --remove-all     remove all RemindMes
  -v, --version         show program's version number and exit

See LICENSE at https://github.com/GochoMugo/remindme/blob/master/LICENSE

```

## Version Information ##

|Aspect|Detail|
|-------|------:|
|Version| 0.3.1|
|Python|2.6, 2.7, 3.2, 3.3, 3.4|
|Last Upgrade|22nd April, 2015|

> I have __not__ yet tested it on __Python 2.6__ but it should work, I hope


## Contribution ##

If you find a bug, please create an [issue][issues].

Waiting so much for your Pull Request. :-)

**Contributors**:

1. [GochoMugo](https://github.com/GochoMugo)
*  [Low Kian Seong](https://github.com/lowks)


## License ##

Remindme and its Source Code is issued under the [MIT License][MIT].


[gh-pages]:https://gochomugo.github.io/remindme "Remindme Home page"
[issues]:https://github.com/GochoMugo/remindme/issues "Create an Issue"
[MIT]:https://github.com/GochoMugo/remindme/blob/master/LICENSE "MIT License"
