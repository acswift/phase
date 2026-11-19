
<!-- vim: set foldmethod=marker fmr=###,--- :-->

# Source Material

The folders in this section represent steps in the color-map creation workflow:
1. `psd` folder: create a 1200x300px `.psd` file containing a double sample image and the desired adjustment layer  
   - File › File Info… in Photoshop to name the color map  
   - English color map name in `Document Title`  
   - French color map name in `Author`  
   - blend mode (normal, overlay, hard light) in `Description`
2. `cube` folder: export the lookup table as a `.cube` file
3. `png-prelim` folder: add a layer mask to deactivate the adjustment layer over one of the sample images and export as a PNG
4. `color-maps` folder (main page): put the `.cube` file inside the PNG with `embed-lut.py`, run from the top of the repo:

```
python3 -I embed-lut.py source-files/png-prelim/alien-prelim.png source-files/cube/alien.cube color-maps/alien.png
```

The tool copies the PNG untouched and adds the `.cube` file, compressed, in an extra chunk that Phase reads when the image is pasted. Re-saving the result in Photoshop drops that chunk, so edit the PSD and run the tool again instead.

-----
### Sources of LUT Files

Sources of the LUTs available on our main page.

##### Phase Originals

- Alien
- Black & White
- Heat Map (inspired by Photo Booth)
- Monochrome
- Spectrum
- Yellow

-----
##### Adobe Photoshop

These are included by default in the Photoshop **Color Lookup** panel:

- 3 Strip as `3Strip`
- Bright Life as `filmstock_50`
- FE2F3 as `Fuji ETERNA 250D Fuji 3510 (by Adobe)`
- Lush Life as `Fuji REALA 500D Kodak 2393 (by Adobe)`
- Orange Teal as `TealOrangePlusContrast`

There are also many others.

-----
##### PresetPro

PresetPro offers more than 150 free `.cube` files — it's well worth a visit!

- [Color 400](https://www.freepresets.com/product/free-lightroom-preset-color-400/)
- [Lomographic](https://www.freepresets.com/product/free-lut-lomography/)
- [Moody Film](https://www.freepresets.com/product/free-lut-moody-film-lookup-table/)
- [Moody Stock](https://www.freepresets.com/product/free-lut-moody-stock/)
- [Portra 400](https://www.freepresets.com/product/free-lut-portra-400-lookup-table/)
- [Sea Breeze](https://www.freepresets.com/product/free-lut-sea-breeze/)

-----
##### Stock Presets

Stock Presets has about 25 free `.cube` files.

- [Roadrunner](https://www.stockpresets.com/product/free-lightroom-preset-profile-roadrunner/)

