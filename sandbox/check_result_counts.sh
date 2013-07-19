cut -f2,3,4 -d'/' pairwise_stats.txt | uniq | grep -v '#' | cut -f1,2 -d'/' | uniq -c | sort -n -r
cut -f1 solo_stats.txt | uniq | grep -v '#' | cut -f2,3 -d'/' | uniq -c | sort -n -r