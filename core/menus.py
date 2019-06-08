MENUS = {
    'NAVBAR': [
        {
            "name": "Inicio",
            "icon": "fa-home",
            "url": "/",
        },
        {
            "name": "Gremios",
            "icon": "",
            "url": "/cartolas_gremios/",
            "validators": ["menu_generator.validators.is_authenticated"],
        },
    ],
    'ACCOUNTS': [
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