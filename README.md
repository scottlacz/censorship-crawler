# censorship-crawler
Final Project for Computer Security

This script pulls random words from a list (in my case, a list of 4.5 million English Wikipedia titles) sends out queries to Baidu.
Theoretically, it checks if the query was censored by looking for a line in the HTML that states (in English):
"In accordance with relevant laws, regulations, and policies, some search results could not be displayed"

Run it from the command line and pass it a value like 5. That's the number of requests it will send.

ISSUES:
I can't find a reliable proxy server into China.
Ideally, I would pull from a list of known available proxies on the web and use a different one upon completion of each request. 

Because I can't reliably proxy into China, I can't actually set off the censors.
Therefore, I don't know what HTML tags to look for in my request.

Censors are normally set off by Chinese words, making the use of English titles ineffective.
To fix this, either translate the current title list or grab a list of banned words in Chinese.

If you want to try it yourself, here's the list of words I use (from November 2016):
https://dumps.wikimedia.org/enwiki/20161020/
