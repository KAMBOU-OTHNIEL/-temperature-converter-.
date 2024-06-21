import rasterio
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from scipy.ndimage import median_filter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import folium
from folium.plugins import HeatMap
import pandas as pd
import webbrowser
import os
from folium import IFrame
from rasterio.transform import rowcol, xy

# Fonction pour lire les images GeoTIFF et les convertir en numpy arrays
def read_image(image_path):
    with rasterio.open(image_path) as src:
        return src.read(), src.profile

# Fonction de correction atmosphérique simple (Dark Object Subtraction)
def dark_object_subtraction(image):
    dark_object_value = np.percentile(image, 1, axis=(1, 2), keepdims=True)
    return np.clip(image - dark_object_value, 0, None)

# Chemins vers vos fichiers d'images satellites locales
image_path_2022 = r'C:/Users/Utilisateur/Documents/PROJET/PERSONELLE/PROJET_PYTHON_FORMATION/PROJET_FORMATION_PYTHON/LC08_L2SP_197056_20220831_20220910_02_T2_SR_B6.TIF'
image_path_2023 = r'C:/Users/Utilisateur/Documents/PROJET/PERSONELLE/PROJET_PYTHON_FORMATION/PROJET_FORMATION_PYTHON/LC08_L2SP_197056_20230802_20230811_02_T2_SR_B6.TIF'

# Verifier les fichiers existant
if not os.path.isfile(image_path_2022):
    print(f"Le fichier {image_path_2022} n'existe pas.")
    exit(1)
if not os.path.isfile(image_path_2023):
    print(f"Le fichier {image_path_2023} n'existe pas.")
    exit(1)

# Lire les images
image_2022, profile_2022 = read_image(image_path_2022)
image_2023, profile_2023 = read_image(image_path_2023)

if image_2022 is None or image_2023 is None:
    exit(1)

# Appliquer la correction atmosphérique
image_2022_corrected = dark_object_subtraction(image_2022)
image_2023_corrected = dark_object_subtraction(image_2023)

# Calculer la différence entre les deux images corrigées
diff = np.abs(image_2023_corrected.astype(np.float32) - image_2022_corrected.astype(np.float32))

# Appliquer un seuil pour détecter les changements
threshold = threshold_otsu(diff)
change_map = diff > threshold

# Réduction du bruit par filtrage
filtered_change_map = median_filter(change_map, size=3)

# Visualiser les images corrigées
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(image_2022_corrected[0], cmap='gray')
plt.title('Image 2022 Corrigée')

plt.subplot(1, 2, 2)
plt.imshow(image_2023_corrected[0], cmap='gray')
plt.title('Image 2023 Corrigée')
plt.show()

# Visualiser la carte des changements
plt.figure(figsize=(10, 10))
plt.imshow(filtered_change_map[0], cmap='gray')
plt.title('Carte des Changements')
plt.show()

# Préparation des données pour la classification des changements
X_change = diff.reshape(-1, diff.shape[0])
y_change = change_map.reshape(-1)

# Entraîner un classificateur Random Forest pour les changements
X_train, X_test, y_train, y_test = train_test_split(X_change, y_change, test_size=0.3, random_state=42)
clf_change = RandomForestClassifier(n_estimators=100, random_state=42)
clf_change.fit(X_train, y_train)

# Prédire les classes de changement sur l'ensemble de test
y_pred_change = clf_change.predict(X_test)

# Évaluer la performance du modèle de classification des changements
print("Rapport de classification des changements")
print(classification_report(y_test, y_pred_change))
print("Matrice de confusion des changements")
print(confusion_matrix(y_test, y_pred_change))

# Analyse statistique des changements
change_count = np.sum(filtered_change_map)
total_pixels = filtered_change_map.size
change_percentage = (change_count / total_pixels) * 100

# Affichage des résultats statistiques
print(f"Nombre total de changements détectés : {change_count}")
print(f"Pourcentage de changements : {change_percentage:.2f}%")

# Créer une carte interactive avec Folium
m = folium.Map(location=[5.79312, -6.59257], zoom_start=10)

# Ajouter les changements détectés sous forme de heatmap
change_coords = np.column_stack(np.where(filtered_change_map[0]))

# Convertir les coordonnées des pixels en coordonnées géographiques
transform = profile_2022['transform']
heat_data_geo = [xy(transform, coord[0], coord[1]) for coord in change_coords]

# Vérifier la transformation des données géographiques
print("Données de la heatmap (coordonnées géographiques):", heat_data_geo[:5])

# Ajouter les données de heatmap à la carte Folium
HeatMap(heat_data_geo).add_to(m)

# Création de la chaîne HTML avec les statistiques des changements
html = f"""
<h3>Rapport de classification des changements</h3>
<pre>{classification_report(y_test, y_pred_change)}</pre>
<h3>Matrice de confusion</h3>
<pre>{confusion_matrix(y_test, y_pred_change)}</pre>
<h3>Analyse statistique des changements</h3>
<p>Nombre total de changements détectés : {change_count}</p>
<p>Pourcentage de changements : {change_percentage:.2f}%</p>
"""

iframe = IFrame(html, width=700, height=400)
popup = folium.Popup(iframe, max_width=700)
folium.Marker([5.79312, -6.59257], popup=popup).add_to(m)

# Enregistrer la carte dans un fichier HTML
html_file = 'change_detection_map.html'
m.save(html_file)

# Vérifier si le fichier a été créé
if os.path.exists(html_file):
    print(f"Carte des changements sauvegardée sous '{html_file}'")
    # Ouvrir automatiquement la carte HTML dans le navigateur
    webbrowser.open(f'file://{os.path.realpath(html_file)}')
else:
    print("Erreur : Le fichier HTML n'a pas été créé.")

# Afficher les métriques du modèle
report_change = classification_report(y_test, y_pred_change, output_dict=True)
report_change_df = pd.DataFrame(report_change).transpose()
print(report_change_df)

# Afficher la matrice de confusion
conf_matrix_change = confusion_matrix(y_test, y_pred_change)
print(conf_matrix_change)
