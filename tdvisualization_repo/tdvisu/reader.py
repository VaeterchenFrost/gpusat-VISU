# -*- coding: utf-8 -*-
"""Usage like:
import reader
r=reader.TwReader()
inp = r.from_file('gr5.td')
inp.num_vertices
inp.num_edges
inp.edges
"""

import logging
import sys

logger = logging.getLogger(__name__)


class Reader():
    @classmethod
    def from_file(cls, fname):
        with open(fname, "r") as file:
            return cls.from_string(file.read())

    @classmethod
    def from_stream(cls, stream):
        return cls.from_string(stream.read().decode())

    @classmethod
    def from_string(cls, string):
        instance = cls()
        instance.parse(string)
        return instance

    def parse(self, string):
        pass


class DimacsReader(Reader):
    def parse(self, string):
        self.problem_solution_type = "?"
        self.format = "?"
        lines = string.split("\n")
        body_start = self.preamble(lines)
        self.store_problem_vars()
        self.body(lines[body_start:])

    def store_problem_vars(self):
        pass

    @staticmethod
    def is_comment(line):
        return line.startswith("c ") or line == "c"

    def body(self, lines):
        pass

    def preamble(self, lines):
        for lineno, line in enumerate(lines):
            if line.startswith("p ") or line.startswith("s "):
                line = line.split()
                self.problem_solution_type = line[0]
                self.format = line[1]
                self._problem_vars = line[2:]
                return lineno + 1
            elif not line or self.is_comment(line):
                continue
            else:
                logger.warning(
                    "Invalid content in preamble at line %d: %s", lineno, line)
        logger.error("No type found in DIMACS file!")
        sys.exit(1)


def _add_edge_to(edges, adjacency_list, vertex1, vertex2):
    if vertex1 in adjacency_list:
        adjacency_list[vertex1].add(vertex2)
    else:
        adjacency_list[vertex1] = {vertex2}
    if vertex2 in adjacency_list:
        adjacency_list[vertex2].add(vertex1)
    else:
        adjacency_list[vertex2] = {vertex1}
    edges.add((vertex1, vertex2))


class TwReader(DimacsReader):
    def __init__(self):
        super().__init__()
        self.edges = set()
        self.adjacency_list = {}

    def store_problem_vars(self):
        self.num_vertices = int(self._problem_vars[0])
        self.num_edges = int(self._problem_vars[1])

    def body(self, lines):
        if self.format != "tw":
            logger.error("Not a tw file!")
            sys.exit(1)

        for lineno, line in enumerate(lines):
            if not line or self.is_comment(line):
                continue

            line = line.split()
            if len(line) != 2:
                logger.warning(
                    "Expected exactly 2 vertices at line %d, but %d found",
                    lineno,
                    len(line))
            vertex1 = int(line[0])
            vertex2 = int(line[1])

            _add_edge_to(self.edges, self.adjacency_list, vertex1, vertex2)

        if len(self.edges) != self.num_edges:
            logger.warning(
                "Number of edges mismatch preamble (%d vs %d)", len(
                    self.edges), self.num_edges)
