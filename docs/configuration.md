---
layout: default
permalink: /configuration/
---

# configuration

Remindme configuration is placed in a **JSON** file at `~/.remindme`.

* [using an external editor](#editor)


<a name="editor"></a>

### using an external editor:

An external editor is necessary for editing existing remindmes. This configures Remindme to open up the editor when adding or editing remindmes.

{% highlight json %}
{
    "editor": "<command>"
}
{% endhighlight %}

where `<command>` can be the editor's command e.g. `vim`, `gedit` etc.
