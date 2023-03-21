# <p align="center">TopasGraphSim</p>

## <p align="center">A GUI to simplify and streamline the plotting and analysis of medical physics simulations</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/87897942/152699152-d4d39654-4449-4354-b899-4adc81eb25a7.png" width="320" height="160" />
</p>

This GUI can visualize and analyze percentage depth dose (pdd) and dose profiles (dp) simulations from [TOPAS](http://www.topasmc.org/). Depth dose measurements are assumed to be in the z-direction, dose profiles in the x- or y-directions. Data read-in is handled by [topas2numpy](https://github.com/davidchall/topas2numpy).

## Installation

Install using pip:

```console
$ pip install topasgraphsim     
```
     
Then, start the GUI by running:
     
```console
$ python -m topasgraphsim
```

Or, if your Python is added to $PATH, simply run:

```console
$ topasgraphsim
```

Open compatible files from the command line:

```console
$ topasgraphsim "path_to_your_file"
```

<b>Note:</b> Linux users need to have python3-tk installed. If it isnt installed yet, use:

```console
$ sudo apt-get install python3-tk
```

Also, you may need python-dev. Install if for your python version using:

```console
$ sudo apt-get install python<your main version>-dev
```

Since all my testing in done on Windows 11, I cannot guarantee this will work on any other plattform. I'm open to suggestions or PRs making the software work better cross-plattfrom!


## Features

 - Reproducible graphing and analysis of 1D TOPAS simulation for medical physics
 - Simultaneous plotting and parameter calculation for all data sets
 - Calculation of the Gamma Index with adjustable parameters
 - Graph adjustment options
     * Normalization (On/Off)
     * Error bars (On/Off)
     * Graph order and colors
     * Marker size and style
     * Line width
 - Drag and drop of files
 - Center axis deviation correction *
 - Import of EGS and RadCalc simulation results *
 - Import of custom measurements (as numpy .txt files) *
 - Import of PTW tbaScan (MEPHYSTO mc<sup>2</sup>) measurements
 - German and english language support
 - Dark mode

 (*) Not yet implemented

 ## Screenshots
 
![Home](https://user-images.githubusercontent.com/87897942/226645582-40258076-d61a-4ec8-850c-e7f40f9b0aa7.png)

![Graph](https://user-images.githubusercontent.com/87897942/226646220-f5dff844-4cd7-427f-b5e8-de7d111e3fa6.png)

 ## Manual
![Gamma](https://user-images.githubusercontent.com/87897942/226646442-40dc390f-05ca-4c18-84e7-52f5631c99ec.png)

![Plot](https://user-images.githubusercontent.com/87897942/226646461-aafc4c98-82b1-4ba0-82f3-de280297eddf.png)

![Tab](https://user-images.githubusercontent.com/87897942/226646489-49aa1319-995b-4f7e-8d42-344768f6ed8e.png)

 ## Parameters

Depending on the imported measurement, the following parameters can be calculated:

| Measurement type | Parameters |                   |                        |                       |                |                |
| ---------------- | :--------: | :---------------: | :--------------------: | :-------------------: | :------------: | :------------: |
|                  |            |                   |                        |                       |                |                |
| Depth dose       |  Q-Factor  |  z<sub>max</sub>  |                        |                       |                |                |
|                  |            |                   |                        |                       |                |                |
| Dose profile     |    FWHM    | CAX<sub>dev</sub> | FLAT<sub>Krieger</sub> | FLAT<sub>stddev</sub> | Penumbra (L&R) | Integral (L&R) |

- Q-Factor : Radiation Quality Factor
- z<sub>max</sub> : Depth at Maximum

- FWHM : Full-Width at Half-Maximum
- CAX<sub>dev</sub> : Centre Axis Deviation
- FLAT<sub>Krieger</sub> : Flatness of Dose Plateau (Definition by Krieger)
- FLAT<sub>stddev</sub> : Flatness of Dose Plateau (Standard Deviation)
- Penumbra (L&R) : Width of Left and Right Penumbra
- Integral (L&R) : Integral below Left and Right Penumbra

## Dependencies

The UI is based on the [customtkinter](http://github.com/TomSchimansky/CustomTkinter) library.

Requires python3, numpy, scipy, matplotlib, Pillow, python-opencv, pynput, requests, topas2numpy, and python-tkdnd.
## Contact me!

Thank you for using TopasGraphSim! Please let me know about any issues you encounter, or suggestions/wishes you might have! 
<br></br>
[![Downloads](https://static.pepy.tech/personalized-badge/topasgraphsim?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/topasgraphsim)
