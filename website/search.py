from .digitalTree import DigitalTree

class Search:
    tree:DigitalTree = None

    @staticmethod
    def searchInit():
        if not Search.tree:
            Search.tree = DigitalTree()

    @staticmethod
    def search(username):
        result = Search.tree.autoCorrection(username) #list[tuple(name,mistakes)]
        best1 = float("inf")
        best2 = float("inf")
        best3 = float("inf")
        name1 = None
        name2 = None
        name3 = None
        for res in result:
            if res[1] == 0:
                return [res[0]]
            if res[1] <best1:
                best3,name3 = best2,name2
                best2,name2 = best1,name1
                best1,name1 = res[1],res[0]
            elif res[1] < best2:
                best3,name3 = best2,name2
                best2,name2 = res[1],res[0]
            elif res[1] < best3:
                best3,name3 = res[1],res[0]
        return [name1,name2,name3] 