MENUS = {
    'MAIN_SIDEBAR': [
        {
            "name": "Gremios",
            "icon": "fa-book",
            "url": "#",
            "validators": ["menu_generator.validators.is_authenticated"],
            "submenu": [
                {
                    "name": "Cartolas de movimientos",
                    "icon": "",
                    "url": "/cartolas_gremios/",
                },
            ],
        },
    ],
    'NAVBAR': [
        {
            "name": "Inicio",
            "icon": "fa-home",
            "url": "/",
        },
        {
            "name": "Iniciar Sesión",
            "icon": "fa-sign-in-alt",
            "url": "/login/",
            "validators": ["menu_generator.validators.is_anonymous"],
        },
        {
            "name": "User",
            "icon": "fa-user",
            "url": "#",
            "validators": ["menu_generator.validators.is_authenticated"],
            "submenu": [
                {
                    "name": "Configuracion",
                    "icon": "fa-sliders-h",
                    "url": "/account/profile",
                },
                {
                    "name": "Cerrar sesión",
                    "icon": "fa-sign-out-alt",
                    "url": "/logout/",
                },
            ],
        },
    ],
}