---
layout: default
permalink: /configuration/
---

# configuration

Remindme configuration is placed in a **JSON** file at `~/.remindme`.

* [using an external editor](#editor)
* [configuring encryption functions](#crypto)


<a name="editor"></a>

### using an external editor:

An external editor is necessary for editing existing remindmes. This configures Remindme to open up the editor when adding or editing remindmes.

{% highlight json %}
{
    "editor": "<command>"
}
{% endhighlight %}

where `<command>` can be the editor's command e.g. `vim`, `gedit` etc.


<a name="crypto"></a>

### configuring encryption functions:

If you only encrypt your remindmes a few times, you may want to change
you choice on encrypting by default. Consequently, you won't be asked
for a password unless you pass the option `--encrypt` (requesting encryption):

{% highlight json %}
{
    "encrypt_by_default": false
}
{% endhighlight %}


Encryption can be disabled altogether:

{% highlight json %}
{
    "disable_encryption": true
}
{% endhighlight %}
