# New Naming conventions

## Country codes: 3 characters

## Fuel codes: 6 characters (Except from the intermediate fuels for NG pipeline)


`^^^___`: first three characters 01-03 represent country code

`___^^^`: last three characters 04-06
- list of fuels: `ETH, CR1, CR2, BIO, COA, LFO, GAS, HFO, SOL, WIN, URN, CHA, WA1, WA2, EL1, HE2, EL2, FW3, HE3, EL3, HF3, LF3, CH3, GA3, CA3, BO3, CR3, DEL, DLG, DNG`
- the fuels that have number `3` at the end represent the final energy demand `FW3, HE3, EL3, HF3, LF3, CH3, GA3, CA3, BO3, CR3`
- the fuels that have the description `GASP` at the end represent the intermediate fuels for NG pipeline

** Note: `BO3` the first two are characters and only the last one is a number

## Tech codes: 12 characters

### Currently not following any coding

`BACKSTOP`

### Power generation technologies/Power plants:

`^^^_________`: first three characters 01-03 represent country code

`___^^^______`: character 04-06 represent the type of fuel (`BIO, COA, CHA, CO1, CO2, EL1, EL2,
ETH, GEO, HE2, HFO, HYD, LFO, NGA, BIO, URN, SOL, WA2, WIN, LNG`) . Note `LNG` is not in the list of fuels but it has been added as a code in the technologies to distinguish between natural gas imports and LNG imports.

`______^^____`: character 07-08 represent the type of technology (`CH`: biomass CHP plant, `SC`:Superctritical coal, `CV`: conventional geothermal, `GC`: gas cycle, `LS`: large size hydro, `MS`: medium size hydro, `SS`: small size hydro, `SA`: stand alone, `RC`: LFO, `CC`: combined cycle, `PW`: pressurized water reactor (nuclear), `CN`: CSP (without storage), `CS`: CSP (with                           storage), `PU`: PV(utility), `PV`: PV(roof top), `PS`: PV (with storage), `ON`: onshore (wind), `OF`: offshore (wind)

`________^___`: character 09 represent if the technology includes CCS or not. (`P`: its a power
generation tech. without CCS, `C`: its a power generation tech. with CCS)

`_________^^_`: character 10-11 represent the cooling type (`00`: means that the cooling type is not one of the following; `01`-`04`: `AIR, MDT, NDT, OTF/OTS`.

Hint: If it is `00` then that means that a cooling type of the following: AIR, MDT, NDT, OTF/OTS has
not been assigned to the power generation technology (example: hydro, wind).
In example Solar PV has `00` as cooling type but a water factor has been assigned to that technology.

`___________^`: character 12 represent if the power plant is Old (code: O) or New (code: N) or if there is no distinction (code: X)

### Extraction/import/export technologies:

`^^^_________`: first three characters 01-03 represent country code

`___^^^______`: character 04-06 represent the type of fuel (BIO, COA, CHA, CO1, CO2, EL1, EL2, ETH, GEO, HE2, HFO, HYD, LFO, NGA, BIO,                   URN, SOL, WA2, WIN, LNG)

`______^^____`: character 07-08 represent the type of technology (IM: imports, PR: production, EX: exports).
                Hint: Exports are represented in a different way in this model

`________^___`: character 09 will be P in this case.

`_________^^_`: character 10-11 represent the cooling type, so code:00 since a cooling type has not been assigned to the technology

`___________^`: character 12 since there is no distinction (code: X)


### Transmission & distribution, Process:

`^^^_________`: first three characters 01-03 represent country code

`___^^^______`: character 04-06 represent the type of fuel (`BIO, COA, CHA, CO1, CO2, EL1, EL2, ETH, GEO, HE2, HFO, HYD, LFO, NGA, BIO, URN, SOL, WA2, WIN, LNG`)

`______^^____`: character 07-08 represent the type of technology (
    `TR`: transmission, `DI`: distribution)
                Hint: the process technologies have `DI` as code.

`________^___`: character 09 will be `P` in this case.

`_________^^_`: character 10-11 represent the cooling type, so code: `00` since a cooling type has not been assigned to the technology

`___________^`: character 12, since there is no distinction the code: `X`


### Conversion technologies (new naming ???):

- (old) `CRUDPROX`	--> (new) `CO1??????`	= Crude oil refinery capacity
- (old) `CRUDRE1X` --> (new) `CO2??????`	= Crude oil refinery 1
- (old) `CRUDRE2X` --> (new) `CO2??????`	= Crude oil refinery 2

## Trade links (new naming ?):

### Exports_EL

  (old) `^^EL^^BP00`: where ^^ country codes
  (new) `^^^EL1EX????`

         2) Exports_NG
  (old) `^^NG^^BP00`: where ^^ country codes
  (new) `^^^NGAEX????`

     VII) Intermediate_NG:
  (old)`^^NG00IPIX`: where ^^ country codes
  (new)`^^^NGA??????`


## Emission factors: 6 characters

`^^^___`: first three characters 01-03 represent country code

`___^^^`: last three characters represent `CO2`, `REN`.
*the other emission factors have not been used.

## Timeslices: 4 characters

`^^__`: first two characters represent season (S1-S4)

`__^^`: last two characters represent dayparts (D1,D2)


# Old Naming conventions

(Vignesh has already the scripts to read the technologies/fuels --> to be checked)

