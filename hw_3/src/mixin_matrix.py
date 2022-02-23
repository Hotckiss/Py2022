import numpy as np
from numbers import Number
from pathlib import Path


class _MyMatrixPropertyMixin:
    @property
    def matrix(self):
        return self._data

    @matrix.setter
    def matrix(self, data):
        self._data = np.asarray(data)


class _MyMatrixStrMixin:
    def __str__(self):
        return '[\n' + '\n'.join(map(lambda row: f' {list(row)},', self._data)) + '\n]'


class _MyMatrixFileDumpMixin:
    def file_dump(self, path):
        Path(path).write_text(str(self))


class _MatrixHashMixin:
    def __hash__(self):
        summ = 0
        for r in self._data:
            summ += sum(r)
        return int(summ) % (10 ** 9 + 7)


class _MyMatrixOperationsMixin(np.lib.mixins.NDArrayOperatorsMixin):
    _HANDLED_TYPES = (np.ndarray, Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (_MyMatrixOperationsMixin,)):
                return NotImplemented

        inputs = tuple(x.matrix if isinstance(x, _MyMatrixOperationsMixin) else x for x in inputs)
        if out:
            kwargs['out'] = tuple(x.matrix if isinstance(x, _MyMatrixOperationsMixin) else x for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


class Matrix(_MyMatrixPropertyMixin, _MyMatrixOperationsMixin, _MyMatrixStrMixin, _MyMatrixFileDumpMixin):
    def __init__(self, data):
        self._data = np.asarray(data)
        if len(self._data.shape) != 2:
            raise ValueError(f'not 2D matrix')


class HashableMatrix(Matrix, _MatrixHashMixin):
    _cache = {}

    __hash__ = _MatrixHashMixin.__hash__

    def __matmul__(self, o):
        if self.matrix.shape[1] != self.matrix.shape[0]:
            raise ValueError("required shapes are not equal")

        h1, h2 = hash(self), hash(o)
        if (h1, h2) in self._cache:
            return self._cache[(h1, h2)]

        result = HashableMatrix(self.matrix @ o.matrix)
        self._cache[(h1, h2)] = result

        return result
