from Bio import SeqIO
import sys 

def main():

    #Setup variables (could parse command line args instead)
    file_f = "/home/vxue/data/SORTCERY_PUBLICATION/SORTCERY_spec_dna/140828Kea_D14-3934_1_sequence.fastq"
    file_r = "/home/vxue/data/SORTCERY_PUBLICATION/SORTCERY_spec_dna/140828Kea_D14-3934_2_sequence.fastq"
    dir_out = "/home/vxue/data/SORTCERY_PUBLICATION/SORTCERY_spec_dna/workspace/"
    myFormat = "fastq-illumina" 
    numBarcodes = (24*7)
    
    records_f = SeqIO.parse(open(file_f,"rU"), myFormat)
    records_r = SeqIO.parse(open(file_r,"rU"), myFormat)
    
    myOpenOutStreams = openOutStreams(dir_out,numBarcodes)
        
    for (forward, reverse) in zip(records_f,records_r):   
        barcodeIndex = getBarcode(forward)
        if(barcodeIndex>-1):
            #print barcodeIndex, forward.seq ,reverse.seq
            SeqIO.write(forward, myOpenOutStreams[barcodeIndex], myFormat)
            SeqIO.write(reverse, myOpenOutStreams[barcodeIndex], myFormat)

    closeOutStreams(myOpenOutStreams)
    
    return 1
    
def openOutStreams(dir_out,num):
    myArray = []
    for i in range(num):
        myArray.append(open(dir_out+"barcode_"+str(i),'w'))
    return myArray

def closeOutStreams(array):
    for each in array:
        each.close()
            
def getBarcode(forward):
    sequence = str(forward.seq)
    forward_Quality = forward.letter_annotations['phred_quality']
    
    #Fist check if barcode2 is available
    myBarcodes2 = ["ATCACG","ACAGTG","CGATGT","CAGATC","GATCAG","GCCAAT","TTAGGC"]
    myBarcodes2Index=-1
    myBarcodes2Index = getClosestBarcode(forward.id[forward.id.index('#')+1:forward.id.index('#')+7],myBarcodes2,5) 
    if(myBarcodes2Index==-1):
        return -1
        

    #Then check barcode1 quality
    for i in range(5):
        if forward_Quality[i]<20:
            return -1
    
    myBarcodes = ["ACTCG","ACTGT", "AATGC", "AGTCA", "ATACG", "ATAGC",
                    "CGATC", "CTAAG", "CTCGA", "CGAAT", "CTGGT", "CGGTT",
                    "GACTT", "GTTCA", "GATAC", "GAGCA", "GATGA", "GTCTG",
                    "TCGGA", "TGACC", "TACTG", "TCCAG", "TCGAC", "TAGCT"]
    firstFive = sequence[0:5]
    if(firstFive in myBarcodes):
        return (myBarcodes2Index*24)+myBarcodes.index(firstFive)
    else:
        return -1

def getClosestBarcode(seq,myBarcodes2,mustMatch):
    bestIndex = -1
    bestScore = -1
    mySeq = list(seq)
    
    for index in range(len(myBarcodes2)):
        mySum = 0
        for nt in range(6):
            if(mySeq[nt]==myBarcodes2[index][nt]):
                mySum+=1
        if(mySum>bestScore):
            bestIndex=index
            bestScore=mySum
            
    if(bestScore>=mustMatch):
        return bestIndex
    else:
        return -1

    
if __name__ == "__main__":
    sys.exit(main())
