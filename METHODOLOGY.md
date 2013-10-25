# Methodology

This recipe explains how to check if the level of a spectral line is correct.

1. Synthesize the line. The parameters are not important. We just want to
   generate the output files.

2. In the file `fort.12`, look for the desired spectral line. To find it, you
   can use the third, fourth and fifth column that are, respectively, the
   central wavelength, the chemical element and the ionization stage.

   What we need is the number of the lower level (11th column) and the upper
   level (12th column).

   For example, let's identify the Si IV line at 4116.104 angstrons. The line
   on the `fort.12` file refferring to this spectral line is:

   >9   5584  4116.104   Si  IV   -0.11  193978.889   1.19E+00    56.8   ** 1394 1395   31
   The values that we want are `1394` and `1395`.


3. For this step, it is needed a output from `Tlusty` with termination `.6`.
   [`Tlusty`](http://nova.astro.umd.edu/) is, as advertsied by the authors,
   "A user-oriented package for modeling stellar atmospheres and accretion
   disks and for stellar spectroscopic diagnostics". The `levelchcker` only
   works if you are using a grid of atmospheric models from `Tlusty`.

   Open the file `.6` file and look for the section called
   *EXPLICIT IONS INCLUDED*. Here, it has all identification levels used by
   `Synspec`. Note that the lower level is for Hydrogen  and the following ones
   will only stacking over one another. Thus, look for the chemical element and
   ionization stage desired and obtain the values of the lowest level (column
   N0).

   For our example, we have:

   >27  Si 4  **1390**  1442  1443     4     0    16      0.000D+00

   And the needed value is in boldface.

4. Subtract the level indifications found on (2) and (3).

   For our little example, we have:

   ```
   lower level : 1394 - 1390 = 05
   upper level : 1395 - 1390 = 06
   ```

   Note that the lower level identification has to be included.

5. With the lower and upper level identified, open the file containing the
   atomica data for the chemical element and ionization stage desired.
   It should be in a folder called `atdata`. In this file, the level are in
   ascending order.

   If we go back to the example, we will look into the file
   `atdata\Si4_53lev.dat` and obtain the 13th and the 19th level:

   > 5.09978082E+15      2.    4 **'SiIV 2Se 2'**  0   0.  -105

   > 4.36843030E+15      6.    4 **'SiIV 2Po 2'**  0   0.  -105

   And the levels are showed in boldface, i.e., the lower level is
   `Si IV 2Se 2` and the upper level is `SiIV 2Po 2`. The last term ('2') means
   that it is the the second level with this term ( '2 Se' for the lower
   level and '2Po' for the upper term.

6. Go to [NIST](http://www.nist.gov/) or look for a table of eletronic
   transitions and check if the wavelength of the desired line is correct.

   The NIST pages to go are the
   [Lines Form](http://physics.nist.gov/PhysRefData/ASD/lines_form.html)
   and the
   [Levels Form](http://physics.nist.gov/PhysRefData/ASD/levels_form.html).

   On the Lines Form fill the chemical element plus ionization stage and
   the wavelength range and then press retrieve. For our example, we have:
   ```
   ---------------------------------------------------------------------------------------------------------------------------------------------------------
    Observed  |      Ritz    |  Rel. |    Aki    | Acc. |      Ei           Ek      |     Lower level     |     Upper level     |Type|    TP  |   Line  |
   Wavelength |   Wavelength |  Int. |    s^-1   |      |    (cm-1)       (cm-1)    |---------------------|---------------------|    |   Ref. |   Ref.  |
    Air  (Å)  |    Air  (Å)  |  (?)  |           |      |                           | Conf.  | Term | J   | Conf.  | Term | J   |    |        |         |
   ---------------------------------------------------------------------------------------------------------------------------------------------------------
              |              |       |           |      |                           |        |      |     |        |      |     |    |        |         |
     4116.10  |     4116.103 |     9 | 1.53e+08  | A+   | 193978.89   -  218266.86  | 2p6.4s | 2S   | 1/2 | 2p6.4p | 2P*  | 1/2 |    |    c33 |  L6098  |
   ---------------------------------------------------------------------------------------------------------------------------------------------------------
   ```

   And we can see that the lower level is `2p6.4s 2S` and the upper level is
   `2p6.4p 2P*`, where `*` means 'odd'.

   On the Levels Form, fill the chemical element and ionization stage and retrieve
   the data. For our example we have:
   ```
   ---------------------------------------------------------------------
   Configuration    | Term   |    J |              Level    | Reference
   -----------------|--------|------|-----------------------|-----------
                     |        |      |                       |
   2p6.3s           | 2S     |  1/2 |               0.00    |     L5815
                     |        |      |                       |
   2p6.3p           | 2P*    |  1/2 |           71287.54    |
                     |        |  3/2 |           71748.64    |
                     |        |      |                       |
   2p6.3d           | 2D     |  5/2 |          160374.41    |
                     |        |  3/2 |          160375.60    |
                     |        |      |                       |
   2p6.4s           | 2S     |  1/2 |          193978.89    |
                     |        |      |                       |
   2p6.4p           | 2P*    |  1/2 |          218266.86    |
                     |        |  3/2 |          218428.67    |
   ...
   ```

   For the lower level we had obtained `2Se 2`, which is the second configuration
   with the term `2Se` and we see from the above table that it is `2p6.45 2S`,
   in accordance with what we got on the Lines Form. The same line of thought
   can be made for the upper level. Thus, we can see that both levels are correct.


