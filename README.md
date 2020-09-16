# Welcome to tess_infos!

This tool provides extremely fast Pythonic access to the full TICv8, GAIA DR2 and Banyan Sigma (Bayesian Young Associations Catalog) parameters for all TESS short-cadence targets from TESS Sectors 1--23. More Sectors and even more parameters (such as stellar rotation) will be added soon.


## Files

The full catalog is hosted in a .feather file (300 MB), for extremely fast Python accessing and data search. To keep GitHub light, you can simply [download it here](https://www.dropbox.com/s/h92c7vye460482h/unique_targets_S001-S023_obs_tic_gaia_banyan.feather?dl=0) and paste it into the directory where you installed tess_infos.  

## Install

    pip install tess_infos

## Quick start (1): get some TESS Infos of TOI-270 (TIC 259377017)

    from tess_infos.tess_infos import catalog
    cat = catalog()
    infos = cat.get(tic_id=259377017, keys=['OBS_Sector', 'TICv8_Tmag','GAIA_DR2_radial_velocity', 'BANYAN_BEST_YA']) 
    #get the Observing Sectors, the TESS magnitude, the GAIA DR2 radial velocity value, and the best Young Association hypothesis from Banyan Sigma
    
## Quick start (2): get Banyan Sigma output for all targets in Sectors 1 and 2
    from tess_infos.tess_infos import catalog
    cat = catalog(keys='BANYAN') #only load BANYAN columns into memory
    infos = cat.get(sector=[1,2]) #access only Sectors 1 and 2
    
## Tips
 If you plan to do a lot with it, it is better to load all the needed keys into memory first, and then retrieve them as you go along. For example (2), you could also call 
    
    cat = catalog() #only load BANYAN columns into memory
    infos = cat.get(sector=[1,2], keys='BANYAN') #access only Sectors 1--2 and only BANYAN

which takes a bit more memory but later in your code will you allow to also do:

    infos2 = cat.get(sector=[1,2], keys='TICv8') #access only Sectors 1--2 and only TICv8
    
## API and usage

### (1) load the catalog into memory

    cat = catalog(keys=None) 
   
   keys : None / str / list of str
   
   None / 'default': defaults to self.default_keys
   '*' / 'all': load all columns
   'OBS': load all columns starting with OBS_
   'TICv8': load all columns starting with TICv8_
   'GAIADR2':  load all columns starting with GAIADR2_
   'BANYAN': load all columns starting with BANYAN_
   'mag': load all TICv8 columns containing magnitudes
   
   Combinations are also possible:
   ['default','OBS','mag']   load all default columns + all columns from OBS + all magnitudes
	
### (2) access the full catalog from memory
    cat.data #this returns the full catalog from memory

### (3) get specific TICs, Sectors, and/or keys from memory
    infos = cat.get(tic_id=None, sector=None, keys=None) #this returns the specified entries

### (4) check which keys you can call
    cat.get_all_keys #returns the full list of keys
    cat.get_default_keys #returns the full list of keys
    cat.get_mag_keys #returns the full list of keys
