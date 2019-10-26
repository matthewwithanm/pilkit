import os, sys, io, base64
from docutils import nodes
from sphinx.directives.code import CodeBlock


def visit_pil(self, node):
    pass


def depart_pil(self, node):
    pass


class PILNode(nodes.Structural, nodes.Element):
    pass


class PILDirective(CodeBlock):
    has_content = True

    def run(self):
        code_node = CodeBlock.run(self)
        nodes.image()

        from PIL import Image

        lib_path = os.path.abspath('..')
        working_path = os.path.dirname(os.path.realpath(__file__))
        static_path = os.path.join(working_path, '..', '_static')

        sys.path.append(lib_path)
        os.chdir(working_path)

        node = PILNode()

        g = globals()
        l = locals()
        for line in self.content:
            result = exec(line, g, l)

        buffer = io.BytesIO()
        new_img = l.get('new_img')
        new_img.save(buffer, format='PNG')

        image_node = nodes.image()
        image_node['alt'] = 'New Image'
        image_node['uri'] = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()

        node += code_node
        node += image_node

        return [node]


def setup(app):
    app.add_node(PILNode, html=(visit_pil, depart_pil))
    app.add_directive('pil-block', PILDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
