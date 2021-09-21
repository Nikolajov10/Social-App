class DigitalNode:
    END_KEY = "EOK"
    def __init__(self,value):
        self.val = value
        self.childs = [] # list of DigitalNodes
        self.freq = 0

class DigitalTree:
    def __init__(self):
        """
        storing usernames letter by letter and searching 
        """
        self.roots = []
    
    def addWord(self,word):
        """
        adding word to tree letter by letter
        if word alredy exist just update freq of every node
        else new EOK and nodes will be inserted
        """
        current_level = self.roots
        for letter in word:
            found_node = None
            for node in current_level:
                if node.val == letter:
                    node.freq += 1
                    found_node=node
                    break
            if found_node:
                current_level = found_node.childs
            else:
                found_node = DigitalNode(letter)
                current_level.append(found_node)
                current_level = found_node.childs
        found_end = False
        for node in current_level:
            if node.val  == DigitalNode.END_KEY:
                node.freq += 1
                found_end= True
                break
        if not found_end:
            current_level.append(DigitalNode(DigitalNode.END_KEY))
    
    def autoCorrection(self,search_input):
        """
        returns the best cases for search_input
        if the input is correct it will return the right word
        """
        results = []
        def findRec(current_level,current_word,current_len,mistakes,word,index,word_len):
            """
            return: tuple(word,mistakes) or None
            """
            if (mistakes > word_len // 3 and index<word_len) or mistakes > word_len // 2:
                return None
            if len(current_level)==0:
                add_mistake = 0
                if word_len < current_len:
                    add_mistake =  current_len -word_len 
                return (current_word,mistakes + add_mistake)
            index = index if index < word_len else word_len-1
            for node in current_level:
                if node.val == word[index]:
                   result = findRec(node.childs,current_word+node.val,current_len+1,mistakes,word,index+1,word_len)
                elif node.val != DigitalNode.END_KEY:
                    if index==0:
                        result = findRec(node.childs,current_word+node.val,current_len+1,mistakes+1,word,index,word_len)
                    else:
                        result = findRec(node.childs,current_word+node.val,current_len+1,mistakes+1,word,index+1,word_len)
                else:
                    result = findRec([],current_word,current_len,mistakes,word,word_len,word_len)
                if result:
                    results.append(result)
            return None

        findRec(self.roots,"",0,0,search_input,0,len(search_input))
        return results

"""
TESTING DIGITAL TREE

import names
tree = DigitalTree()
for i in range(100):
    name = names.get_first_name()
    tree.addWord(name)
tree.autoCorrection("Richard")
tree.autoCorrection("Richedd")
tree.autoCorrection("Nakkk")
tree.autoCorrection("Nancy")
"""

                
