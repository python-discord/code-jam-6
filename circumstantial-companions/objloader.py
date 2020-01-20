class MeshData(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.vertex_format = [(b'v_pos', 3, 'float'),
                              (b'v_normal', 3, 'float'),
                              (b'v_tc0', 2, 'float')]
        self.vertices = []
        self.indices = []

    def calculate_normals(self):
        for i in range(len(self.indices) / (3)):
            fi = i * 3
            indices = v1i, v2i, v3i = self.indices[fi:fi + 3]

            vs = self.vertices
            p1, p2, p3 = [vs[index:index + 3] for index in indices]

            v = [p2[i] - p1[i] for i in range(3)]
            u = [p3[i] - p1[i] for i in range(3)]

            pairs = ((1, 2), (2, 0), (0, 1))
            n = [u[a] * v[b] - u[b] * v[a] for a, b in pairs]

            for index in indices:
                self.vertices[index + 3: index + 6] = n

class ObjFile:
    def finish_object(self):
        if self._current_object is None:
            return

        mesh = MeshData()
        idx = 0
        for f in self.faces:
            verts = f[0]
            norms = f[1]
            tcs = f[2]
            for i in range(3):
                # get normal components
                n = (0.0, 0.0, 0.0)
                if norms[i] != -1:
                    n = self.normals[norms[i] - 1]

                # get texture coordinate components
                t = (0.0, 0.0)
                if tcs[i] != -1:
                    t = self.texcoords[tcs[i] - 1]

                # get vertex components
                v = self.vertices[verts[i] - 1]

                data = [v[0], v[1], v[2], n[0], n[1], n[2], t[0], t[1]]
                mesh.vertices.extend(data)

            tri = [idx, idx + 1, idx + 2]
            mesh.indices.extend(tri)
            idx += 3

        self.objects[self._current_object] = mesh
        # mesh.calculate_normals()
        self.faces = []

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
