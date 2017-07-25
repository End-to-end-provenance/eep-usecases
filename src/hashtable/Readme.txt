These scripts demonstrate writing to hashtable.csv in the ~/.ddg folder.

The first script, HT.R, demonstrates writing to a file.
The second script, HT2.R, demonstrates reading from a file. For the purposes of
this example and checking hashes, HT2.R reads the files that are output by HT.R.
The third script, HT3.R, demonstrates both reading and writing.

If one runs the same script multiple times, all entries in the hashtable with
the same path to their DDG should be removed before the new entries are added.
For example, if the scripts were run sequentially, the data should be printed in
order in hashtable.csv, with the data from HT.R printed first, the data from
HT2.R printed second, and the data from HT3.R printed last.

If one was to run HT2.R again and examine hashtable.csv, the entries from HT.R
would be printed first, the entries from HT3.R would be printed second, and the
entries from HT3.R would be printed last, as it was run most recently.

HT4.R and HT5.R are included simply to demonstrate that multiple different
workflows can be loaded, and function almost identically to HT.R and HT3.R.

HTEmpty.R demonstrates that the hashtable is not modified if the file being run
makes no read or write attempts.

Additional information from the hashtable is written to the ddg.json and the
ddg.txt in the local ddg directory.
