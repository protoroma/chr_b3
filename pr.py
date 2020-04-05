class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append("%s='%s'" % (attribute, value))
        attrs = " ".join(attrs)
        if len(self.children) > 0:
            opening = "\n        <{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "\n        </%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "\n        <{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            else:
                return "        <{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )


class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass  

    def __str__(self):
        stag = "\n    <%s>\n" % self.tag
        for child in self.children:
            stag += str(child)
        stag += "\n    </%s>" % self.tag
        return stag

class HTML:
    def __init__(self, output=None):
        self.output = output  
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)    

    def __str__(self):
        html = "<html>"
        for child in self.children:
            html += str(child)
        html += "\n</html>"
        return html

if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head.children.append(title)
            doc.children.append(head)
        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1: #  запятая klass=("main-text",) для того, чтобы пробел не ставился между каждым символом одиночного класса
                h1.text = "Test"
                body.children.append(h1)
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as p:
                    p.text = "another test"
                    div.children.append(p)
                with Tag("img", scr="/icon.png", data_image="responsive", is_single=True) as img:
                    div.children.append(img)
                body.children.append(div)
            doc.children.append(body)