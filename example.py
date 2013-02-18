from highroller import Highroller    
hr = Highroller()
hr.domain = "http://localhost"
hr.inject_head = "<!-- headinject -->"
hr.inject_body = "<!-- bodyinject -->"
hr.register_additional_site("/index.html")
for element in hr.additional_sites:
    print "roll: {0}".format(element[0])
    hr.roll_site(element)
