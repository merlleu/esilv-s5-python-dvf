from .heatmap_renderer import heatmap_render

visus = [
    {
        "name": "Heatmap",
        "options": [
            {
                "name": "Représentation",
                "choices": [
                    {"name": "Prix moyen au m²"},
                    {"name": "Volume foncier total"},
                    {"name": "Nombre de gares"},
                    {"name": "Nombre de gares par prix au m2"},
                    {"name": "Nombre de gares par surface carrez totale vendue"},
                    {"name": "Nombre de gares par volume foncier total"},
                    {"name": "Nombre de transactions par nombre de gares"},
                    {"name": "Carte des Gares", "exclusive": True},
                ]
            },
            {
                "name": "Zone",
                "choices": [
                    {"name": "France"},
                    {"name": "IDF"},
                    {"name": "France hors IDF"}
                ]
            },
            {
                "name": "Période",
                "choices": [
                    {"name": "2017-2023"},
                    {"name": "2018"},
                    {"name": "2019"},
                    {"name": "2020"},
                    {"name": "2021"},
                    {"name": "2022"},
                    {"name": "2023"}
                ]
            }
        ],
        "renderer": heatmap_render
    }
]

for vi, vd in enumerate(visus):
    vd["id"] = vi
    for oi, od in enumerate(vd["options"]):
        od["id"] = oi
        for ci, cd in enumerate(od["choices"]):
            cd["id"] = ci


