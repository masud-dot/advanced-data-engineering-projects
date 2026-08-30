import time
class PipelineMetrics:
    def __init__(self,pipeline_name): self.name=pipeline_name; self.start_time=time.time(); self.rows=0; self.errors=0
    def record_rows(self,count): self.rows+=count
    def record_error(self): self.errors+=1
    def duration(self): return round(time.time()-self.start_time,2)
    def summary(self): return {'pipeline':self.name,'rows':self.rows,'errors':self.errors,'duration':self.duration()}
