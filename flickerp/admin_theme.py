ADMIN_REORDER = (
    'recruiting',
)
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Flick ERP",

    # Title on the brand, and login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Flick ERP",

    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    # "site_logo": "/img/logo.png",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to Flick ERP",

    # Copyright on the footer
    "copyright": "Flick ERP",

    "search_model": "recruiting.Candidate",

    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [
        {"app": "recruiting"},
        #{"app": "User"},
        # {"app": "education"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://www.geitpl.com/", "new_window": True},
        {"name": "privacy_policy", "url": "https://www.geitpl.com/", "new_window": True},
        {"name": "T&C", "url": "https://www.geitpl.com/", "new_window": True}

    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ['Field_History'],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": ['auth.group'],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    # "order_with_respect_to": ["institution","song", "education"],

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "recruiting": "fas fa-university"
        # "institution.UserProfile":"fas fa-users",
        # "institution.Institution":"fas fa-university",
        # "song.Song":"fas fa-music",
        # "song.Playlist":"fas fa-stream",
        # "song.Activity":"fas fa-snowboarding",
        # "song.Tags":"fas fa-tags",
        # "song.Type":"fas fa-text-height",
        # "education.Article":"fas fa-newspaper",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']
