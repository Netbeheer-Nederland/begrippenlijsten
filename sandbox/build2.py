from __future__ import annotations

from dataclasses import dataclass

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.parser import Parser
from rdflib import Graph
from rdflib.namespace import RDF, SKOS


@dataclass
class SkosBlock:
    graph: Graph
    source: str

    @property
    def concepts(self):
        return list(self.graph.subjects(RDF.type, SKOS.Concept))

    @property
    def schemes(self):
        return list(self.graph.subjects(RDF.type, SKOS.ConceptScheme))


class SkosExtension(Extension):
    tags = {"skos"}

    def parse(self, parser: Parser):
        lineno = next(parser.stream).lineno

        # Parse:
        #
        #     {% skos as vocabulary %}
        #
        # We expect "as" followed by an identifier.
        if not parser.stream.skip_if("name:as"):
            parser.fail(
                "expected 'as' followed by a variable name",
                lineno,
            )

        variable = parser.stream.expect("name")

        body = parser.parse_statements(
            end_tokens=("name:endskos",),
            drop_needle=True,
        )

        call = nodes.CallBlock(
            self.call_method("_parse_skos"),
            [],
            [],
            body,
        )

        return nodes.Assign(
            nodes.Name(variable.value, "store"),
            call,
        ).set_lineno(lineno)

    def _parse_skos(self, caller):
        source = caller()

        graph = Graph()
        graph.parse(
            data=source,
            format="turtle",
        )

        return SkosBlock(
            graph=graph,
            source=source,
        )


if __name__ == "__main__":
    from jinja2 import Environment, FileSystemLoader

    env = Environment(
        loader=FileSystemLoader("src"),
        extensions=[
            SkosExtension,
        ],
    )

    shacl_template = env.get_template("netbeheerder.adoc")
    shacl = shacl_template.render()

    print(shacl)
