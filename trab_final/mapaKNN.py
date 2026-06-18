import matplotlib.pyplot as plt
import geopandas as gpd

estados_knn = [
    ((-46.63, -23.55), "Industrial", "SP"),
    ((-43.20, -22.90), "Industrial", "RJ"),
    ((-43.93, -19.92), "Industrial", "MG"),
    ((-49.27, -25.43), "Agro", "PR"),
    ((-51.21, -30.03), "Agro", "RS"),
    ((-49.25, -16.67), "Agro", "GO"),
    ((-38.52, -3.71), "Serviços", "CE"),
    ((-38.50, -12.97), "Serviços", "BA"),
    ((-34.88, -8.05), "Serviços", "PE"),
    ((-48.54, -27.59), "Serviços", "SC"),
    ((-48.49, -1.45), "Serviços", "PA"),
    ((-60.02, -3.10), "Serviços", "AM"),
    ((-40.31, -20.31), "Serviços", "ES"),
]

plots = {
    "Industrial": ([], []),
    "Agro": ([], []),
    "Serviços": ([], [])
}

markers = {
    "Industrial": "s",
    "Agro": "^",
    "Serviços": "o"
}

colors = {
    "Industrial": "red",
    "Agro": "green",
    "Serviços": "blue"
}

for (longitude, latitude), perfil, uf in estados_knn:
    plots[perfil][0].append(longitude)
    plots[perfil][1].append(latitude)

url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson"
brazil = gpd.read_file(url)

fig, ax = plt.subplots(figsize=(12, 12))

brazil.plot(
    ax=ax,
    color="whitesmoke",
    edgecolor="black",
    alpha=0.8
)

for perfil, (x, y) in plots.items():
    ax.scatter(
        x,
        y,
        color=colors[perfil],
        marker=markers[perfil],
        label=perfil,
        s=150,
        zorder=5
    )

for (longitude, latitude), perfil, uf in estados_knn:
    ax.text(
        longitude + 0.6,
        latitude - 0.2,
        uf,
        fontsize=11,
        fontweight='bold',
        zorder=6
    )

guarapuava_lon = -51.46
guarapuava_lat = -25.39

ax.scatter(
    guarapuava_lon,
    guarapuava_lat,
    color="black",
    s=300,
    marker="*",
    zorder=10
)

ax.text(
    guarapuava_lon - 3.2,
    guarapuava_lat - 1.2,
    "Guarapuava)",
    fontsize=11,
    fontweight="bold",
    color="black",
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.3')
)

plt.title("Classificação kNN: Perfis Econômicos Regionais", fontsize=16, fontweight='bold')
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(title="Perfil Predito", title_fontsize='13', fontsize='11', loc='lower left')
plt.grid(True, linestyle='--', alpha=0.5)

plt.savefig('grafico_mapa_knn.png', bbox_inches='tight', dpi=300)
plt.show()