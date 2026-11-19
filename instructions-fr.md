
<!-- vim: set foldmethod=marker fmr=###,--- :-->

*[English version](instructions.md)*

# Créer un fichier `.cube`

1. téléchargez le fichier Photoshop d’exemple [color-map.psd](color-map.psd)
   - le défaut visuel est volontaire, pour des raisons de licence
2. remplacez l’image d’exemple (facultatif)
3. utilisez le calque de réglage **Courbe de transfert de dégradé** ou **Correspondance de couleurs** pour créer votre effet  
   - utilisez les modes de fusion si vous le souhaitez
4. masquez le calque de réglage inutilisé
5. menu Fichier › Exporter › Tables de correspondance des couleurs…  
   - points de grille : 64 / élevée  
   - formats : CUBE

-----
##### REMARQUES

Pour exporter un fichier `.cube`, seuls *deux calques* doivent être visibles dans le fichier Photoshop :
- un calque d’arrière-plan
- un calque de réglage

Pour convertir un calque normal en arrière-plan :
- Calque › Nouveau › Arrière-plan d’après un calque

Phase applique les color maps dans l’espace colorimétrique Display P3 : un document en Display P3 donne donc les mêmes couleurs dans Phase que dans Photoshop :
- Édition › Convertir en profil… › Display P3

---
### Créer une color map en PNG (facultatif)

Phase crée lui-même un aperçu pour un fichier `.cube` collé, et lui donne le nom du fichier. Pour donner à une color map sa propre image d’aperçu, un nom en anglais et en français et un mode de fusion — comme les color maps de la page principale — placez le fichier `.cube` dans un PNG :

1. dans Photoshop, menu Fichier › Informations sur le fichier…  
   - `Titre du document` : le nom anglais de la color map  
   - `Auteur` : son nom français (facultatif)  
   - `Description` : le mode de fusion, exactement `normal`, `overlay` ou `hard light`
2. ajoutez un masque de fusion qui masque le calque de réglage sur l’image d’exemple de gauche
3. menu Fichier › Enregistrer sous…, format PNG, en cochant **Inclure le profil colorimétrique**  
   - utilisez Enregistrer sous, pas Exporter : l’export de Photoshop peut laisser de côté les informations sur le fichier
4. dans le Terminal, placez le fichier `.cube` dans le PNG avec [embed-lut.py](embed-lut.py) :

```
python3 -I embed-lut.py apercu.png map.cube color-map.png
```

Les noms sont limités à 16 caractères. Si un seul nom est rempli, Phase l’utilise dans les deux langues.

Réenregistrer le résultat dans Photoshop en retire le fichier `.cube` : modifiez plutôt le PSD et relancez `embed-lut.py`.

---
### Autres fichiers `.cube`

De nombreux sites proposent des fichiers LUT gratuits :
- [freepresets.com](https://www.freepresets.com/product-category/free-luts-color-lookup-table/)
- [giggster.com](https://giggster.com/guide/free-luts/)

La plupart des fichiers `.cube` fonctionnent avec Phase — il suffit de les enregistrer dans iCloud pour y accéder depuis votre téléphone.

---
### Utiliser un fichier `.cube` dans Phase

1. sur votre ordinateur : enregistrez le fichier `.cube` dans iCloud
2. sur votre iPhone : retrouvez le fichier `.cube` dans l’app **Fichiers**
3. appuyez longuement dessus et choisissez « Copier »  
   - attendez qu’il se télécharge si nécessaire
4. appuyez longuement dans les réglages de Phase et choisissez « Autoriser le collage »
5. touchez la nouvelle color map pour la renommer

---

*[Retour à la page principale](README-FR.md)*
