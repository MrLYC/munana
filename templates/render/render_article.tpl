{% if not without_title %}{{article.title}}{% endif %}
{% load filters %}{{article.content|remove_all:remove}}
