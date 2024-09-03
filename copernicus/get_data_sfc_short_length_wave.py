import cdsapi

c = cdsapi.Client()

year =1990
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            '10m_u_component_of_neutral_wind', '10m_v_component_of_neutral_wind',
            'mean_sea_level_pressure', 
            # 'mean_wave_direction',
            # 'mean_direction_of_wind_waves',
            # 'mean_wave_period',
            # 'mean_period_of_wind_waves',  
            # 'mean_period_of_total_swell',
            'peak_wave_period', 
            'significant_height_of_combined_wind_waves_and_swell', 
            # 'significant_height_of_wind_waves',
            # 'significant_height_of_total_swell',
            # 'coefficient_of_drag_with_waves', 
        ],
        'year': f'{year}',
        'time': [
            '00:00', 
            # '01:00', '02:00',
            # '03:00', '04:00', '05:00',
            '06:00', 
            # '07:00', '08:00',
            # '09:00', '10:00', '11:00',
            '12:00',
            # '13:00', '14:00',
            # '15:00', '16:00', '17:00',
            '18:00',
            # '19:00', '20:00',
            # '21:00', '22:00', '23:00',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',            
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
    },
    f'/datasets/FourCastNet/wave_5var_6h/{year}.nc')