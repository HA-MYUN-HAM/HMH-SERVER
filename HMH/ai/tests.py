from django.test import TestCase

def create_prompt_with_event_info(template_text, event_title, event_date):
    return template_text.format(event_title=event_title, event_date=event_date)