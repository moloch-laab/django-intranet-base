from django import template
register = template.Library()

@register.inclusion_tag('my_snippet.html')
def show_form(form):
      return {'form': form}

register.inclusion_tag('core/snippets/form.html')(show_form)   # Here register is a django.template.Library instance.