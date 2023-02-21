MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'project.middleware.session.CreateSessionKeyMiddleware',

    'corsheaders.middleware.CorsMiddleware',  # corsheaders

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',  # toolbar
    'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware', # ?debug-toolbar
    # custom
    'apps.base.middleware.MoveJWTRefreshCookieIntoTheBody'
]
