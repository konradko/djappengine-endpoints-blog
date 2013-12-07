from django import template
from google.appengine.api import users

register = template.Library()

@register.assignment_tag
def is_current_user_admin():
    return users.is_current_user_admin()

@register.simple_tag
def get_logout_url():
    return users.create_logout_url('/')