"""Configuración mínima de permisos para la app de usuarios."""

PERMISSIONS = {
    "usuarios": {
        "users.view_usuario": {
            "name": "Puede ver usuarios",
            "description": "Acceso de lectura de usuarios",
            "roles": ["Administrador"],
        },
        "users.add_usuario": {
            "name": "Puede crear usuarios",
            "description": "",
            "roles": ["Administrador"],
        },
        "users.change_usuario": {
            "name": "Puede modificar usuarios",
            "description": "",
            "roles": ["Administrador"],
        },
        "users.delete_usuario": {
            "name": "Puede eliminar usuarios",
            "description": "",
            "roles": ["Administrador"],
        },
    },
    "roles": {
        "users.view_role": {"name": "Puede ver roles", "description": "", "roles": ["Administrador"]},
        "users.add_role": {"name": "Puede crear roles", "description": "", "roles": ["Administrador"]},
        "users.change_role": {"name": "Puede modificar roles", "description": "", "roles": ["Administrador"]},
        "users.delete_role": {"name": "Puede eliminar roles", "description": "", "roles": ["Administrador"]},
    },
    "permisos": {
        "users.view_permission": {"name": "Puede ver permisos", "description": "", "roles": ["Administrador"]},
    },
}
