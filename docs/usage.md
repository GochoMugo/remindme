---
layout: default
permalink: /usage/
---

# usage

* [adding a note](#add)
* [listing notes](#list)
* [reading a note](#read)
* [editing an existing note](#edit)
* [removing a note](#remove)
* [using the list index](#index)
* [removing all remindmes](#remove-all)
* [help information](#help)
* [version information](#version)

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

If you want to get the raw, unmodified content
without colors, status information, etc.,
use the `-o/--raw` flag. This is useful when you want to
pipe the content to some other process.

{% highlight bash %}
⇒ remindme Title of The Note --raw
This is some content of the note

You can keep entering content over
several lines
{% endhighlight %}


<a name="edit"></a>

### editing an existing note:

Editing an existing note is simple too. Although [we need an external editor]({{ site.baseurl }}/configuration/#editor) for this.

{% highlight bash %}
⇒ remindme --edit Title of The Note
{% endhighlight %}


<a name="remove"></a>

### removing a note:

We may require to remove a note:

{% highlight bash %}
⇒ remindme --remove Title of The Note
[runner]: remindme successfully removed
{% endhighlight %}


<a name="index"></a>

### using the list index:

When you list the remindmes with `--list`, they are numbered in the list
shown. To allow faster operations, the number, here referred to as the
**index**, can be used instead of the title. You just have to use `--index`
to tell remindme, that it is an index.

For example,

{% highlight bash %}
⇒ remindme --index --remove 2
[runner]: remindme successfully removed
{% endhighlight %}

> **Note**: These indices **change** with additions and removal of other notes since
> the list is kept ordered alphabetically. Do **not** assume a remindme has the
> same index, without checking first.


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
