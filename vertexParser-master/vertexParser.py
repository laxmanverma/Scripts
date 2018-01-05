def getAllVertices(file, text):
    file = 'copy' + file
    end = 0
    start = text.find("vertices", end)
    #print(start)
    if start == -1:
        return 
    beg = text[start-1:start+11]    
    with open(file, "w+") as wr:
        wr.write(beg + '\n')
    wr.close()
        
    start += 10

    while(1):
        start = text.find("{", start)
        if start == -1:
            with open(file, "a+") as wr:
                wr.write("]")
            wr.close()
            return
        end = text.find("}", start)
        vertex = text[start:end+1]
        with open(file, "a+") as wr:
            wr.write(vertex + ',' + '\n')
        wr.close()
        start = end
        """if start == -1:
            with open(file, "a+") as wr:
                wr.write(",]")
            wr.close()
            exit()"""

def start():
    while(1):
        file = input("\nEnter the file name: (-1 to exit)")
        if(file == '-1'):
            exit()

        file+='.json'
        v = open(file,"r")
        text=v.read()
        v.close()
        getAllVertices(file, text)
        
start()
