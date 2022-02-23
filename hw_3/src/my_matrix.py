import copy


class MyMatrix:
    def __init__(self, data):
        if len(data) == 0:
            raise ValueError("empty matrix was passed")
        if len(data[0]) == 0:
            raise ValueError("empty row was passed")
        if any(map(lambda row: len(row) != len(data[0]), data)):
            raise ValueError(f'rows are not equal shaped')

        self._shape = (len(data), len(data[0]))
        self._data = data

    @property
    def shape(self):
        return self._shape

    def __getitem__(self, k):
        return self._data[k[0]][k[1]]

    def __setitem__(self, k, v):
        self._data[k[0]][k[1]] = v

    def __add__(self, o):
        if not isinstance(o, MyMatrix):
            raise ValueError("second is not a matrix")
        if self._shape != o.shape:
            raise ValueError("shapes are not equal")

        sum_data = copy.deepcopy(self._data)
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                sum_data[i, j] += o[i, j]
        return MyMatrix(sum_data)

    def __mul__(self, o):
        if not isinstance(o, MyMatrix):
            raise ValueError("second is not a matrix")
        if self._shape != o.shape:
            raise ValueError("shapes are not equal")

        mul_data = copy.deepcopy(self._data)
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                mul_data[i, j] *= o[i, j]
        return MyMatrix(mul_data)

    def __matmul__(self, o):
        if self._shape[1] != o.shape[0]:
            raise ValueError("required shapes are not equal")

        matmul_data = [[0] * o._shape[1] for _ in range(self._shape[0])]
        for i in range(self._shape[0]):
            for j in range(o._shape[1]):
                for k in range(self._shape[1]):
                    matmul_data[i][j] += self[i, k] * o[k, j]
        return MyMatrix(matmul_data)

    def __str__(self):
        return '[\n' + '\n'.join(map(lambda r: f' {r},', self._data)) + '\n]'
