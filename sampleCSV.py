import pandas
import sys
import getopt

class sampleCSV():
    #-------------------------------------------------------------
    # Sample the movie ratings csv.
    #-------------------------------------------------------------
    def sample(filename, N, seed):
        if N<0:
            N=sampleCSV.defaultN
        if seed<0:
            seed=sampleCSV.defaultSeed
        fullDF=pandas.read_csv(filename)
        sampleDF=fullDF.sample(N,random_state=seed)
        return sampleDF
    
    #-------------------------------------------------------------
    # Default sample number.
    #-------------------------------------------------------------
    defaultN=100000
    
    #-------------------------------------------------------------
    # Default seed number.
    #-------------------------------------------------------------
    defaultSeed=478596
    
    #-------------------------------------------------------------
    # Save the sampled movie ratings csv.
    #-------------------------------------------------------------
    def writeSample(df, prefix, N, seed):
        if N<0:
            N=sampleCSV.defaultN
        if seed<0:
            seed=sampleCSV.defaultSeed
        filename=prefix+'_N'+str(N)+'_S'+str(seed)+'.csv'
        df.to_csv(filename,index=False)
    
    #-------------------------------------------------------------
    # Usage options.
    #-------------------------------------------------------------
    def usage():
        print("Sample options:")
        print("-h or --help")
        print("      Print this messege and quit")
        print("-i [filename] or --input=[filename]")
        print("      Read data from [filename]. Required!")
        print("-n [integer] or --number=[integer]")
        print("      Sample this many lines. Default=",sampleCSV.defaultN,".")
        print("-s [integer] or --seed=[integer]")
        print("      Random number seed. Default=",sampleCSV.defaultSeed,".")



def main():
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hi:n:s:",
        ["help","input=","number=","seed="])
    except getopt.GetoptError as err:
        print(err)
        sampleCSV.usage()
        sys.exit(2)
    filename=''
    N=-1
    seed=-1
    for o,a in opts:
        if o in ("-h", "--help"):
            sampleCSV.usage()
            sys.exit()
        elif o in ("-i", "--input"):
            filename=a
        elif o in ("-n", "--number"):
            N=int(a)
        elif o in ("-s", "--seed"):
            seed=int(a)
        else:
            assert False, "unhandled option"
    if len(filename)==0:
        sampleCSV.usage()
        sys.exit()
    sampleDF=sampleCSV.sample(filename,N,seed)
    sampleCSV.writeSample(sampleDF,filename.split('.')[0],N,seed)


if __name__ == "__main__":
    main()
