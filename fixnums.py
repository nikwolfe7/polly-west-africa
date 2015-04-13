f = "allph_game.txt"
def main():
    numbers = [l.strip() for l in open(f).readlines()]
    fixed = set()
    for num in numbers:
        if len(num) >= 9:
            if num.startswith("1"):
                num = "00" + num
            if num.startswith("6"):
                num = "224" + num
            fixed.add(num)
    
    o = open(f,"w")
    for num in fixed: o.write(num + "\n")
    o.close()
        

if __name__ == '__main__': main()
    