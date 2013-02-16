highroller
============

This is your dynamic webpage::

   <html><body>
   <h1>It works!</h1>
   all is normal
   <!-- highroller: exclude start -->
   dont render me
   <!-- highroller: exclude end -->
   <!-- highroller: additional start --><a href="index2.html">Index 2</a><!-- highroller: additional end -->
   </body></html>

Highroller removes everything between the "exculude" tags and looks for links wrapped in an "additional" tags. The additional links are gathered and then crawled as well. THe link itself is rewritten to match the new static loation of the new generated link target.
