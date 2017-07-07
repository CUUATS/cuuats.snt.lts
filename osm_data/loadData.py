from pandana.loaders import osm

network = osm.pdna_network_from_bbox(40.043386, -88.358231, 40.161034, -88.14537)
network.save_hdf5('cunetwork.h5')


