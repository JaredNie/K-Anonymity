from treelib import Tree

class Tree1(Tree):

    def createTree(self,path):
        infile = open(path, 'r')
        lines = infile.readlines()  # 读取多行

        tree1 = Tree()
        #['Anv;Professional,Artist\n', 'Professional;Lawyer,Engineer,Doctor\n', 'Artist;Writer,Dancer,Singer\n']
        line1 = lines[0] # Anv;Professional,Artist\n
        root = line1.split(';')[0] #root = Anv
        children = line1.split(';')[1][:-1] #children = Professional,Artist
        childs = children.split(',')#['Professional', 'Artist']

        tree1.create_node(root, root) #创建父节点 Anv
        for child in childs:
            tree1.create_node(child, child, parent=root)
        #创建两个子节点 Professional Artist

        for line in lines[1:]:
            parent = line.split(';')[0]
            children = line.split(';')[1][:-1]
            childs1 = children.split(',')
            for child1 in childs1:
                tree1.create_node(child1, child1, parent=parent)
        return tree1



