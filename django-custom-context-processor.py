# Settings.py==>templates=>OPTIONS>context_processors>'accounts.context_processor.load_site_extras'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processor.load_site_extras'
            ],
        },
    },
]

from django.conf import settings

create new file(context_processor.py) in inside settings.py
def load_site_extras(request):
    config = {
        "SITE_IMG": "logo.png",
        "SITE_FOOTER_TEXT" : "DEMO",
        "POWERED_URL" : "www.google.com",
        "POWERED_SRC": "Demo",
    }
    return config
