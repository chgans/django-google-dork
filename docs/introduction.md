# Models and classes

`django-google-dork` is built around few models and classes.

On one hand `Django` models are used to manage your search campaigns and
store their results, on the other hand a couple of ad-hoc class are
used to perform the actual work in an asynchronous way.

### Class diagram					

                         Django Models  <- | ->	 Regular classes
        													  
               +--------+ *	   	   	   	   	   		 +----------+  	   	 
           	   |Campaign|------------, 	   	   	   	 | Scrapper	|		 
        	   +--------+  	  	 	 '	  			 +----------+		 
                   '   	   	  	 	 '	  			 	  '	   	   	   	 
        	   	   '*	   	  	 	 '	  			 	  '	   	   		 
        	   +--------+ *	   	   	 ' 	   	   	 		  '	  +----------+	 	 		  	 
        	   | Dork  	|-------, 	 '	  		   	   	  `---|Downloader| 	 
        	   +--------+  	0..1'    '0..1		    	  '	  +----------+ 	 
           	   	   ' 	   	  +----------+		  		  '	  	 		 	 
        	   	   '*	   	,-| Engine   |		 	 	  '	  			 	 
        	   +--------+ * ' +----------+ 	   	       	  '	  +----------+ 	 
        	   | Run    |---'             		  		  `---| Parser   |	 
        	   |        |---              		  			  +----------+	 
               +--------+ * ' +----------+									 
        	       '*       `-|Downloader|											 
        	       '*      	  +----------+							
        	   +--------+  	  										
        	   | Result |  	  										
           	   +--------+     										
			   		  	   	  										
### Class outline		   	  										
			   			   	  										
* Django models:		   	  										
    * `Campaign`: A logical container for `Dorks`					
    * `Dork`: A search expression or query							
    * `Engine`: A google engine, eg: google.com, google.fr, google.co.nz, ...
    * `Run`: A search instance of a `Dork` against a google `Engine`, yielding `Results`
    * `Result`: A search result, composed of a `title`, a `url` and a `summary`
    * `Downloader`: Downloads a given URL. **FIXME** 	
* Helper classes:		   
    * `Scrapper`: Downloads pages, parse them and recurse if needed
    * `Downloader`: Downloads a given url. **FIXME**
    * `Parser`: Parse a page and returns search results and page links
						   
## Asynchronous tasks	   

Under the hood `django-google-dork` uses `django-celery` to perform the background job, all you need to do is configure a periodic job to call the main task: `django_google_dork.dork_tem_all`.

For each `Dork` of each `Campaign`, `dork_them_all` will download the initial result page, and then in a recursive way, it will create additional asynchronous task to scrap all the other pages up to the last one.

**TODO?**

* Add a number of page limit to `Campaign`

## Diversity			   

### Dork

A `Campaign` allows you to use more than a `Dork` to find what you are
after, might it be because you're looking for something that requires
internationalised dork, for example *"Powered by Wordpress"* and
*"Fièrement propulsé par WordPress"* will gives you both English and
French websites based on `WordPress`.

### Engines				   
						   
Using `google.fr` to search for French stuff lead to significant
better results, thus the `Engine` model allows you to optionally
associate a specific `Engine` to a `Campaign` or a `Dork`.

At the same time using `google.com.br` to search for Russian stuff
might brings you unexpected but yet interesting results. This is why
if no `Engine` is associated with a `Campaign` or a `Dork`, then an
engine will be selected randomly.

If the list of `Engine` is empty, a default one will be created using
the hostname `google.com`.

### Downloaders			   

To avoid get banned by google search engines, you need to use
different IP addresses, that's what the `Downloader` is for. It's up
to you to implement it, you could for example use the python
`requests` module to proxy the queries to a pool of external machine.

The whole `Dork` run will be done using the same `Downloader` and the same
google `Engine`.

##  Example

Let say that you want to find r57 php shells around, so using the `Django Admin Panel`:

* You create a campaign that you name *r57 PHP Sh3lls*
* You create a dork with the query *intitle:r57shell +uname +rwx* and you assoicate it with the previous `Campaign`
* You create a new periodic task (let say that run every 6 hours), and you select the `django_google_dork.dork_tem` task

You can nowmonitor your `Celery` queue and as the tasks get executed you can start looking at the list of results.

