ADMIN_REORDER = (
    'recruiting',
)
JAZZMIN_SETTINGS = {
    "site_title": "Flick ERP",

    "site_header": "Flick ERP",
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
    "usermenu_links": [
        {"name": "Support", "url": "https://www.geitpl.com/", "new_window": True},
        {"name": "privacy_policy", "url": "https://www.geitpl.com/", "new_window": True},
        {"name": "T&C", "url": "https://www.geitpl.com/", "new_window": True}

    ],
    # Whether to display the side menu
    "show_sidebar": True,
    "language_chooser": True,

    # Whether to aut expand the menu
    "navigation_expanded": False,
    "hide_apps": ['Field_History'],
    "icons": {
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "recruiting": "fas fa-university"
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "changeform_format": "horizontal_tabs",
}

X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']
