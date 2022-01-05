'''Class structure describing external importations'''
from abc import ABC
from numpy import exp, ones, zeros
from scipy.interpolate import interp1d

class ImportModel(ABC):
    '''Abstract class for importation models'''
    def __init__(self,
                no_inf_compartments,
                no_age_classes):
        self.no_inf_compartments = no_inf_compartments
        self.no_age_classes = no_age_classes
        self.no_entries = no_inf_compartments * no_age_classes
    def cases(self, t):     # Cases is a list of import functions
        pass


class NoImportModel(ImportModel):
    def cases(self, t):
        return zeros(self.no_age_classes,)

    @classmethod
    def make_from_spec(cls, spec, det):
        return cls()


class FixedImportModel(ImportModel):
    def __init__(
            self,
            no_inf_compartments,
            no_age_classes,
            import_array):
        '''import_arrays should be a list of arrays. The number of arrays is
        no_inf_compartments and each has length no_age_classes. The jth element of
        the ith array is the rate at which individuals in age class j are infected
        by external cases in infectious compartment i.'''
        super().__init__(no_inf_compartments, no_age_classes)
        self.import_array = import_array

    def cases(self, t):
        return self.import_array

class StepImportModel(ImportModel):
    def __init__(
            self,
            time,
            external_prevalance):       # External prevalence is now a age classes by inf compartments array
        self.prevalence_interpolant = []
        for i in range(self.no_entries):
            self.prevalence_interpolant.append(interp1d(
                time, external_prevalance[i,:],
                kind='nearest',
                bounds_error=False,
                fill_value='extrapolate',
                assume_sorted=True))

    def cases(self, t):
        imports = zeros(no_entries,)
        for i in range(self.no_entries):
            imports[i] = self.prevalence_interpolant[i](t)
        return imports
