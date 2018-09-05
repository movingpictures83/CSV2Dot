import sys
#import numpy
import PyPluMA


class CSV2DotPlugin:
   def input(self, filename):
      filestuff = open(filename, 'r')
      networkdata = dict()
      for line in filestuff:
         keyval = line.split('\t')
         networkdata[keyval[0]] = keyval[1].strip()
      if (not networkdata.has_key('correlations')):
         PyPluMA.log("Error in CSV2DotPlugin, no correlations file defined")
         sys.exit(1)
      else:
         self.correlations = open(networkdata['correlations'], 'r')
      if (networkdata.has_key('abundances')):
         self.abundances = open(networkdata['abundances'], 'r')
      else:
         self.abundances = None
      if (networkdata.has_key('clusters')):
         self.clusters = open(networkdata['clusters'], 'r')
      else:
         self.clusters = None

   def run(self):
      ##########################################################
      # CORRELATIONS
      firstline = self.correlations.readline()
      self.bacteria = firstline.split(',')
      if (self.bacteria.count('\"\"') != 0):
         self.bacteria.remove('\"\"')
      for i in range(0, len(self.bacteria)):
         self.bacteria[i] = self.bacteria[i].strip()
      self.n = len(self.bacteria)
      self.ADJ = []
      i = 0
      for line in self.correlations:
         contents = line.split(',')
	 self.ADJ.append([])
         for j in range(self.n):
            value = float(contents[j+1])
            if (i != j and value != 0):
               self.ADJ[i].append(value)
            else:
               self.ADJ[i].append(0)
         i += 1
      ##########################################################

      ##########################################################
      # ABUNDANCES
      if (self.abundances != None):
         firstline = self.abundances.readline()
         self.bacteria = firstline.split(',')
         if (self.bacteria.count('\"\"') != 0):
            self.bacteria.remove('\"\"')
         self.n = len(self.bacteria)
         self.ABUND = []
         for i in range(self.n):
            self.ABUND.append(0.0)
         m = 0
         for line in self.abundances:
            contents = line.split(',')
            for j in range(self.n):
               value = float(contents[j+1])
               self.ABUND[j] += value*100.0
            m += 1
         for i in range(self.n):
            self.ABUND[i] /= m
      ##########################################################
      
      ##########################################################
      # CLUSTERS
      if (self.clusters != None):
         self.CLUST = []
         for line in self.clusters:
            contents = line.split(',')
            if (contents[0] == "\"\""):
               self.CLUST.append([])
            else:
               self.CLUST[len(self.CLUST)-1].append(contents[1].strip())
      ##########################################################

   def output(self, filename):
      #gmlfilename = self.myfile[0:len(self.myfile)-3] + "gml"
      #gmlfile = open(gmlfilename, 'w')
      dotfile = open(filename, 'w')
      PyPluMA.log("Writing Dot file ")

      dotfile.write("graph {\n")
      dotfile.write("forcelabels=true;\n")
      dotfile.write("penwidth=10;\n")
      if (self.abundances != None):
         for i in range(self.n):
            dotfile.write(self.bacteria[i]+"[label="+self.bacteria[i]+",fontsize="+str(int(200+self.ABUND[i]*100))+",penwidth=10,width="+str('{:f}'.format(20+self.ABUND[i]*10))+",height="+str('{:f}'.format(20+self.ABUND[i]*10))+"];\n")
      else:
         for i in range(self.n):
            dotfile.write(self.bacteria[i]+"[label="+self.bacteria[i]+",fontsize=100,penwidth=10,width=10,height=10];\n")


      for i in range(self.n):
         for j in range(i+1, self.n):
            if (self.ADJ[i][j] != 0):
               dotfile.write(self.bacteria[i]+" -- "+self.bacteria[j]+"[w="+str(self.ADJ[i][j])+",color=\"")
               if (self.ADJ[i][j] < 0):
                  dotfile.write("red")
               else:
                  dotfile.write("green")
               dotfile.write("\";penwidth="+str(self.ADJ[i][j]*10)+"];\n")

      if (self.clusters != None):
       count = 0
       for cluster in self.CLUST:
         dotfile.write("subgraph clusterC"+str(count)+" { ")
         for node in cluster:
            dotfile.write(node+"; ")
         dotfile.write("}\n")
         count += 1
         
       dotfile.write("}\n")




