from highroller import Highroller


def test_exclude():
    """Check if the exclude function works and only removed the start and end tags and everything in between, nothing more or less"""

    test_case = """<html><body><h1>It works!</h1>
<p>This is the default web page for this server.</p>
<p>The web server software is running but no content has been added, yet.</p>
<!-- -->
<!-- highroller: exclude start -->
dont show me
<!-- highroller: exclude end -->

<!-- highroller: additional start --><a href="index2.html">Index 2</a><!-- highroller: additional end -->

<!-- highroller: exclude start -->
dont show me 2
<!-- highroller: exclude end -->
</body></html>"""

    test_response = """<html><body><h1>It works!</h1>
<p>This is the default web page for this server.</p>
<p>The web server software is running but no content has been added, yet.</p>
<!-- -->


<!-- highroller: additional start --><a href="index2.html">Index 2</a><!-- highroller: additional end -->


</body></html>"""

    hr = Highroller()
    response = hr._run_exclude(test_case)
    assert test_response == response


def test_additional():
    test_case = """<html><body><h1>It works!</h1>
<p>This is the default web page for this server.</p>
<p>The web server software is running but no content has been added, yet.</p>
<!-- -->
<!-- highroller: exclude start -->
dont show me
<!-- highroller: exclude end -->

<!-- highroller: additional start --><a href="index2.html">Index 2</a><!-- highroller: additional end -->

<!-- highroller: exclude start -->
dont show me 2
<!-- highroller: exclude end -->
</body></html>"""

    test_response = """<html><body><h1>It works!</h1>
<p>This is the default web page for this server.</p>
<p>The web server software is running but no content has been added, yet.</p>
<!-- -->
<!-- highroller: exclude start -->
dont show me
<!-- highroller: exclude end -->

<a href="/static/index2.html">Index 2</a>

<!-- highroller: exclude start -->
dont show me 2
<!-- highroller: exclude end -->
</body></html>"""

    hr = Highroller()
    response = hr._run_additional(test_case)
    assert test_response == response

def test_include():
    test_case = """<html><body><!-- highroller: include start --<h1>It works!</h1>!-- highroller: include end -->
<p>This is the default web page for this server.</p>
<p>The web server software is running but no content has been added, yet.</p>
<!-- --><!-- highroller: include start --<h1>Show me!</h1>!-- highroller: include end -->
<!-- highroller: exclude start -->
dont show me 2
<!-- highroller: exclude end -->
</body></html>"""

    test_response = """<html><body><h1>It works!</h1>
<p>This is the default web page for this server.</p>
<p>The web server software is running but no content has been added, yet.</p>
<!-- --><h1>Show me!</h1>
<!-- highroller: exclude start -->
dont show me 2
<!-- highroller: exclude end -->
</body></html>"""

    hr = Highroller()
    response = hr._run_include(test_case)
    print response
    assert test_response == response


def test_register_additional_site():
    test_case = "/index.html"
    test_response = "/static/index.html"
    hr = Highroller()
    response = hr.register_additional_site(test_case)
    assert response == test_response
    assert [(test_case, test_response)] == hr.additional_sites

    # add again the same thing, nothing should change
    response = hr.register_additional_site(test_case)
    assert response == test_response
    assert [(test_case, test_response)] == hr.additional_sites


def test_inject():
    def _get_content_custom(self):
        response = """<html><head></head><body><h1>It works!</h1></body></html>"""
        return response

    hr = Highroller()
    hr._get_content = _get_content_custom
    hr.inject_head = "<!-- headinject -->"
    hr.inject_body = "<!-- bodyinject -->"
    hr.register_additional_site("/index.html")
    assert len(hr.additional_sites) == 1
    for element in hr.additional_sites:
        response = hr.roll_site(element)
        assert response == """<html><head><!-- headinject --></head><body><h1>It works!</h1><!-- bodyinject --></body></html>"""

if __name__ == '__main__':
    print "test"
    test_include()
