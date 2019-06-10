from multiprocessing import Pool

def job(tupleData):
    try:
        for x in tupleData:
            print(x)
    except Exception("Some error") as e:
        print(e)
        return f"Error while doing job{tupleData}"
    return "No error"

if __name__ == "__main__":

    tupleList = [("name","adress")]

    #use case when you want to return some info
    pool = Pool(10)

    map = pool.map_async(func=job,iterable=tupleList)

    pool.close()
    pool.join()


    result = map.get()
    print(result)
    # use if return not important
    pool = Pool(10)
    for obj in tupleList:
        pool.apply(func=job,args=(obj,))
    pool.close()
    pool.join()
    print("end of program")