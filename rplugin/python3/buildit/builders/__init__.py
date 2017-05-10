''' Standard builder definitions for BuildIt '''

from . import cargo
from . import cmake
from . import gobuild
from . import make
from . import oasis
from . import stack

BUILDER_DEFS = {
    'cargo': cargo.cargo,
    'cmake': cmake.cmake,
    'go build': gobuild.go_build,
    'make': make.make,
    'oasis': oasis.oasis,
    'stack': stack.stack
}
