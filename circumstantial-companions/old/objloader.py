from itertools import islice

class MeshData(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.vertex_format = [(b'v_pos', 3, 'float'),
                              (b'v_normal', 3, 'float'),
                              (b'v_tc0', 2, 'float')]
        self.vertices = []
        self.indices = []

    def calculate_normals(self):
        indices = iter(self.indices)
        while True:
            slices = islice(indices, 3)
            if not slices:
                break

            p1, p2, p3 = [self.vertices[index:index + 3] for index in indices]

            v = [p2[i] - p1[i] for i in range(3)]
            u = [p3[i] - p1[i] for i in range(3)]

            pairs = ((1, 2), (2, 0), (0, 1))
            n = [u[a] * v[b] - u[b] * v[a] for a, b in pairs]

            for index in slices:
                self.vertices[index + 3: index + 6] = n

class ObjFile:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.objects = {}
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self._current_object = None

        with open(filename, 'r') as obj:
            obj = obj.readlines()

        for line in obj:
            if (   not line.strip()
                or line.startswith('#')
                or line.startswith('s')):
                continue

            start, *rest = line.split()
            if start == 'o':
                self.finish_object()
                self._current_object, *_ = rest

            if start in ('v', 'vn'):
                vertex = list(map(float, rest))
                if swapyz:
                    vertex[1:] = vertex[-1:0:-1]
                (self.vertices if start == 'v' else self.normals).append(vertex)
            elif start == 'vt':
                self.texcoords.append(map(float, rest))
            elif start == 'f':
                lists = [face, texcoords, norms] = [[], [], []]
                for indices in rest:
                    for list_, index in zip(lists, indices.split('/')):
                        list_.append(int(index) if index else - 1)
                self.faces.append((face, norms, texcoords))
        self.finish_object()

    def finish_object(self):
        if self._current_object is None:
            return

        mesh = MeshData()
        for index, face in enumerate(self.faces):
            for vertex, norm, tex_coord in zip(*face):
                vertex = self.vertices[vertex - 1]
                norm = self.normals[norm - 1] if norm != -1 else (0.0, ) * 3
                tex_coord = self.texcoords[tex_coord - 1] if tex_coord != -1 else (0.0, ) * 2
                mesh.vertices.extend([*vertex, *norm, *tex_coord]) # Mesh vertices have len == 8
            mesh.indices.extend(range(index * 3, index * 3 + 3))

        self.objects[self._current_object] = mesh
        self.faces = []