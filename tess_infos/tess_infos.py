#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 18:28:06 2020

@author:
Maximilian N. Günther
MIT Kavli Institute for Astrophysics and Space Research, 
Massachusetts Institute of Technology,
77 Massachusetts Avenue,
Cambridge, MA 02109, 
USA
Email: maxgue@mit.edu
Web: www.mnguenther.com
"""

from __future__ import print_function, division, absolute_import

#::: modules
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from glob import glob
from pprint import pprint
import feather
from time import time as timer
from pathlib import Path

#::: my modules
import allesfitter

#::: plotting settings
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({"xtick.direction": "in","ytick.direction": "in"})
sns.set_context(rc={'lines.markeredgewidth': 1})




__version__ = '0.1.0'



class catalog(object):
    '''
    keys: 
        None / default   defaults to self.default_keys
        * / all          load all columns
        OBS              load all columns starting with OBS_
        TICv8            load all columns starting with TICv8_
        GAIADR2          load all columns starting with GAIADR2_
        BANYAN           load all columns starting with BANYAN_
        mag              load all TICv8 columns containing magnitudes
        
        also possible:
        ['default','OBS','mag']   load all default columns + all columns from OBS + all magnitudes
    '''
    
    def __init__(self, keys=None, path=None):
        
        #::: set the path to the catalog file
        if path is None:
            path = Path(__file__).parent.absolute()
        
        #::: translate input into keys
        keys = list(np.atleast_1d(keys))
        
        if None in keys:
            keys += self.get_default_keys()
            keys.remove(None)
            
        if 'default' in keys:
            keys += self.get_default_keys()
            keys.remove('default')
            
        if 'all' in keys:
            keys = self.get_all_keys()
            
        if '*' in keys:
            keys = self.get_all_keys()
        
        if 'mag' in keys:
            keys += self.get_magnitude_keys()
        
        keys = [i for i in self.get_all_keys() if any([s in i for s in keys])] #translate wild cards into keys
        used = set() #buffer
        keys = [x for x in keys if x not in used and (used.add(x) or True)] #make it unique while keeping the order
        del used
        
        #::: 15.8 seconds to load all
        # f = '/Users/mx/Dropbox (Personal)/Science/TESS/TESS_SC_target_lists/unique_targets_S001-S023_obs_tic_gaia_banyan.csv.gz'
        # self.data = pd.read_csv(f, dtype=str, usecols=keys)
        
        #::: 11.8 seconds to load all
        # f = '/Users/mx/Dropbox (Personal)/Science/TESS/TESS_SC_target_lists/unique_targets_S001-S023_obs_tic_gaia_banyan.h5'
        # self.data = pd.read_hdf(f, dtype=str, usecols=keys)
        
        #::: 8.2 seconds to load all
        # f = '/Users/mx/Dropbox (Personal)/Science/TESS/TESS_SC_target_lists/unique_targets_S001-S023_obs_tic_gaia_banyan.feather'
        f = os.path.join(path, 'unique_targets_S001-S023_obs_tic_gaia_banyan.feather')
        self.data = pd.read_feather(f, columns=keys)
        
        
        
    def get(self, tic_id=None, sector=None, keys=None):
        df2 = self.data
        
        #::: filter by tic_id(s), select only requested rows
        if tic_id is not None: 
            tic_id = [str(int(t)) for t in np.atleast_1d(tic_id)]
            df2 = df2.loc[df2['TIC_ID'].isin(list(tic_id))]
            df2 = pd.merge(pd.DataFrame(data=tic_id,columns=['TIC_ID_requested'],dtype=str), df2, left_on='TIC_ID_requested', right_on='TIC_ID', how='left')
            # df2 = df2.iloc[pd.Index(df2['TIC_ID']).get_indexer(list(tic_id))]
        
        #::: filter by sector(s), select only requested rows
        if sector is not None: 
            ind = [False]*len(df2)
            sector = [str(x) for x in np.atleast_1d(sector)]
            for i in range(len(df2)):
                a = list(set(sector) & set(df2['OBS_Sector'][i].split(';')))
                if len(a)>0: ind[i] = True
            df2 = df2[ind]
        
        #::: filter by keys, select only requested columns
        if keys is not None:
            keys = list(np.atleast_1d(keys))
            keys += ['TIC_ID_requested']
            df2 = df2[keys]
            
        return df2
    
    
    
    def get_all_keys(self):
        return ['TIC_ID',
                 'OBS_TICID',
                 'OBS_Tmag',
                 'OBS_RA',
                 'OBS_Dec',
                 'OBS_Sector',
                 'OBS_Camera',
                 'OBS_CCD',
                 'TICv8_ID',
                 'TICv8_version',
                 'TICv8_HIP',
                 'TICv8_TYC',
                 'TICv8_UCAC',
                 'TICv8_TWOMASS',
                 'TICv8_SDSS',
                 'TICv8_ALLWISE',
                 'TICv8_GAIA',
                 'TICv8_APASS',
                 'TICv8_KIC',
                 'TICv8_objType',
                 'TICv8_typeSrc',
                 'TICv8_ra',
                 'TICv8_dec',
                 'TICv8_POSflag',
                 'TICv8_pmRA',
                 'TICv8_e_pmRA',
                 'TICv8_pmDEC',
                 'TICv8_e_pmDEC',
                 'TICv8_PMflag',
                 'TICv8_plx',
                 'TICv8_e_plx',
                 'TICv8_PARflag',
                 'TICv8_gallong',
                 'TICv8_gallat',
                 'TICv8_eclong',
                 'TICv8_eclat',
                 'TICv8_Bmag',
                 'TICv8_e_Bmag',
                 'TICv8_Vmag',
                 'TICv8_e_Vmag',
                 'TICv8_umag',
                 'TICv8_e_umag',
                 'TICv8_gmag',
                 'TICv8_e_gmag',
                 'TICv8_rmag',
                 'TICv8_e_rmag',
                 'TICv8_imag',
                 'TICv8_e_imag',
                 'TICv8_zmag',
                 'TICv8_e_zmag',
                 'TICv8_Jmag',
                 'TICv8_e_Jmag',
                 'TICv8_Hmag',
                 'TICv8_e_Hmag',
                 'TICv8_Kmag',
                 'TICv8_e_Kmag',
                 'TICv8_TWOMflag',
                 'TICv8_prox',
                 'TICv8_w1mag',
                 'TICv8_e_w1mag',
                 'TICv8_w2mag',
                 'TICv8_e_w2mag',
                 'TICv8_w3mag',
                 'TICv8_e_w3mag',
                 'TICv8_w4mag',
                 'TICv8_e_w4mag',
                 'TICv8_GAIAmag',
                 'TICv8_e_GAIAmag',
                 'TICv8_Tmag',
                 'TICv8_e_Tmag',
                 'TICv8_TESSflag',
                 'TICv8_SPFlag',
                 'TICv8_Teff',
                 'TICv8_e_Teff',
                 'TICv8_logg',
                 'TICv8_e_logg',
                 'TICv8_MH',
                 'TICv8_e_MH',
                 'TICv8_rad',
                 'TICv8_e_rad',
                 'TICv8_mass',
                 'TICv8_e_mass',
                 'TICv8_rho',
                 'TICv8_e_rho',
                 'TICv8_lumclass',
                 'TICv8_lum',
                 'TICv8_e_lum',
                 'TICv8_d',
                 'TICv8_e_d',
                 'TICv8_ebv',
                 'TICv8_e_ebv',
                 'TICv8_numcont',
                 'TICv8_contratio',
                 'TICv8_disposition',
                 'TICv8_duplicate_id',
                 'TICv8_priority',
                 'TICv8_eneg_EBV',
                 'TICv8_epos_EBV',
                 'TICv8_EBVflag',
                 'TICv8_eneg_Mass',
                 'TICv8_epos_Mass',
                 'TICv8_eneg_Rad',
                 'TICv8_epos_Rad',
                 'TICv8_eneg_rho',
                 'TICv8_epos_rho',
                 'TICv8_eneg_logg',
                 'TICv8_epos_logg',
                 'TICv8_eneg_lum',
                 'TICv8_epos_lum',
                 'TICv8_eneg_dist',
                 'TICv8_epos_dist',
                 'TICv8_distflag',
                 'TICv8_eneg_Teff',
                 'TICv8_epos_Teff',
                 'TICv8_TeffFlag',
                 'TICv8_gaiabp',
                 'TICv8_e_gaiabp',
                 'TICv8_gaiarp',
                 'TICv8_e_gaiarp',
                 'TICv8_gaiaqflag',
                 'TICv8_starchareFlag',
                 'TICv8_VmagFlag',
                 'TICv8_BmagFlag',
                 'TICv8_splists',
                 'TICv8_e_RA',
                 'TICv8_e_Dec',
                 'TICv8_RA_orig',
                 'TICv8_Dec_orig',
                 'TICv8_e_RA_orig',
                 'TICv8_e_Dec_orig',
                 'TICv8_raddflag',
                 'TICv8_wdflag',
                 'TICv8_objID',
                 'GAIADR2_source_id',
                 'GAIADR2_random_index',
                 'GAIADR2_ref_epoch',
                 'GAIADR2_ra',
                 'GAIADR2_ra_error',
                 'GAIADR2_dec',
                 'GAIADR2_dec_error',
                 'GAIADR2_parallax',
                 'GAIADR2_parallax_error',
                 'GAIADR2_parallax_over_error',
                 'GAIADR2_pmra',
                 'GAIADR2_pmra_error',
                 'GAIADR2_pmdec',
                 'GAIADR2_pmdec_error',
                 'GAIADR2_ra_dec_corr',
                 'GAIADR2_ra_parallax_corr',
                 'GAIADR2_ra_pmra_corr',
                 'GAIADR2_ra_pmdec_corr',
                 'GAIADR2_dec_parallax_corr',
                 'GAIADR2_dec_pmra_corr',
                 'GAIADR2_dec_pmdec_corr',
                 'GAIADR2_parallax_pmra_corr',
                 'GAIADR2_parallax_pmdec_corr',
                 'GAIADR2_pmra_pmdec_corr',
                 'GAIADR2_astrometric_n_obs_al',
                 'GAIADR2_astrometric_n_obs_ac',
                 'GAIADR2_astrometric_n_good_obs_al',
                 'GAIADR2_astrometric_n_bad_obs_al',
                 'GAIADR2_astrometric_gof_al',
                 'GAIADR2_astrometric_chi2_al',
                 'GAIADR2_astrometric_excess_noise',
                 'GAIADR2_astrometric_excess_noise_sig',
                 'GAIADR2_astrometric_params_solved',
                 'GAIADR2_astrometric_primary_flag',
                 'GAIADR2_astrometric_weight_al',
                 'GAIADR2_astrometric_pseudo_colour',
                 'GAIADR2_astrometric_pseudo_colour_error',
                 'GAIADR2_mean_varpi_factor_al',
                 'GAIADR2_astrometric_matched_observations',
                 'GAIADR2_visibility_periods_used',
                 'GAIADR2_astrometric_sigma5d_max',
                 'GAIADR2_frame_rotator_object_type',
                 'GAIADR2_matched_observations',
                 'GAIADR2_duplicated_source',
                 'GAIADR2_phot_g_n_obs',
                 'GAIADR2_phot_g_mean_flux',
                 'GAIADR2_phot_g_mean_flux_error',
                 'GAIADR2_phot_g_mean_flux_over_error',
                 'GAIADR2_phot_g_mean_mag',
                 'GAIADR2_phot_bp_n_obs',
                 'GAIADR2_phot_bp_mean_flux',
                 'GAIADR2_phot_bp_mean_flux_error',
                 'GAIADR2_phot_bp_mean_flux_over_error',
                 'GAIADR2_phot_bp_mean_mag',
                 'GAIADR2_phot_rp_n_obs',
                 'GAIADR2_phot_rp_mean_flux',
                 'GAIADR2_phot_rp_mean_flux_error',
                 'GAIADR2_phot_rp_mean_flux_over_error',
                 'GAIADR2_phot_rp_mean_mag',
                 'GAIADR2_phot_bp_rp_excess_factor',
                 'GAIADR2_phot_proc_mode',
                 'GAIADR2_bp_rp',
                 'GAIADR2_bp_g',
                 'GAIADR2_g_rp',
                 'GAIADR2_radial_velocity',
                 'GAIADR2_radial_velocity_error',
                 'GAIADR2_rv_nb_transits',
                 'GAIADR2_rv_template_teff',
                 'GAIADR2_rv_template_logg',
                 'GAIADR2_rv_template_fe_h',
                 'GAIADR2_phot_variable_flag',
                 'GAIADR2_l',
                 'GAIADR2_b',
                 'GAIADR2_ecl_lon',
                 'GAIADR2_ecl_lat',
                 'GAIADR2_priam_flags',
                 'GAIADR2_teff_val',
                 'GAIADR2_teff_percentile_lower',
                 'GAIADR2_teff_percentile_upper',
                 'GAIADR2_a_g_val',
                 'GAIADR2_a_g_percentile_lower',
                 'GAIADR2_a_g_percentile_upper',
                 'GAIADR2_e_bp_min_rp_val',
                 'GAIADR2_e_bp_min_rp_percentile_lower',
                 'GAIADR2_e_bp_min_rp_percentile_upper',
                 'GAIADR2_flame_flags',
                 'GAIADR2_radius_val',
                 'GAIADR2_radius_percentile_lower',
                 'GAIADR2_radius_percentile_upper',
                 'GAIADR2_lum_val',
                 'GAIADR2_lum_percentile_lower',
                 'GAIADR2_lum_percentile_upper',
                 'BANYAN_TIC_ID',
                 'BANYAN_YA_PROB',
                 'BANYAN_LIST_PROB_YAS',
                 'BANYAN_BEST_HYP',
                 'BANYAN_BEST_YA']
    
    
    
    def get_default_keys(self):
        return ['TIC_ID',
                 'OBS_Sector',
                 'TICv8_TWOMASS',
                 'TICv8_GAIA',
                 'TICv8_ra',
                 'TICv8_dec',
                 'TICv8_pmRA',
                 'TICv8_e_pmRA',
                 'TICv8_pmDEC',
                 'TICv8_e_pmDEC',
                 'TICv8_plx',
                 'TICv8_e_plx',
                 'TICv8_Vmag',
                 'TICv8_Kmag',
                 'TICv8_GAIAmag',
                 'TICv8_Tmag',
                 'TICv8_Teff',
                 'TICv8_e_Teff',
                 'TICv8_logg',
                 'TICv8_e_logg',
                 'TICv8_MH',
                 'TICv8_e_MH',
                 'TICv8_rad',
                 'TICv8_e_rad',
                 'TICv8_mass',
                 'TICv8_e_mass',
                 'TICv8_rho',
                 'TICv8_e_rho',
                 'TICv8_lumclass',
                 'TICv8_lum',
                 'TICv8_e_lum',
                 'TICv8_d',
                 'TICv8_e_d',
                 'TICv8_ebv',
                 'TICv8_e_ebv',
                 'TICv8_contratio',
                 'TICv8_disposition',
                 'TICv8_gaiabp',
                 'TICv8_gaiarp',
                 'TICv8_e_RA',
                 'TICv8_e_Dec',
                 'GAIADR2_radial_velocity',
                 'GAIADR2_radial_velocity_error',
                 'BANYAN_YA_PROB',
                 'BANYAN_BEST_HYP']
    
    

    def get_magnitude_keys(self):
        return ['TICv8_Bmag',
                 'TICv8_e_Bmag',
                 'TICv8_Vmag',
                 'TICv8_e_Vmag',
                 'TICv8_umag',
                 'TICv8_e_umag',
                 'TICv8_gmag',
                 'TICv8_e_gmag',
                 'TICv8_rmag',
                 'TICv8_e_rmag',
                 'TICv8_imag',
                 'TICv8_e_imag',
                 'TICv8_zmag',
                 'TICv8_e_zmag',
                 'TICv8_Jmag',
                 'TICv8_e_Jmag',
                 'TICv8_Hmag',
                 'TICv8_e_Hmag',
                 'TICv8_Kmag',
                 'TICv8_e_Kmag',
                 'TICv8_TWOMflag',
                 'TICv8_prox',
                 'TICv8_w1mag',
                 'TICv8_e_w1mag',
                 'TICv8_w2mag',
                 'TICv8_e_w2mag',
                 'TICv8_w3mag',
                 'TICv8_e_w3mag',
                 'TICv8_w4mag',
                 'TICv8_e_w4mag',
                 'TICv8_GAIAmag',
                 'TICv8_e_GAIAmag',
                 'TICv8_Tmag',
                 'TICv8_e_Tmag']



if __name__ == '__main__':
    t0 = timer()
    cat = catalog()
    t1 = timer()
    print('took',t1-t0,'s')
    print(cat.data)




# def load(tic_id=None, sector=None, keys=None):
#     f = '/Users/mx/Dropbox (Personal)/Science/TESS/TESS_SC_target_lists/unique_targets_S001-S023_obs_tic_gaia_banyan.csv.gz'
#     df = pd.read_csv(f, dtype=str, usecols=keys)
    
#     #::: filter by tic_id(s), select only requested rows
#     if tic_id is not None: 
#         tic_id = [str(int(t)) for t in np.atleast_1d(tic_id)]
#         df = df.loc[df['TIC_ID'].isin(list(tic_id))]
    
#     #::: filter by sector(s), select only requested rows
#     if sector is not None: 
#         ind = [False]*len(df)
#         sector = [str(x) for x in np.atleast_1d(sector)]
#         for i in range(len(df)):
#             a = list(set(sector) & set(df['OBS_Sector'][i].split(';')))
#             if len(a)>0: ind[i] = True
#         df = df[ind]
        
#     return df


# load(1078)