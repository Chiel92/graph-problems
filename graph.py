from random import sample, random
from .bitset import iterate, size, contains, bit, bits, disjoint, index, domain, tolist


class Graph:

    def __init__(self, vertices=None, neighborhoods=None):
        self.neighborhoods = neighborhoods or {}
        self._vertices = vertices or 0

    @property
    def vertices(self):
        return self._vertices

    def __repr__(self):
        return 'vertices: {}'.format(list(self.vertices))

    def __str__(self):
        return repr(self)

    def __iter__(self):
        """Iterate over all vertices."""
        return iterate(self.vertices)

    def __contains__(self, v):
        """Test if we contain vertex v."""
        return contains(self.vertices, v)

    def __len__(self):
        """Iterate over all vertices."""
        return size(self.vertices)

    def __call__(self, vertices):
        """Return the union of neighborhoods of vertices."""
        result = 0
        for v in iterate(vertices):
            result = result | self.neighborhoods[v]
            #result |= self.neighborhoods[v]
        return result

    def __getitem__(self, vertices):
        """Return the union of neighborhoods of vertices including the vertices."""
        return self(vertices) | vertices

    @property
    def edges(self):
        """Iterate over each pair of connected vertices exactly once."""
        for v in self:
            for w in iterate(self(v)):
                if w < v:
                    yield v, w

    def add(self, vertices):
        """Add new vertices to the graph."""
        assert isinstance(vertices, int)
        if not disjoint(self.vertices, vertices):
            raise ValueError('Graph already contain some of [{}]'.format(vertices))

        self._vertices |= vertices

        for v in iterate(vertices):
            self.neighborhoods[v] = 0

    def remove(self, vertices):
        """Remove vertices from the graph."""
        if not vertices in self.vertices:
            raise ValueError('Graph don\'t contain some of [{}]'.format(vertices))

        for v in iterate(vertices):
            for w in iterate(self(v)):
                self.disconnect(v, w)

        self._vertices -= vertices

        for v in iterate(vertices):
            del self.neighborhoods[v]

    def connect(self, v, w):
        """Connect two vertices."""
        if not v in self:
            raise ValueError('{} not in graph'.format(v))
        if not w in self:
            raise ValueError('{} not in graph'.format(w))

        if w == v:
            raise ValueError('{} and {} are the same vertex.'.format(v, w))

        # if w in self(v):
            #raise ValueError('{} and {} already connected.'.format(v, w))

        # Only support undirected edges
        #assert not v in self(w)

        self.neighborhoods[v] |= w
        self.neighborhoods[w] |= v

    def disconnect(self, v, w):
        """Disconnect two vertices."""
        if not v in self:
            raise ValueError
        if not w in self:
            raise ValueError

        if w == v:
            raise ValueError('{} and {} are the same vertex.'.format(v, w))

        if not contains(self(v), w):
            raise ValueError('{} and {} are not connected.'.format(v, w))

        # Only support undirected edges
        assert contains(self(w), v)

        self.neighborhoods[v] -= w
        self.neighborhoods[w] -= v

    def contract(self, v):
        """Contract a vertex."""
        if not v in self:
            raise ValueError

        neighbors = list(iterate(self(v)))
        self.remove(v)

        for w1 in neighbors:
            for w2 in neighbors:
                if w1 < w2 and not w1 in self[w2]:
                    self.connect(w1, w2)

    def split(self, v, w):
        """Split edge between two vertices."""
        if not v in self:
            raise ValueError
        if not w in self:
            raise ValueError

        if w == v:
            raise ValueError('{} and {} are the same vertex.'.format(v, w))

        if contains(self(v), w):
            raise ValueError('{} and {} are not connected.'.format(v, w))

        # Only support undirected edges
        assert contains(self(w), v)

        new = bit(size(self.vertices))
        self.add(new)
        self.disconnect(v, w)
        self.connect(v, new)
        self.connect(w, new)

    def complement(self):
        """Construct a graph representing the complement of self."""
        setlength = len(self)
        neighborhoods = {v: self[v].invert(setlength) for v in self}
        return Graph(self.vertices, neighborhoods)

    def subgraph(self, vertices):
        """Return a graph which is the subgraph of self induced by given vertex subset."""
        neighborhoods = {v: self(v) & vertices for v in self}
        return Graph(self.vertices, neighborhoods)

    def verify_symmetry(self):
        for v in self:
            for w in iterate(self(v)):
                assert v in self(w)

    def adjacency_matrix(self):
        length = domain(self.vertices) + 1
        result = []
        for i in range(length):
            v = bit(i)
            if v in self:
                result.append(tuple(tolist(self(v), length)))
            else:
                result.append(tuple([0] * length))
        return result

    @property
    def density(self):
        n = size(self.vertices)
        m = len(list(self.edges))
        return float(2 * m) / float(n * (n - 1))

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write('p edges {} {}\n'.format(size(self.vertices), len(list(self.edges))))
            f.writelines(
                'n {}\n'.format(index(v)) for v in self
            )
            f.writelines(
                'e {} {}\n'.format(index(v), index(w)) for v, w in self.edges
            )

    @staticmethod
    def load(filename):
        graph = Graph()
        with open(filename, 'r') as f:
            while 1:
                line = f.readline()
                #print('Parsing `{}`'.format(line[:-1]))
                if line == '':
                    break
                if line == '\n':
                    continue

                if line[0] == 'n':
                    v = bit(int(line[1:]))
                    graph.add(v)
                elif line[0] == 'e':
                    edge = line[1:].split()
                    v, w = bit(int(edge[0])), bit(int(edge[1]))
                    if v not in graph:
                        graph.add(v)
                    if w not in graph:
                        graph.add(w)
                    graph.connect(v, w)
        print('Graph loaded')
        return graph

    @staticmethod
    def generate_random(nr_vertices, nr_edges=0):
        if not 0 <= nr_edges <= nr_vertices * (nr_vertices - 1) / 2:
            raise ValueError

        if not nr_edges:
            nr_edges = 0.5

        graph = Graph()
        graph.add(bits(*range(nr_vertices)))

        if nr_edges < 1:
            # Add random edges between groups
            for v in graph:
                for w in graph:
                    if v < w and random() < nr_edges:
                        graph.connect(v, w)
            return graph
        else:
            vertex_list = list(iterate(graph.vertices))
            for _ in range(nr_edges):
                while 1:
                    v, w = sample(vertex_list, 2)
                    # Don't connect vertices twice
                    if not w in graph[v]:
                        break
                graph.connect(v, w)

            return graph

