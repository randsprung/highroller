highroller
============

Get static light versions of a (dynamic) webpage and sub-pages. 
You have to controll over the original source and annotate it with some custom markup so highroller knows what can be removed and what links to follow.

For Example, this is your dynamic webpage::

   <html><body>
   <h1>It works!</h1>
   all is normal
   <!-- highroller: exclude start -->
   dont render me
   <!-- highroller: exclude end -->
   <!-- highroller: additional start --><a href="index2.html">Index 2</a><!-- highroller: additional end -->
   </body></html>

Highroller retrieves and saves the HTML. He removes everything between the "exculude" tags and looks for links wrapped in an "additional" tags. The additional links are gathered and then crawled as well. The link itself is rewritten to match the new static loation of the new generated link target.i

Place the script somewhere nice, include the Highrollerclass and use it::
   from highroller import Highroller
   hr = Highroller()
   hr.domain = "http://localhost"
   hr.register_additional_site("/index.html")
   for element in hr.additional_sites:
       hr.roll_site(element)
