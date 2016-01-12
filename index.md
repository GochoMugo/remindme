---
layout: default
permalink: /
---

# remindme

{{ site.description }}

|version|0.5.0|
|python|2.7, 3.3, 3.4|
|last upgrade|13th January, 2016|

* [why use remindme](#why)
* [see it work](#work)
* [installation](#install)
  * [upgrading](#upgrade)

<a name="why"></a>

## why use remindme

Since we can not always remember everything, we sometimes need to write
some notes. Writing notes on paper is tiring, messy and not so
portable. Keeping a file(s) with several such notes may get messy real
fast.

Features:

* simple interface

    Using remindme is quite simple. Its interface is focused on being simple
    with sane default options, which are easily configured.

* multi-platform

    Remindme can run in any system with Python support. Yes, it can run on
    Windows.

* encryption support

    Uses AES cipher, in CBC mode, with 128-bit key size. See the
    [official docs](https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet)
    on the encryption techniques used and detailed documentation.


<a name="work"></a>

<center>click to view it better</center>

[![Working with remindme](img/working.gif)](img/working.gif)


<a name="install"></a>

## installation

You can install remindme using `pip`:

{% highlight bash %}
⇒ pip install remindme
{% endhighlight %}

<a name="upgrade"></a>

### upgrading

You can also upgrade remindme anytime:

{% highlight bash %}
⇒ pip install --upgrade remindme
{% endhighlight %}
