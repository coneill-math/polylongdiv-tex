# polylongdiv-tex
Perform polynomial long division using modular arithmetic and output well-formatted LaTeX.

You can find action shots in the `samples` folder.  

Please note that this is an *alpha version* and subject to change without notice.  

## License
numsgps-sage is released under the terms of the [MIT license](https://tldrlegal.com/license/mit-license).  The MIT License is simple and easy to understand and it places almost no restrictions on what you can do with this software.

## Usage
To set up your machine to use polylongdiv-tex, do the following.  

* Download and unzip polylongdiv-tex.  
* Alternatively, simply download the polylongdiv.py file.  
* It does not need to be placed in any particular location on your computer

To use polylongdiv-tex, use your favorite Python interpreter, or open the command prompt and run the following commands (replace `PATH_TO_POLYLONGDIV_TEX` with the path of whichever folder contains `staircase.py`).  

	cd PATH_TO_POLYLONGDIV_TEX
	python polylongdiv.py --help
	python polylongdiv.py -a 1 3 -7 0 5 4  -b 2 1 5  -n 11
	python polylongdiv.py -t -a 1 3 -7 0 5 4  -b 2 1 5  -n 11
	python polylongdiv.py -t -V y -a 1 3 -7 0 5 4  -b 2 1 5  -n 11
	python polylongdiv.py -t -o myfile.txt -a 1 3 -7 0 5 4  -b 2 1 5  -n 11

