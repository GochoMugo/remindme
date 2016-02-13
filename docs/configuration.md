---
layout: default
permalink: /configuration/
---

# configuration

Remindme configuration is placed in a **JSON** file at `~/.remindme`.

* [using an external editor](#editor)
* [configuring encryption functions](#crypto)
* [retries](#retry)


<a name="editor"></a>

### using an external editor:

An external editor is necessary for editing existing remindmes. This configures Remindme to open up the editor when adding or editing remindmes.

{% highlight json %}
{
    "editor": "<command>"
}
{% endhighlight %}

where `<command>` can be the editor's command e.g. `vim`, `gedit` etc.

However, if you are using the built-in editor and want to change the 'line end',
that is, the `:end` to something shorter or your preferred keys:

{% highlight json %}
{
    "end_line": ":q"
}
{% endhighlight %}


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


<a name="retry"></a>
## retries:

When entering a password for a note that is about to be encrypted, you are
prompted to re-enter the password so as to ensure they match. This can be
disabled using:

{% highlight json %}
{
    "retry_password_match": false
}
{% endhighlight %}

When decryption fails, you may want to be prompted again for a correct
password. This behavior can be enabled using:

{% highlight json %}
{
    "retry_decryption": true
}
{% endhighlight %}

