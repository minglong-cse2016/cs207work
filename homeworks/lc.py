import reprlib
import itertools
import os
from collections import defaultdict

# lc_reader
def lc_reader(filename):
    lclist=[]
    dict_names=[]
    dict_values=[]
    with open(filename) as fp:
        
        for line in fp:
            
            if line.find('Field') != -1:
                dict_names = line[1:].split()
    
            if (line.find('#')==0) & (line.find('Field') == -1) & (line.find('MJD') == -1):
                dict_values = line[1:].split()
                
            if line.find('#')!=0:
                lclist.append([float(f) for f in line.strip().split()])
                
    dict_of_facets = dict(zip(dict_names, dict_values))
    
    return lclist, dict_of_facets


# LightCurve
class LightCurve:
    
    def __init__(self, data, metadict):
        self._time = [x[0] for x in data]
        self._amplitude = [x[1] for x in data]
        self._error = [x[2] for x in data]
        self.metadata = metadict
        self.filename = None
        # add self.timeseries
        self.timeseries = zip(self._time, self._amplitude)
    
    @classmethod
    def from_file(cls, filename):
        lclist, metadict = lc_reader(filename)
        instance = cls(lclist, metadict)
        instance.filename = filename
        return instance
    
    def __repr__(self):
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self.timeseries,0,10)))
        components = components[components.find('['):]
        return '{}({})'.format(class_name, components)        
        
    #your code here
    @property
    def time(self):
        return self._time
    
    @property
    def amplitude(self):
        return self._amplitude
    
    @property
    def timseries(self):
        return self.timeseries   

    def __len__(self):
        return len(self._time)
    
    def __getitem__(self, position):
        return (self._time[position], self._amplitude[position])


# LightCurveDB
class LightCurveDB:
    
    def __init__(self):
        self._collection={}
        self._field_index=defaultdict(list)
        self._tile_index=defaultdict(list)
        self._color_index=defaultdict(list)
    
    def populate(self, folder):
        for root,dirs,files in os.walk(folder): # DEPTH 1 ONLY
            for file in files:
                if file.find('.mjd')!=-1:
                    the_path = root+"/"+file
                    self._collection[file] = LightCurve.from_file(the_path)
    
    def index(self):
        for f in self._collection:
            #print(f)
            lc, tilestring, seq, color, _ = f.split('.')
            field = int(lc.split('_')[-1])
            tile = int(tilestring)
            self._field_index[field].append(self._collection[f])
            self._tile_index[tile].append(self._collection[f])
            self._color_index[color].append(self._collection[f])
        #print(self._tile_index[4289])    
     
    #your code here
    def retrieve(self, facet, value):
        if facet == 'tile':
            return self._tile_index[value]
        elif facet == 'field':
            return self._field_index[value]
        elif facet == 'color':
            return self._color_index[value]