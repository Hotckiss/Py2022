import numpy as np
from pathlib import Path

from src.my_matrix import MyMatrix
from src.mixin_matrix import Matrix, HashableMatrix


if __name__ == '__main__':
    rnd = np.random.RandomState(seed=0)
    a_data, b_data = rnd.randint(0, 10, (10, 10)), rnd.randint(0, 10, (10, 10))
    mp = lambda op: Path('artifacts', 'easy', f'matrix{op}.txt')
    a, b = MyMatrix(a_data), MyMatrix(b_data)
    mp('+').write_text(str(a + b))
    mp('*').write_text(str(a * b))
    mp('@').write_text(str(a @ b))

    a, b = Matrix(a_data), Matrix(b_data)

    (a + b).file_dump('artifacts/medium/matrix+.txt')
    (a * b).file_dump('artifacts/medium/matrix*.txt')
    (a @ b).file_dump('artifacts/medium/matrix@.txt')

    a = HashableMatrix([[10**9+7 + 1, 5], [5, 5]])
    c = HashableMatrix([[1, 5], [5, 5]])
    b = HashableMatrix([[5, 5], [5, 5]])
    d = HashableMatrix([[5, 5], [5, 5]])

    assert (hash(a) == hash(c)) and (a != c) and (b == d) and ((a @ b) == (c @ d)).matrix.all()
    
    a.file_dump('artifacts/hard/A.txt')
    b.file_dump('artifacts/hard/B.txt')
    c.file_dump('artifacts/hard/C.txt')
    d.file_dump('artifacts/hard/D.txt')
    (a @ b).file_dump('artifacts/hard/AB.txt')
    (Matrix(c.matrix) @ Matrix(d.matrix)).file_dump('artifacts/hard/CD.txt')
    Path('artifacts/hard/hashes.txt').write_text(f'{hash(a @ b)} {hash(c @ d)}')