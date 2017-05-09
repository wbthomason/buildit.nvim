''' Standard builder definitions for BuildIt '''

import buildit.builders.cargo as cargo
import buildit.builders.cmake as cmake
import buildit.builders.gobuild as gobuild
import buildit.builders.make as make
import buildit.builders.oasis as oasis
import buildit.builders.stack as stack

BUILDER_DEFS = {
    'cargo': cargo.cargo,
    'cmake': cmake.cmake,
    'go build': gobuild.go_build,
    'make': make.make,
    'oasis': oasis.oasis,
    'stack': stack.stack
}
