def main():
    numbers = [l.strip() for l in open("PollyCallers.csv").readlines()]
    fixed = set()
    for num in numbers:
        if len(num) >= 9:
            if num.startswith("1"):
                num = "00" + num
            if num.startswith("6"):
                num = "224" + num
            fixed.add(num)
    
    o = open("PollyCallers.csv","w")
    for num in fixed: o.write(num + "\n")
    o.close()
        
        
    

if __name__ == '__main__': main()
    