from collections import Counter
import defines as d
file_to_mine = "./logs/logfile-full-2015-02-12.txt"
needle = "HTTP Request Generated:"
discard_needle = "9543679247"

def mine_logs_for_requests():
    logfile = [l.strip() for l in open(file_to_mine).readlines() if l.strip != ""]
    count = 0
    unique_urls = [l.strip() for l in open(d.log_dir+d.pending_reqs,"w+").readlines()]
    for haystack in logfile:
        if needle in haystack and (d.script + d.guinea_cc) in haystack:
            if not discard_needle in haystack:
                count += 1
                haystack = haystack.split(needle)[-1]
                unique_urls.append(haystack.strip())
    
    unique_urls = Counter(unique_urls)
    print(str(count)+" url mentions found!")
    print(str(len(unique_urls))+" unique urls found!")
    f = open(d.log_dir + d.pending_reqs,"w")
    for unique_url in unique_urls:
        print(unique_url)
        number = unique_url.split(d.script)[-1].split(d.syslang_prefix)[0].strip()
        open(d.reminder_list,"a").write(number+"\n")
        f.write(unique_url + "\n")
    f.close()
    print("Finished!")
            
if __name__ == '__main__':
    mine_logs_for_requests()
    