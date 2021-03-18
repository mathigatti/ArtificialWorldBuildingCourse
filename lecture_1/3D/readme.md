# 3DCA

Generate 3D cellular automatas.

![]("https://github.com/mathigatti/ArtificialWorldBuilding/blob/main/lecture_1/3D/sample.jpeg?raw=true")

# Requirements

- Python 3
- Some libraries depending the 3D format you want to use. 

# Usage

## Create 3D file

```
python 3DCA.py
```

## Export it to the desired 3D format


- `npy2blender.py`: This uses Blender GUI to generate each pixel. It's pretty slow though, it's better to import an .stl file into Blender.
- `npy2stl.py`: Convert the file to .stl
- `npy2image.py`: Render the image using povray
- `npy2scad.py`: Convert the file to .scad

### Usage example

```
python npy2stl.py
```
