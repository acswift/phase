
<!-- vim: set foldmethod=marker fmr=###,--- :-->

*[version française](instructions-fr.md)*

# Create a `.cube` File

1. download the example Photoshop file [color-map.psd](color-map.psd)  
   - the visual defect is intentional, for licensing reasons
2. replace the sample image (optional)
3. use either the **gradient map** or **color lookup** adjustment layer to create your effect  
   - use blending modes if desired
4. turn off the unused adjustment layer
5. menu File › Export › Color Lookup Tables…  
   - grid points: 64 / high  
   - formats: cube

-----
##### NOTES

To export a `.cube` file, the Photoshop file must contain *only* two visible layers:
- a background layer
- an adjustment layer

To convert a regular layer into a background layer:
- Layer › New › Background from Layer

Phase applies color maps in the Display P3 color space, so a Display P3 document gives the same colors in Phase as in Photoshop:
- Edit › Convert to Profile… › Display P3

---
### Create a Color Map PNG (optional)

Phase makes its own preview for a pasted `.cube` file, and names it after the file. To give a color map its own preview image, names in English and French and a blend mode — like the color maps on the main page — put the `.cube` file inside a PNG:

1. in Photoshop, menu File › File Info…  
   - `Document Title`: the color map's English name  
   - `Author`: its French name (optional)  
   - `Description`: the blend mode, exactly `normal`, `overlay` or `hard light`
2. add a layer mask that hides the adjustment layer over the left-hand sample image
3. menu File › Save As…, format PNG, with **Include Color Profile** checked  
   - use Save As, not Export: Photoshop's export can leave out the File Info
4. in Terminal, put the `.cube` file inside the PNG with [embed-lut.py](embed-lut.py):

```
python3 -I embed-lut.py preview.png map.cube color-map.png
```

Names are cut to 16 characters. When only one name is filled in, Phase uses it in both languages.

Re-saving the result in Photoshop removes the `.cube` file from it: edit the PSD and run `embed-lut.py` again instead.

---
### Other `.cube` Files

Many websites provide free LUT files:
- [freepresets.com](https://www.freepresets.com/product-category/free-luts-color-lookup-table/)
- [giggster.com](https://giggster.com/guide/free-luts/)

Most `.cube` files will work with Phase — just save them in iCloud to access them from your phone.

---
### Use a `.cube` File in Phase

1. on your computer: save the `.cube` file in iCloud
2. on your iPhone: locate the `.cube` file in the **Files** app
3. long-press it and select "Copy"  
   - wait for it to download if necessary
4. long-press in Phase settings and select "Allow Paste"
5. tap the new color map to rename it

---

*[Return to main page](https://github.com/acswift/phase)*
