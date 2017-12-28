# lambdastack

This language was orginally defined by 'EzoLang', on the [Esolang wiki](https://www.esolangs.org/wiki/Lambdastack). As a school project, I chose to implement this language, as it had not yet been implemented. It was an exciting project, and I would like to share the result.

## Installation

You can head on over to the [releases](https://github.com/SPK44/lambdastack/releases/latest) section to get the precompiled binaries. To be fair though, I have little to no experience with releasing binaries. If this method does not work for you, an equivalent method would be to clone the repository, or download the zip, then install the requirements (just [Ply](https://github.com/dabeaz/ply)). You can then run:

``` bash
python main.py
```

If you would like to build your own binary, you may install [cx_freeze](https://github.com/anthony-tuininga/cx_Freeze), then run the following on the source code:

``` bash
python setup.py build
```

This was built on Python 3.6

## Language Reference

I am going to refer you to mostly to the [Esolang wiki](https://www.esolangs.org/wiki/Lambdastack) entry for the language, however one big change is that the `O` operator will print out _anything_ on the top of the stack. This is very useful for debugging.
