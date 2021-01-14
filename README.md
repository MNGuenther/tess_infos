# Welcome to tess_infos!

This tool provides Pythonic access to the full TICv8, GAIA DR2 and Banyan Sigma parameters for all TESS short-cadence targets from TESS Sectors 1--26. More Sectors and even more parameters (rotation, flares, ...) will be added soon.


## Files

The full catalog is hosted in a `feather' file (~300 MB), for extremely fast Python accessing and data search. To keep GitHub light, you can simply [download it here](https://www.dropbox.com/s/kx5w4xombyvf4tg/unique_targets_S001-S026_obs_tic_gaia_banyan.feather?dl=0) and save it anywhere on your computer.  


## Initialize

The first time you run tess_infos (or after updating it, or after downloading a new feather file) you have to initialize the software and tell it where you store the `feather' file on your computer. Simply call it once as:

    from tess_infos.tess_infos import catalog
    cat = catalog(path='path/to/my/dir/unique_targets_S001-S026_obs_tic_gaia_banyan.feather')

Really, you just have to do it once, then it's all good.


## Install

    pip install tess-infos 

Note: here it is a hyphen, everywhere else it is an underscore; thanks a lot, PyPi!


## Quick Start Example (1): Several infos of TOI-270 (TIC 259377017)

    from tess_infos.tess_infos import catalog
    cat = catalog()
    infos = cat.get(tic_id=259377017, keys=['OBS_Sector', 'TICv8_Tmag','GAIA_DR2_radial_velocity', 'BANYAN_BEST_YA']) 

Rhis will get the Observing Sectors, the TESS magnitude, the GAIA DR2 radial velocity value, and the best Young Association hypothesis from Banyan Sigma for TOI-270 (TIC 259377017).
    
## Quick Start Example (2): All Banyan Sigma infos for all targets in Sectors 1 and 2
    from tess_infos.tess_infos import catalog
    cat = catalog()
    infos = cat.get(sector=[1,2], keys=['BANYAN'])
    
This will get you all Banyan Sigma (Clusters & Associations) infos for all TIC IDs in Sectors 1 and 2.


## Tips: Speed and Memory

If you plan to do a lot with the catalog, it is best to load all the needed keys into memory first, and then retrieve them as you go along. That is what we did in Quick Start Examples (1) and (2). Another example of this:
    
    cat = catalog() #load absolutely all columns into memory
    infos = cat.get(sector=[1,2], keys='BANYAN') #access only Sectors 1--2 and only BANYAN
    [...] #all your other code
    infos2 = cat.get(tic_id= 259377017, keys='Tmag') #access a specific Tmag 

However, if you don't have much memory on your old laptop, only want to load a specific thing, or want to safe the 1 second of loading the entire catalog -- then it's best to directly pass your desired keys into the catalog() function. As in the above example, but now with less memory usage:

    cat = catalog(keys=['BANYAN','Tmag']) #load only the keys into memory that you know you'll need later
    infos = cat.get(sector=[1,2], keys='BANYAN') #access only Sectors 1--2 and only BANYAN
    [...] #all your other code
    infos2 = cat.get(tic_id= 259377017, keys='Tmag') #access a specific Tmag 

    
## API and Usage

### (1) load the catalog into memory

    cat = catalog(keys=None) 
   
   keys : None / str / list of str

 - None / 'default': load the default keys (only the most important ones; see `cat.get_default_keys()')
 - '*' / 'all': load all keys (same as cat.data; see `cat.get_all_keys()')
 - 'OBS': load all columns starting with OBS_
 - 'TICv8': load all columns starting with TICv8_
 - 'GAIADR2':  load all columns starting with GAIADR2_ 
 - 'BANYAN': load all columns starting with BANYAN_
 - 'mag': load all TICv8 columns containing magnitudes (see `cat.get_mag_keys()')

Combinations are also possible:
 - ['default','OBS','mag']   load all default columns + all columns from OBS + all magnitudes

	
### (2) access the full catalog from memory
    cat.data #this returns the full catalog from memory

### (3) get specific TICs, Sectors, and/or keys from memory
    infos = cat.get(tic_id=None, sector=None, keys=None) #this returns the specified entries

### (4) check which keys you can call
    cat.get_all_keys #returns the full list of keys
    cat.get_default_keys #returns the list of default keys
    cat.get_mag_keys #returns the list of magnitude-related keys
