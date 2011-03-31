class Scanline():
    def __init__(self,skip,speed,columns,rows):
        self.line = 0
        self.offset = 0
        self.skip = skip
        self.speed = speed
        self.rows = rows
        self.columns = columns
    def update(self):
        lines = []
        for i in range(0,self.speed):
            lines.append(((0,self.line),(self.columns,self.line)))
            self.line+= self.skip
            if self.line > self.rows:
                self.offset+=1
                self.line = self.offset
            if self.offset == self.skip:
                self.offset = 0
        return lines
