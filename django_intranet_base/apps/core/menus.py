MENUS = {
    'MAIN_SIDEBAR': [
        {
            "name": "Prueba",
            "icon": "fa-book",
            "url": "#",
            "validators": ["menu_generator.validators.is_authenticated"],
            "submenu": [
                {
                    "name": "Otra prueba",
                    "icon": "",
                    "url": "/no/hay/nada",
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
    ],
}