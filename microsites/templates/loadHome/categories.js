{% load i18n extra_tags %}

var $el = $("#id_filter_category");
$el.empty();

$el.append(new Option("{% trans "FILTER-ENTITY-OPTION" %}", "", true));
{% for category in categories %}
  $el.append(new Option("{{category.name}}", "{{category.id}}"));
{% endfor %}
