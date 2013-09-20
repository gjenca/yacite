{{usage}}

**DESCRIPTION:**

{{help}}
{% if posargs %}

**POSITIONAL ARGUMENTS:**
{% for arg in posargs %}> `{{arg.args.0}}`
>> {{arg.kwargs.help}}

{% endfor %}{% endif %}
{% if optargs %}

**OPTIONAL ARGUMENTS:**
{% for arg in optargs %}> `{{arg.args|join(", ")}}`
>> {{arg.kwargs.help}}

{% endfor %}{% endif %}

* * *

