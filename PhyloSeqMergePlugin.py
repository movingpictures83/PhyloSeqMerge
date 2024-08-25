import PyPluMA

class PhyloSeqMergePlugin:
    def input(self, infile):
       self.parameters = dict()
       thefile = open(infile, 'r')
       for line in thefile:
           contents = line.strip().split('\t')
           self.parameters[contents[0]] = contents[1]

       self.abundfile = open(PyPluMA.prefix()+"/"+self.parameters["abund"], 'r')
       self.taxfile = open(PyPluMA.prefix()+"/"+self.parameters["tax"], 'r')

       self.abundances = []
       self.abundheader = self.abundfile.readline().strip()
       for line in self.abundfile:
           contents = line.strip().split(',')
           self.abundances.append(contents)

       self.taxonomy = []
       self.taxheader = self.taxfile.readline().strip()
       for line in self.taxfile:
           contents = line.strip().split(',')
           self.taxonomy.append(contents)
       self.NCBI = self.taxheader.strip().split(',').index('\"NCBI\"')

    def run(self):
       self.taxa = dict()
       for i in range(len(self.taxonomy)):
           NCBIid = self.taxonomy[i][self.NCBI] #NCBI ID
           if (NCBIid not in self.taxa):  # If first time, create list with self
              self.taxa[NCBIid] = [self.taxonomy[i][0]]
           else:  # Else, append
              self.taxa[NCBIid].append(self.taxonomy[i][0])

       abundancesToRemove = []
       taxonomyToRemove = []
       for i in range(len(self.abundances)):
           # For each taxon in the abundance file
           # Find in dictionary
           taxon = self.abundances[i][0]
           for key in self.taxa:
               # If the taxon is not the first entry in the dictionary, it is a duplicate
               # It then needs to be merged with the first
               if (taxon in self.taxa[key] and self.taxa[key].index(taxon) != 0):
                  firsttaxon = self.taxa[key][0]
                  # Find that first taxon in the abundances
                  for j in range(len(self.abundances)):
                      if (self.abundances[j][0] == firsttaxon):
                          for k in range(1, len(self.abundances[j])):
                             self.abundances[j][k] = str(float(self.abundances[j][k])+float(self.abundances[i][k]))
                  abundancesToRemove.append(i)
                  for j in range(len(self.taxonomy)):
                     if (self.taxonomy[j][0] == taxon):
                         taxonomyToRemove.append(j)
       self.finalAbundances = []
       self.finalTaxa = []

       for i in range(len(self.abundances)):
            if (i not in abundancesToRemove):
                self.finalAbundances.append(self.abundances[i])
       for i in range(len(self.taxonomy)):
            if (i not in taxonomyToRemove):
                self.finalTaxa.append(self.taxonomy[i])

    def output(self, outfile):
       abundout = open(outfile+".tab.csv", 'w')
       taxaout = open(outfile+".tax.csv", 'w')
       abundout.write(self.abundheader+"\n")
       taxaout.write(self.taxheader+"\n")
       for i in range(len(self.finalAbundances)):
          for j in range(len(self.finalAbundances[i])):
              abundout.write(self.finalAbundances[i][j])
              if (j != len(self.finalAbundances[i])-1):
                      abundout.write(",")
              else:
                      abundout.write('\n')

       for i in range(len(self.finalTaxa)):
          for j in range(len(self.finalTaxa[i])):
              taxaout.write(self.finalTaxa[i][j])
              if (j != len(self.finalTaxa[i])-1):
                      taxaout.write(",")
              else:
                      taxaout.write('\n')
