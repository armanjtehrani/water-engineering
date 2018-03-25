
def copy2dir(source, destination):
    src = open(source,"r")
    dst = open(destination,"w")

    file = src.readlines()

    for line in file:
        dst.write(line)

    src.close()
    dst.close()

#copy2dir("testfile.txt", "staticmaps/new.txt")

