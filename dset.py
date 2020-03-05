class DsetHandler():
    '''Allows lazy loading of examples, i.e. only loads an example if the
    current index is changed.
    '''

    def __init__(self, dataset):
        self.dset = dataset
        self._index = None

    def __getitem__(self, idx):
        if self._index != idx:
            self.ex = self.dset[idx]
            self._index = idx

            print('loading new example')

        return self.ex
