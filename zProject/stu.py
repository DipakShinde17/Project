class Studentt():
    def __init__(self,id,name,clas,dept):
        self.eid = id
        self.ename = name
        self.clas = clas
        self.dept = dept

    def __str__(self):
        return f'{self.eid},{self.ename},{self.clas},{self.dept}'
    
    
