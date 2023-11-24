class Obj:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in self.lines:
            try:
                prefix, value = line.split(" ", 1)
            except:
                continue

            if prefix == "v":  # Vertices
                self.vertices.append(list(map(float, list(filter(None, value.split(" "))))))
            elif prefix == "vt":  # Texture coordinates
                self.texcoords.append(list(map(float, list(filter(None, value.split(" "))))))
            elif prefix == "vn":  # Normals
                self.normals.append(list(map(float, list(filter(None, value.split(" "))))))
            elif prefix == "f":  # Faces
                self.faces.append([list(map(int, list(filter(None, vert.split("/"))))) for vert in
                                   list(filter(None, value.split(" ")))])

    def parse_data(self):
        objData = []
        for face in self.faces:
            if len(face) == 3:
                for vertexInfo in face:
                    vertexId, texcoordId, normalId = vertexInfo
                    vertex = self.vertices[vertexId - 1]
                    normals = self.normals[normalId - 1]
                    uv = self.texcoords[texcoordId - 1]
                    uv = [uv[0], uv[1]]
                    objData.extend(vertex + uv + normals)
            elif len(face) == 4:
                for i in [0, 1, 2]:
                    vertexInfo = face[i]
                    vertexId, texcoordId, normalId = vertexInfo
                    vertex = self.vertices[vertexId - 1]
                    normals = self.normals[normalId - 1]
                    uv = self.texcoords[texcoordId - 1]
                    uv = [uv[0], uv[1]]
                    objData.extend(vertex + uv + normals)
                for i in [0, 2, 3]:
                    vertexInfo = face[i]
                    vertexId, texcoordId, normalId = vertexInfo
                    vertex = self.vertices[vertexId - 1]
                    normals = self.normals[normalId - 1]
                    uv = self.texcoords[texcoordId - 1]
                    uv = [uv[0], uv[1]]
                    objData.extend(vertex + uv + normals)

        return objData