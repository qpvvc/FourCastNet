import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            'model_bathymetry',
        ],
        'year': '2021',
        'month': '10',
        'day': [
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': [
            '00:00', '06:00', '12:00',
            '18:00',
        ],
    },
    '/datasets/FourCastNet/oct_2021_19_31_bath.nc')