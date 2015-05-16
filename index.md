---
layout: default
permalink: /
no_menu: true
---

# remindme

{{ site.description }}

|version|0.3.2|
|python|2.6, 2.7, 3.2, 3.3, 3.4|
|last upgrade|15th May, 2015|


## contents:

* [why use remindme](#why)
* [using remindme](#usage)
  * [adding a note](#add)
  * [listing notes](#list)
  * [reading a note](#read)
  * [removing a note](#remove)
  * [removing all remindmes](#remove-all)
  * [help information](#help)
  * [version information](#version)
* [installation](#install)
  * [upgrading](#upgrade)


<a name="why"></a>

## why use remindme

Since we can not always remember everything, we sometimes need to write some notes. Writing notes on paper is tiring, messy and not so portable. Keeping a file(s) with several such notes may get messy real fast.

*remindme* makes keeping such notes easy and fast.


<a name="usage"></a>

## using remindme

<a name="add"></a>

### adding new notes:
Adding a note is simple:

{% highlight bash %}
⇒ remindme --add Title of The Note
[runner]: Enter what you remember now?
> This is some content of the note
>
> You can keep entering content over
> several lines
>
> :end
[runner]: RemindMe will remind you next time.
{% endhighlight %}

To exit edit mode, you need to type `:end` in a separate line. You can also use `Cmd`/`Ctrl` + `C` to exit.

If you have content that you want to add without entering edit mode, you can simply pipe it into remindme.

{% highlight bash %}
⇒ echo "content of the note" | remindme --in Another Awesome Note
{% endhighlight %}

This is useful, say, you have a file with some content and want to save it as a note.


<a name="list"></a>

### listing notes:

To see the notes you have added:

{% highlight bash %}
⇒ remindme --list
[runner]: Found 1 remindme
1  - Title of The Note
{% endhighlight %}


<a name="read"></a>

### reading a note:

Reading a note is even simpler:

{% highlight bash %}
⇒ remindme Title of The Note
[runner]: Reminding you:
1 This is some content of the note
2
3 You can keep entering content over
4 several lines
{% endhighlight %}

<a name="remove"></a>

### removing a note:

We may require to remove a note:

{% highlight bash %}
⇒ remindme --remove Title of The Note
[runner]: remindme successfully removed
{% endhighlight %}

<a name="remove-all"></a>

### removing all remindmes:

Removing all remindmes (**TAKE CARE**):

{% highlight bash %}
⇒ remindme --remove-all
{% endhighlight %}

<a name="help"></a>

### help information:

See help information with:

{% highlight bash %}
⇒ remindme --help
{% endhighlight %}

<a name="version"></a>

### version information:

Version information can be seen with:

{% highlight bash %}
⇒ remindme --version
{% endhighlight %}

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
