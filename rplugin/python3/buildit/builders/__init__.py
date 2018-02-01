''' Standard builder definitions for BuildIt '''

from . import cargo, cmake, gobuild, jbuilder, make, meson, oasis, stack

BUILDER_DEFS = {
    'cargo': cargo.cargo,
    'cmake': cmake.cmake,
    'meson': meson.meson,
    'go build': gobuild.go_build,
    'jbuilder': jbuilder.jbuilder,
    'make': make.make,
    'oasis': oasis.oasis,
    'stack': stack.stack
}
