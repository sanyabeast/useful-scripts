for pkg in `brew list --formula -1 | egrep -v '\.|\.\.'`
  do echo $pkg `brew info $pkg | egrep '[0-9]* files, ' | sed 's/^.*[0-9]* files, \(.*\)).*$/\1/' | awk '{print $1;}/[0-9]$/{s+=$1};/[mM][bB]$/{s+=$1*(1024*1024);next};/[kK][bB]$/{s+=$1*1024;next} END { suffix=" KMGT"; for(i=1; s>1024 && i < length(suffix); i++) s/=1024; printf "\t(all versions: %0.1f%s)",s,substr(suffix, i, 1), $3; }'`
done