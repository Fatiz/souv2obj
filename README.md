# souv2obj
**VERY** rough converter for sou,v to usable object and material files for the software Blender.

Current usuage is to drag a sou,v file on souv2obj or run
```
> .\souv2obj.py '.\URFILEHERE.sou,v'
```

Currently h2png will take .h,v files formatted like the example one provided and convert them into a usable png.

Current plans are follows:
* Retrieve textures alongside sou,v files and then apply said textures correctly to the generated obj files. (To be incorporated in texture2mtl, currently just colours are supported for the build obj)
* Add the ability to read .c,v files which would be used in conjunction with multiple sou,v and .h,v files to completely build and texture an model in correct orientation.
