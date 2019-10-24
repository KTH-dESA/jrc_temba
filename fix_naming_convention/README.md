# New Naming conventions

1) Country codes: 3 letters

2) Fuel codes: 3 letters (Except from the intermediate fuels for NG pipeline)
    - the fuels that have number 3 at the end represent the final energy demand = FW3, HE3, EL3, HF3, LF3, CH3, GA3, CO3, BO3, CR3
    - the fuels that have the description ^^^GASP at the end represent the intermediate fuels for NG pipeline (the first 3 letters will be the country code)
    
* List of fuels: ETH, CO1, CO2, BIO, COA, LFO, GAS, HFO, SOL, WIN, URN, CHA, WA1, WA2, EL1, HE2, EL2, FW3, HE3, EL3, HF3, LF3, CH3, GA3, CO3, BO3, CR3, DEL, DLG, DNG
** Hint: CO1, CO2, CO3, BO3 the first two are characters. 
    
4) Tech codes (new: 12 characters): 
    I) Not following any coding: BACKSTOP, BIOFUELX, CRUDPROX, CRUDRE1X, CRUDRE2X, ETHANOLX, LFRCFURX, NPCHA00X, WIND

    II) Power generation technologies/Power plants:
      ^^^______: first three characters represent country code
      ___^^^______: character 04-06 represent the type of fuel (BIO, COA, CHA, CO1, CO2, EL1, EL2, ETH, GEO, HE2, HFO, HYD, LFO, NGA, BIO, URN, SOL, WA2,           

    III) Extraction/import technologies

     IV) Transmission & distribution
     
     
     V) Conversion technologies:
     
     VI) Trade links:
         1) Exports_EL
         
         
         2) Exports_NG


     VII) Intermediate_NG:


* The 3 letters which represent the fuel correspond to the input fuel of the technology.
** The extraction and import technologies, the 3 letters which represent the fuel correspond to the output fuel of the technology
**Hint: GEO, HYD, NGA do not exist in the list of fuels

Example BM00X00X

^^^________ first three characters represent country code
___^^______ type of fuel
_____^^^___ type of technology ()
________^^_ cooling type (01, 02, 03, 04)
__________^ old or new (O or N)


5) Emission factor: 3 letters







# Old Naming conventions (Vignesh has already the scripts to read the technologies/fuels --> to be checked)
Old technology code (first 2 letters Country code),

New technology code (first 3 letters country code);
Power generation technologies: 3-4 letter type of fuel, 5-7 letter type of technology (if 7 letter is C then is CCS), 8-9 letter cooling type (01-04) and 10 letter old/new (0 or N) **
